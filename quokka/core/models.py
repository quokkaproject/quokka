#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
import random
from flask import url_for, current_app, redirect, request
from flask.ext.mistune import markdown

from quokka.core import TEXT_FORMATS
from quokka.core.db import db
from quokka.core.fields import MultipleObjectsReturned
from quokka.modules.accounts.models import User
from quokka.utils.text import slugify
from quokka.utils import get_current_user_for_models
from quokka.utils.shorturl import ShorterURL
from quokka.utils.settings import get_setting_value, get_site_url
from .base_models.custom_values import HasCustomValue
from .admin.utils import _l

logger = logging.getLogger()


###############################################################
# Commom extendable base classes
###############################################################

class ContentFormat(object):
    content_format = db.StringField(
        choices=TEXT_FORMATS,
        default=get_setting_value('DEFAULT_TEXT_FORMAT', 'html')
    )


class Dated(object):
    available_at = db.DateTimeField(default=datetime.datetime.now)
    available_until = db.DateTimeField(required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)


class Owned(object):
    created_by = db.ReferenceField(User)
    last_updated_by = db.ReferenceField(User)
    authors = db.ListField(db.ReferenceField(User))

    def get_authors(self, sortedf=None):
        return set(self.authors + [self.created_by])

    @property
    def has_multiple_authors(self):
        return len(self.get_authors()) > 1


class Publishable(Dated, Owned):
    published = db.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()

        user = get_current_user_for_models()

        if not self.id and not self.created_by:
            self.created_by = user
        self.last_updated_by = user

        super(Publishable, self).save(*args, **kwargs)


class Slugged(object):
    slug = db.StringField(max_length=255, required=True)

    def validate_slug(self, title=None):
        if self.slug:
            self.slug = slugify(self.slug)
        else:
            self.slug = slugify(title or self.title)


class LongSlugged(Slugged):
    long_slug = db.StringField(unique=True, required=True)
    mpath = db.StringField()

    def _create_mpath_long_slug(self):
        if isinstance(self, Channel):
            if self.parent and self.parent != self:
                self.long_slug = "/".join(
                    [self.parent.long_slug, self.slug]
                )
                self.mpath = "".join(
                    [self.parent.mpath, self.slug, ',']
                )
            else:
                self.long_slug = self.slug
                self.mpath = ",%s," % self.slug
        elif isinstance(self, Content):
            self.long_slug = "/".join(
                [self.channel.long_slug, self.slug]
            )
            self.mpath = "".join([self.channel.mpath, self.slug, ','])

    def validate_long_slug(self):
        self._create_mpath_long_slug()

        filters = dict(long_slug=self.long_slug)
        if self.id:
            filters['id__ne'] = self.id

        exist = self.__class__.objects(**filters)
        if exist.count():
            if current_app.config.get('SMART_SLUG_ENABLED', False):
                self.slug = "{0}-{1}".format(self.slug, random.getrandbits(32))
                self._create_mpath_long_slug()
            else:
                raise db.ValidationError(
                    _l("%(slug)s slug already exists",
                       slug=self.long_slug)
                )


class Tagged(object):
    tags = db.ListField(db.StringField(max_length=50))


class Ordered(object):
    order = db.IntField(required=True, default=1)


class ChannelConfigs(object):
    content_filters = db.DictField(required=False, default=lambda: {})
    inherit_parent = db.BooleanField(default=True)


class TemplateType(HasCustomValue):
    title = db.StringField(max_length=255, required=True)
    identifier = db.StringField(max_length=255, required=True, unique=True)
    template_suffix = db.StringField(max_length=255, required=True)
    theme_name = db.StringField(max_length=255, required=False)

    def __unicode__(self):
        return self.title


class ChannelType(TemplateType, ChannelConfigs, db.DynamicDocument):
    """Define the channel template type and its filters"""


class ContentProxy(db.DynamicDocument):
    content = db.GenericReferenceField(required=True, unique=True)

    def __unicode__(self):
        return self.content.title


