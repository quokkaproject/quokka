
from wtforms.widgets import TextArea


class BigTextArea(TextArea):
    def __init__(self, *args, **kwargs):
        super(BigTextArea, self).__init__()
        self.rows = kwargs.get('rows')
        self.cols = kwargs.get('cols')
        self.css_cls = kwargs.get('css_cls')
        self.style_ = kwargs.get('style_')

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (self.css_cls, c)
        kwargs['rows'] = self.rows
        kwargs['cols'] = self.cols
        kwargs['style'] = self.style_
        return super(BigTextArea, self).__call__(field, **kwargs)
