# coding: utf-8

import logging
import collections
from datetime import datetime
from flask import request, redirect, url_for
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from quokka.core.models import Channel, Content, Comment
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

        channel = Channel.objects.get_or_404(mpath=mpath)

        if channel.render_content:
            return ContentDetail().get(
                channel.render_content.content.long_slug, True)

        self.channel = channel

        filters = {
            'published': True,
            'available_at__lte': now,
            'show_on_channel': True
        }

        if not channel.is_homepage:
            filters['__raw__'] = {'mpath': {'$regex': "^{0}".format(mpath)}}

        filters.update(channel.get_content_filters())
        contents = Content.objects(**filters)

        themes = channel.get_themes()
        return render_template(self.get_template_names(),
                               theme=themes, contents=contents)


class ContentDetail(MethodView):
    object_name = "content"
    template_suffix = "detail"
    template_ext = "html"

    form = model_form(
        Comment,
        exclude=['created_at', 'created_by', 'published']
    )

    def get_template_names(self):

        if self.content.template_type:
            type_suffix = self.content.template_type.template_suffix
        else:
            type_suffix = 'default'

        self.template_suffix = "{0}_{1}".format(type_suffix,
                                                self.template_suffix)

        module = self.content.__module__
        module_name = module.replace('quokka.modules.', '').split('.')[0]
        model_name = self.content.content_type.lower()

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

        form = self.form(request.form)

        self.content = content

        context = {
            "content": content,
            "form": form
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

    def post(self, long_slug):
        context = self.get_context(long_slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            content = context.get('content')
            content.comments.append(comment)
            content.save()

            return redirect(url_for('.detail', long_slug=long_slug))

        return render_template(
            self.get_template_names(),
            theme=self.content.get_themes(),
            **context
        )


class ContentFeed(MethodView):
    pass


class ChannelFeed(ContentFeed):
    pass