class Channel(Tagged, HasCustomValue, Publishable, LongSlugged,
              ChannelConfigs, ContentFormat, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    description = db.StringField()
    show_in_menu = db.BooleanField(default=False)
    is_homepage = db.BooleanField(default=False)
    roles = db.ListField(
        db.ReferenceField('Role', reverse_delete_rule=db.PULL))
    include_in_rss = db.BooleanField(default=True)
    indexable = db.BooleanField(default=True)
    canonical_url = db.StringField()
    order = db.IntField(default=0)

    parent = db.ReferenceField('self', required=False, default=None,
                               reverse_delete_rule=db.DENY)

    per_page = db.IntField(default=0)
    aliases = db.ListField(db.StringField(), default=[])
    channel_type = db.ReferenceField(ChannelType, required=False,
                                     reverse_delete_rule=db.NULLIFY)

    redirect_url = db.StringField(max_length=255)
    render_content = db.ReferenceField(ContentProxy,
                                       required=False,
                                       reverse_delete_rule=db.NULLIFY)
    sort_by = db.ListField(db.StringField(), default=[])

    meta = {
        'ordering': ['order', 'title'],
    }

    def get_text(self):
        if self.content_format == "markdown":
            return markdown(self.description)
        else:
            return self.description

    def get_content_filters(self):
        filters = {}
        if self.channel_type and self.channel_type.content_filters:
            filters.update(self.channel_type.content_filters)
        if self.content_filters:
            filters.update(self.content_filters)
        return filters

    def get_ancestors_count(self):
        """
        return how many ancestors this node has based on slugs
        """
        return len(self.get_ancestors_slugs())

    def get_ancestors_slugs(self):
        """return ancestors slugs including self as 1st item
        >>> channel = Channel(long_slug='articles/technology/programming')
        >>> channel.get_ancestors_slugs()
        ['articles/technology/programming',
         'articles/technology',
         'articles']
        """

        channel_list = []
        channel_slugs = self.long_slug.split('/')
        while channel_slugs:
            channel_list.append("/".join(channel_slugs))
            channel_slugs.pop()
        return channel_list

    def get_ancestors(self, **kwargs):
        """return all ancestors includind self as 1st item"""
        channel_list = self.get_ancestors_slugs()
        ancestors = self.__class__.objects(
            long_slug__in=channel_list,
            **kwargs
        ).order_by('-long_slug')
        return ancestors

    def get_children(self, **kwargs):
        """return direct children 1 level depth"""
        return self.__class__.objects(
            parent=self, **kwargs
        ).order_by('long_slug')

    def get_descendants(self, **kwargs):
        """return all descendants including self as 1st item"""
        return self.__class__.objects(
            __raw__={'mpath': {'$regex': '^{0}'.format(self.mpath)}}
        ).order_by('long_slug')

    def get_themes(self):
        return list({
            c.channel_type.theme_name
            for c in self.get_ancestors(channel_type__ne=None)
            if c.channel_type and c.channel_type.theme_name
        })

    @classmethod
    def get_homepage(cls, attr=None):
        try:
            homepage = cls.objects.get(is_homepage=True)
        except Exception as e:
            logger.info("There is no homepage: %s", e.message)
            return None
        else:
            if not attr:
                return homepage
            else:
                return getattr(homepage, attr, homepage)

    def __unicode__(self):
        return self.long_slug

    def get_absolute_url(self, *args, **kwargs):
        if self.is_homepage:
            return "/"
        return "/{0}/".format(self.long_slug)

    def get_canonical_url(self, *args, **kwargs):
        """
        This method should be reviewed
        Canonical URL is the preferred URL for a content
        when the content can be served by multiple URLS
        In the case of channels it will never happen
        until we implement the channel alias feature
        """
        if self.is_homepage:
            return "/"
        return self.get_absolute_url()

    def get_http_url(self):
        site_url = Config.get('site', 'site_domain', request.url_root)
        return u"{}{}".format(site_url, self.get_absolute_url())

    def clean(self):
        homepage = Channel.objects(is_homepage=True)
        if self.is_homepage and homepage and self not in homepage:
            raise db.ValidationError(_l("Home page already exists"))
        super(Channel, self).clean()

    def validate_render_content(self):
        if self.render_content and \
                not isinstance(self.render_content, ContentProxy):
            self.render_content, created = ContentProxy.objects.get_or_create(
                content=self.render_content)
        else:
            self.render_content = None

    def heritage(self):
        """populate inheritance from parent channels"""
        parent = self.parent
        if not parent or not self.inherit_parent:
            return

        self.content_filters = self.content_filters or parent.content_filters
        self.include_in_rss = self.include_in_rss or parent.include_in_rss
        self.show_in_menu = self.show_in_menu or parent.show_in_menu
        self.indexable = self.indexable or parent.indexable
        self.channel_type = self.channel_type or parent.channel_type

    def update_descendants_and_contents(self):
        """
        Need to Detect if self.long_slug and self.mpath has changed.
        if so, update every descendant using get_descendatns method
        to query.
        Also update long_slug and mpath for every Content in this channel
        This needs to be done by default in araw immediate way, but if
        current_app.config.get('ASYNC_SAVE_MODE') is True it will delegate
        all those tasks to celery."""

    def save(self, *args, **kwargs):
        self.validate_render_content()
        self.validate_slug()
        self.validate_long_slug()
        self.heritage()
        self.update_descendants_and_contents()
        if not self.channel_type:
            self.channel_type = ChannelType.objects.first()
        super(Channel, self).save(*args, **kwargs)


class Channeling(object):
    channel = db.ReferenceField(Channel, required=True,
                                reverse_delete_rule=db.DENY)
    related_channels = db.ListField(
        db.ReferenceField('Channel', reverse_delete_rule=db.PULL)
    )
    related_mpath = db.ListField(db.StringField())
    show_on_channel = db.BooleanField(default=True)
    channel_roles = db.ListField(db.StringField())

    def populate_related_mpath(self):
        self.related_mpath = [rel.mpath for rel in self.related_channels]

    def populate_channel_roles(self):
        self.channel_roles = [role.name for role in self.channel.roles]


class ChannelingNotRequired(Channeling):
    channel = db.ReferenceField(Channel, required=False,
                                reverse_delete_rule=db.NULLIFY)


class Config(HasCustomValue, ContentFormat, Publishable, db.DynamicDocument):
    group = db.StringField(max_length=255)
    description = db.StringField()

    @classmethod
    def get(cls, group, name=None, default=None):

        try:
            instance = cls.objects.get(group=group)
        except:
            return None

        if not name:
            ret = instance.values
            if group == 'settings':
                ret = {}
                ret.update(current_app.config)
                ret.update({item.name: item.value for item in instance.values})
        else:
            try:
                ret = instance.values.get(name=name).value
            except (MultipleObjectsReturned, AttributeError):
                ret = None

        if not ret and group == 'settings' and name is not None:
            # get direct from store to avoid infinite loop
            ret = current_app.config.store.get(name)

        return ret or default

    def __unicode__(self):
        return self.group


class Quokka(Dated, Slugged, db.DynamicDocument):
    """ Hidden collection """


class ContentTemplateType(TemplateType, db.Document):
    """Define the content template type and its theme"""


class SubContentPurpose(db.Document):
    title = db.StringField(max_length=255, required=True)
    identifier = db.StringField(max_length=255, required=True, unique=True)
    module = db.StringField()

    def save(self, *args, **kwargs):
        self.identifier = slugify(self.identifier or self.title)
        super(SubContentPurpose, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class SubContent(Publishable, Ordered, db.EmbeddedDocument):
    """Content can have inner contents
    Its useful for any kind of relation with Content childs
    Images, ImageGalleries, RelatedContent, Attachments, Media
    """

    content = db.ReferenceField('Content', required=True)
    caption = db.StringField()
    purpose = db.ReferenceField(SubContentPurpose, required=True)
    identifier = db.StringField()

    @property
    def thumb(self):
        try:
            return url_for('media', filename=self.content.thumb)
            # return self.content.thumb
        except Exception as e:
            logger.warning(str(e))
            return self.content.get_main_image_url(thumb=True)

    meta = {
        'ordering': ['order'],
        'indexes': ['order']
    }

    def clean(self):
        self.identifier = self.purpose.identifier

    def __unicode__(self):
        return self.content and self.content.title or self.caption


class License(db.EmbeddedDocument):
    LICENSES = (('custom', 'custom'),
                ('creative_commons_by_nc_nd', 'creative_commons_by_nc_nd'))
    title = db.StringField(max_length=255)
    link = db.StringField(max_length=255)
    identifier = db.StringField(max_length=255, choices=LICENSES)


class ShortenedURL(db.EmbeddedDocument):
    original = db.StringField(max_length=255)
    short = db.StringField(max_length=255)

    def __str__(self):
        return self.short


###############################################################
# Base Content for every new content to extend. inheritance=True
###############################################################


class Content(HasCustomValue, Publishable, LongSlugged,
              Channeling, Tagged, ContentFormat, db.DynamicDocument):
    title = db.StringField(max_length=255, required=True)
    summary = db.StringField(required=False)
    template_type = db.ReferenceField(ContentTemplateType,
                                      required=False,
                                      reverse_delete_rule=db.NULLIFY)
    contents = db.ListField(db.EmbeddedDocumentField(SubContent))
    model = db.StringField()
    comments_enabled = db.BooleanField(default=True)
    license = db.EmbeddedDocumentField(License)
    shortened_url = db.EmbeddedDocumentField(ShortenedURL)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at'],
    }

    @classmethod
    def available_objects(cls, **filters):
        now = datetime.datetime.now()
        default_filters = {
            "published": True,
            'available_at__lte': now,
        }
        default_filters.update(filters)
        return cls.objects(**default_filters)

    def get_main_image_url(self, thumb=False,
                           default=None, identifier='mainimage'):
        """
        """
        if not isinstance(identifier, (list, tuple)):
            identifier = [identifier]

        for item in identifier:
            try:
                if not thumb:
                    path = self.contents.get(identifier=item).content.path
                else:
                    path = self.contents.get(identifier=item).content.thumb
                return url_for('media', filename=path)
            except Exception as e:
                logger.warning('get_main_image_url:' + str(e))

        return default

    def get_uid(self):
        return str(self.id)

    def get_themes(self):
        themes = self.channel.get_themes()
        theme = self.template_type and self.template_type.theme_name
        if theme:
            themes.insert(0, theme)
        return list(set(themes))

    def get_http_url(self):
        site_url = get_site_url()
        absolute_url = self.get_absolute_url()
        absolute_url = absolute_url[1:]
        return u"{}{}".format(site_url, absolute_url)

    def get_absolute_url(self, endpoint='detail'):
        if self.channel.is_homepage:
            long_slug = self.slug
        else:
            long_slug = self.long_slug

        try:
            return url_for(self.URL_NAMESPACE, long_slug=long_slug)
        except:
            return url_for(endpoint, long_slug=long_slug)

    def get_canonical_url(self, *args, **kwargs):
        return self.get_absolute_url()

    def get_recommendations(self, limit=3, ordering='-created_at', *a, **k):
        now = datetime.datetime.now()
        filters = {
            'published': True,
            'available_at__lte': now,
            "id__ne": self.id
        }
        contents = Content.objects(**filters).filter(tags__in=self.tags or [])

        return contents.order_by(ordering)[:limit]

    def get_summary(self):
        if self.summary:
            return self.summary
        return self.get_text()

    def get_text(self):
        if hasattr(self, 'body'):
            text = self.body
        elif hasattr(self, 'description'):
            text = self.description
        else:
            text = self.summary or ""

        if self.content_format == "markdown":
            return markdown(text)
        else:
            return text

    def __unicode__(self):
        return self.title

    @property
    def short_url(self):
        return self.shortened_url.short if self.shortened_url else ''

    @property
    def model_name(self):
        return self.__class__.__name__.lower()

    @property
    def module_name(self):
        module = self.__module__
        module_name = module.replace('quokka.modules.', '').split('.')[0]
        return module_name

    def heritage(self):
        self.model = "{0}.{1}".format(self.module_name, self.model_name)

    def save(self, *args, **kwargs):
        # all those functions should be in a dynamic pipeline
        self.validate_slug()
        self.validate_long_slug()
        self.heritage()
        self.populate_related_mpath()
        self.populate_channel_roles()
        self.populate_shorter_url()
        super(Content, self).save(*args, **kwargs)

    def pre_render(self, render_function, *args, **kwargs):
        return render_function(*args, **kwargs)

    def populate_shorter_url(self):
        if not self.published or not get_setting_value('SHORTENER_ENABLED'):
            return

        url = self.get_http_url()
        if not self.shortened_url or url != self.shortened_url.original:
            shortener = ShorterURL()
            self.shortened_url = ShortenedURL(original=url,
                                              short=shortener.short(url))


class Link(Content):
    link = db.StringField(required=True)
    force_redirect = db.BooleanField(default=True)
    increment_visits = db.BooleanField(default=True)
    visits = db.IntField(default=0)
    show_on_channel = db.BooleanField(default=False)

    def pre_render(self, render_function, *args, **kwargs):
        if self.increment_visits:
            self.visits = self.visits + 1
            self.save()
        if self.force_redirect:
            return redirect(self.link)
        return super(Link, self).pre_render(render_function, *args, **kwargs)
