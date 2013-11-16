# coding: utf-8

import logging
import collections
from urlparse import urljoin
from datetime import datetime
from flask import request, redirect, url_for, abort, current_app
from flask.views import MethodView
from werkzeug.contrib.atom import AtomFeed
from quokka.core.models import Channel, Content, Config
from quokka.core.templates import render_template

logger = logging.getLogger()


class ContentList(MethodView):
    object_name = "content"
    template_suffix = "list"
    template_ext = "html"

    def get_template_names(self):

        if self.channel.channel_type:
            type_suffix = self.channel.channel_type.template_suffix
        else:
            type_suffix = 'default'

        self.template_suffix = "{0}_{1}".format(type_suffix,
                                                self.template_suffix)

        common_data = dict(
            object_name=self.object_name,
            suffix=self.template_suffix,
            ext=self.template_ext
        )

        channel_list = self.channel.get_ancestors_slugs()
        names = [
            u"{object_name}/{channel}/{suffix}.{ext}".format(
                channel=channel, **common_data
            )
            for channel in channel_list
        ]

        names.append(u"{object_name}/{suffix}.{ext}".format(**common_data))
        return names

    def get(self, long_slug):
        now = datetime.now()
        path = long_slug.split('/')
        mpath = ",".join(path)
        mpath = ",{0},".format(mpath)

        channel = Channel.objects.get_or_404(mpath=mpath, published=True)

        # if channel.is_homepage and request.path != "/":
        #     return redirect("/")

        if channel.redirect_url:
            return redirect(channel.redirect_url)

        if channel.render_content:
            return ContentDetail().get(
                channel.render_content.content.long_slug, True)

        self.channel = channel

        base_filters = {}

        filters = {
            'published': True,
            'available_at__lte': now,
            'show_on_channel': True
        }

        if not channel.is_homepage:
            base_filters['__raw__'] = {
                'mpath': {'$regex': "^{0}".format(mpath)}}

        filters.update(channel.get_content_filters())
        contents = Content.objects(**base_filters).filter(**filters)

        if current_app.config.get("PAGINATION_ENABLED", True):
            pagination_arg = current_app.config.get("PAGINATION_ARG", "page")
            page = request.args.get(pagination_arg, 1)
            per_page = channel.per_page or current_app.config.get(
                "PAGINATION_PER_PAGE", 10
            )
            contents = contents.paginate(page=int(page), per_page=per_page)

        # this can be overkill! try another solution
        # to filter out content in unpublished channels
        # when homepage and also in blocks
        # contents = [content for content in contents
        #             if content.channel.published]

        themes = channel.get_themes()
        return render_template(self.get_template_names(),
                               theme=themes,
                               contents=contents,
                               channel=channel)


class ContentDetail(MethodView):
    object_name = "content"
    template_suffix = "detail"
    template_ext = "html"

    def get_template_names(self):

        if self.content.template_type:
            type_suffix = self.content.template_type.template_suffix
        else:
            type_suffix = 'default'

        self.template_suffix = "{0}_{1}".format(type_suffix,
                                                self.template_suffix)

        module_name = self.content.module_name
        model_name = self.content.model_name

        common_data = dict(
            object_name=self.object_name,
            module_name=module_name,
            model_name=model_name,
            suffix=self.template_suffix,
            ext=self.template_ext
        )

        names = [
            u"{object_name}/{content_slug}.{ext}".format(
                content_slug=self.content.long_slug, **common_data),
            u"{object_name}/{content_slug}_{suffix}.{ext}".format(
                content_slug=self.content.long_slug, **common_data),
            u"{object_name}/{content_slug}.{ext}".format(
                content_slug=self.content.slug, **common_data),
            u"{object_name}/{content_slug}_{suffix}.{ext}".format(
                content_slug=self.content.slug, **common_data)
        ]

        channel_list = self.content.channel.get_ancestors_slugs()
        for channel in channel_list:
            path = ("{object_name}/_{module_name}/{channel}/"
                    "{model_name}_{suffix}.{ext}")
            names.append(path.format(channel=channel, **common_data))

        for channel in channel_list:
            path = "{object_name}/_{module_name}/{channel}/{suffix}.{ext}"
            names.append(path.format(channel=channel, **common_data))

        names.append(
            "{object_name}/_{module_name}/{model_name}_{suffix}.{ext}".format(
                **common_data
            )
        )

        names.append(
            "{object_name}/_{module_name}/{suffix}.{ext}".format(**common_data)
        )

        for channel in channel_list:
            path = "{object_name}/{channel}/{model_name}_{suffix}.{ext}"
            names.append(path.format(channel=channel, **common_data))

        for channel in channel_list:
            path = "{object_name}/{channel}/{suffix}.{ext}"
            names.append(path.format(channel=channel, **common_data))

        names.append(
            "{object_name}/{model_name}_{suffix}.{ext}".format(**common_data)
        )

        names.append("{object_name}/{suffix}.{ext}".format(**common_data))

        return names

    def get_context(self, long_slug, render_content=False):
        now = datetime.now()
        homepage = Channel.objects.get(is_homepage=True)

        if long_slug.startswith(homepage.slug) and \
                len(long_slug.split('/')) < 3 and \
                not render_content:
            slug = long_slug.split('/')[-1]
            return redirect(url_for('detail', long_slug=slug))

        filters = {
            'published': True,
            'available_at__lte': now
        }

        try:
            content = Content.objects.get(
                long_slug=long_slug,
                **filters
            )
        except Content.DoesNotExist:
            content = Content.objects.get_or_404(
                channel=homepage,
                slug=long_slug,
                **filters
            )

        if not content.channel.published:
            return abort(404)

        self.content = content

        context = {
            "content": content,
            "channel": content.channel
        }

        return context

    def get(self, long_slug, render_content=False):
        context = self.get_context(long_slug, render_content)
        if not render_content and isinstance(context, collections.Callable):
            return context
        return render_template(
            self.get_template_names(),
            theme=self.content.get_themes(),
            **context
        )


