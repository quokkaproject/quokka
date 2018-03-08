from flask import current_app as app
from flask_htmlbuilder.htmlbuilder import html
from quokka.core.content.models import make_model


def format_datetime(self, request, obj, fieldname, *args, **kwargs):
    """Returns the formated datetime in string from object"""
    model = make_model(obj)
    return html.div(style='min-width:130px;')(
        getattr(model, fieldname).strftime(
            app.config.get('ADMIN_DATE_FORMAT', '%Y-%m-%d')
        )
    )


def format_view_on_site(self, request, obj, fieldname, *args, **kwargs):
    """Returns button to view or preview depending on content status"""
    model = make_model(obj)
    return html.a(
        href=model.external_url,
        target='_blank',
    )(html.i(class_="icon fa fa-globe glyphicon glyphicon-globe",
             style="margin-right: 5px;")(),
      'View' if model.published else 'Preview')


def format_ul(self, request, obj, fieldname, *args, **kwars):
    """Given a list of data format it is ul/li"""
    model = make_model(obj)
    field = getattr(model, fieldname)
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('ul', {}).get(fieldname, {})
    ul = html.ul(style=_args.get('style', "min-width:200px;max-width:300px;"))
    placeholder = _args.get('placeholder', u"{i}")
    lis = [html.li(placeholder.format(item=item)) for item in field]
    return ul(*lis)


def format_link(self, request, obj, fieldname, *args, **kwars):
    """Format a link from the model"""
    model = make_model(obj)
    value = getattr(model, fieldname)
    return html.a(href=value, title=value, target='_blank')(
        html.i(class_="icon  icon-resize-small",
               style="margin-right: 5px;")()
    )


def format_status(self, request, obj, fieldname, *args, **kwargs):
    """Format the status published or not published and other booleans"""
    model = make_model(obj)
    status = getattr(model, fieldname)
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('status', {}).get(fieldname, {})
    labels = _args.get('labels', {})
    return html.span(
        class_="label label-{0}".format(labels.get(status, 'default')),
        style=_args.get('style', 'min-height:18px;')
    )(status)


def format_url(self, request, obj, fieldname, *args, **kwargs):
    """Get the url of a content object"""
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('get_url', {}).get(fieldname, {})
    attribute = _args.get('attribute', 'url')
    method = _args.get('method', 'url')
    model = make_model(obj)
    text = getattr(model, fieldname, '')
    if attribute:
        target = getattr(model, attribute, None)
    else:
        target = model

    url = getattr(target, method, lambda: '#')()

    return html.a(href=url)(text if text not in [None, 'None'] else '')
