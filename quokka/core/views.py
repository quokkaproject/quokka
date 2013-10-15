# coding: utf-8

import logging
import collections
from datetime import datetime
from flask import request, redirect, url_for  # render_template
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from quokka.core.models import Channel, Content, Comment
from quokka.core.templates import render_template

logger = logging.getLogger()


class ContentList(MethodView):

    def get_template_names(self):
        names = []
        names.append('content/list.html')
        return names

    def get(self, long_slug):
        now = datetime.now()
        path = long_slug.split('/')
        mpath = ",".join(path)
        mpath = ",{0},".format(mpath)

        channel = Channel.objects.get_or_404(mpath=mpath)

        filters = {
            'published': True,
            'available_at__lte': now,
            'show_on_channel': True
        }

        if not channel.is_homepage:
            filters['__raw__'] = {'mpath': {'$regex': mpath}}

        contents = Content.objects(**filters)

        return render_template(self.get_template_names(), contents=contents)


class ContentDetail(MethodView):
    object_name = "content"
    template_suffix = "detail"
    template_ext = "html"

    form = model_form(
        Comment,
        exclude=['created_at', 'created_by', 'published']
    )

    def get_template_names(self):
        module = self.content.__module__
        module_name = module.replace('quokka.modules.', '').split('.')[0]
        model_name = self.content.__class__.__name__.lower()

        common_data = dict(
            object_name=self.object_name,
            module_name=module_name,
            model_name=model_name,
            suffix=self.template_suffix,
            ext=self.template_ext
        )

        # start with the most specific templates
        # using content slug and long slug
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

        # define per module/channel templates
        channel_list = []
        channel_slugs = self.content.channel.long_slug.split('/')
        while channel_slugs:
            channel_list.append("/".join(channel_slugs))
            channel_slugs.pop()

        for channel in channel_list:
            path = ("{object_name}/{module_name}/{channel}/"
                    "{model_name}_{suffix}.{ext}")
            names.append(path.format(channel=channel, **common_data))

        for channel in channel_list:
            path = "{object_name}/{module_name}/{channel}/{suffix}.{ext}"
            names.append(path.format(channel=channel, **common_data))

        # per module/model
        names.append(
            "{object_name}/{module_name}/{model_name}_{suffix}.{ext}".format(
                **common_data
            )
        )

        # module general detail
        names.append(
            "{object_name}/{module_name}/{suffix}.{ext}".format(
                **common_data
            )
        )

        # per channel/model templates
        for channel in channel_list:
            path = "{object_name}/{channel}/{model_name}_{suffix}.{ext}"
            names.append(path.format(channel=channel, **common_data))

        for channel in channel_list:
            path = "{object_name}/{channel}/{suffix}.{ext}"
            names.append(path.format(channel=channel, **common_data))

        # model_detail
        names.append(
            "{object_name}/{model_name}_{suffix}.{ext}".format(
                **common_data
            )
        )

        # last one is the default detail template
        names.append(
            "{object_name}/{suffix}.{ext}".format(
                **common_data
            )
        )

        return names

    def get_context(self, long_slug):
        now = datetime.now()
        homepage = Channel.objects.get(is_homepage=True)

        if long_slug.startswith(homepage.slug) and \
                len(long_slug.split('/')) < 3:
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

        self.content = content  # template loader will use this

        context = {
            "content": content,
            "form": form
        }

        return context

    def get(self, long_slug):
        context = self.get_context(long_slug)
        if isinstance(context, collections.Callable):
            return context
        return render_template(self.get_template_names(), **context)

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

        return render_template(self.get_template_names(), **context)


class ContentFeed(MethodView):
    pass


class ChannelFeed(ContentFeed):
    pass
