
from flask_htmlbuilder.htmlbuilder import html
from quokka.admin.utils import _l


def format_datetime(self, request, obj, fieldname, *args, **kwargs):
    return html.div(style='min-width:130px;')(
        getattr(obj, fieldname).strftime(self.get_datetime_format())
    )


def view_on_site(self, request, obj, fieldname, *args, **kwargs):
    available = obj.is_available
    endpoint = kwargs.pop(
        'endpoint',
        'quokka.core.detail' if available else 'quokka.core.preview'
    )
    return html.a(
        href=obj.get_absolute_url(endpoint),
        target='_blank',
    )(html.i(class_="icon icon-eye-open", style="margin-right: 5px;")(),
      _l('View on site') if available else _l('Preview on site'))


def format_ul(self, request, obj, fieldname, *args, **kwars):
    field = getattr(obj, fieldname)
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('ul', {}).get(fieldname, {})
    ul = html.ul(style=_args.get('style', "min-width:200px;max-width:300px;"))
    placeholder = _args.get('placeholder', u"{i}")
    lis = [html.li(placeholder.format(item=item)) for item in field]
    return ul(*lis)


def format_link(self, request, obj, fieldname, *args, **kwars):
    value = getattr(obj, fieldname)
    return html.a(href=value, title=value, target='_blank')(
        html.i(class_="icon  icon-resize-small",
               style="margin-right: 5px;")()
    )


def format_status(self, request, obj, fieldname, *args, **kwargs):
    status = getattr(obj, fieldname)
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('status', {}).get(fieldname, {})
    labels = _args.get('labels', {})
    return html.span(
        class_="label label-{0}".format(labels.get(status, 'default')),
        style=_args.get('style', 'min-height:18px;')
    )(status)


def get_url(self, request, obj, fieldname, *args, **kwargs):
    column_formatters_args = getattr(self, 'column_formatters_args', {})
    _args = column_formatters_args.get('get_url', {}).get(fieldname, {})
    attribute = _args.get('attribute')
    method = _args.get('method', 'get_absolute_url')
    text = getattr(obj, fieldname, '')
    if attribute:
        target = getattr(obj, attribute, None)
    else:
        target = obj

    url = getattr(target, method, lambda: '#')()

    return html.a(href=url)(text if text not in [None, 'None'] else '')