class BaseTagView(MethodView):
    def get_contents(self, tag):
        now = datetime.now()
        filters = {
            'published': True,
            'available_at__lte': now
        }
        contents = Content.objects(**filters).filter(tags=tag)

        if current_app.config.get("PAGINATION_ENABLED", True):
            pagination_arg = current_app.config.get("PAGINATION_ARG", "page")
            page = request.args.get(pagination_arg, 1)
            per_page = current_app.config.get(
                "PAGINATION_PER_PAGE", 10
            )
            contents = contents.paginate(page=int(page), per_page=per_page)

        return contents


class TagList(BaseTagView):
    object_name = "content"
    template_suffix = "list"
    template_ext = "html"

    def get_template_names(self):
        self.template_suffix = "{0}_{1}".format('tag',
                                                self.template_suffix)

        names = [
            u"{0}/{1}.{2}".format(
                self.object_name, self.template_suffix, self.template_ext
            )
        ]

        return names

    def get(self, tag):
        contents = self.get_contents(tag)
        return render_template(self.get_template_names(),
                               contents=contents)


class BaseFeed(MethodView):

    def make_external_url(self, url):
        return urljoin(request.url_root, url)

    def make_atom(self, feed_name, contents):
        feed = AtomFeed(
            feed_name,
            feed_url=request.url,
            url=request.url_root
        )
        for content in contents:
            if not content.channel.include_in_rss:
                continue

            if content.created_by:
                author = content.created_by.name
            else:
                author = Config.get('site', 'site_author', '')

            feed.add(
                content.title,
                content.get_text(),
                content_type="html",
                author=author,
                url=self.make_external_url(content.get_absolute_url()),
                updated=content.updated_at,
                published=content.created_at
            )
        return feed

    def make_rss(self):
        """TODO: Issue # 70 """


class ContentFeed(BaseFeed):

    def get_contents(self, long_slug):
        now = datetime.now()
        path = long_slug.split('/')
        mpath = ",".join(path)
        mpath = ",{0},".format(mpath)

        channel = Channel.objects.get_or_404(mpath=mpath, published=True)
        if not channel.include_in_rss:
            abort(404)

        self.channel = channel

        base_filters = {}

        filters = {
            'published': True,
            'available_at__lte': now,
        }

        if not channel.is_homepage:
            base_filters['__raw__'] = {
                'mpath': {'$regex': "^{0}".format(mpath)}}

        filters.update(channel.get_content_filters())
        contents = Content.objects(**base_filters).filter(**filters)

        if current_app.config.get("PAGINATION_ENABLED", True):
            pagination_arg = current_app.config.get("PAGINATION_ARG", "page")
            page = request.args.get(pagination_arg, 1)
            per_page = channel.per_page or current_app.config.get(
                "PAGINATION_PER_PAGE", 10
            )
            contents = contents.paginate(page=int(page), per_page=per_page)

        return contents


class FeedAtom(ContentFeed):

    def get(self, long_slug):
        contents = self.get_contents(long_slug)
        if current_app.config.get("PAGINATION_ENABLED", True):
            contents = contents.items

        feed_name = u"{0} | {1} | feed".format(
            Config.get('site', 'site_name', ''),
            self.channel.title
        )
        feed = self.make_atom(feed_name, contents)

        return feed.get_response()


class TagAtom(BaseFeed, BaseTagView):
    def get(self, tag):
        contents = self.get_contents(tag)
        if current_app.config.get("PAGINATION_ENABLED", True):
            contents = contents.items

        feed_name = u"{0} | {1} | feed".format(
            Config.get('site', 'site_name', ''),
            "Tag {0}".format(tag)
        )
        feed = self.make_atom(feed_name, contents)

        return feed.get_response()
