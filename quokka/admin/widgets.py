
from flask import current_app
from quokka.core.template import render_template
from wtforms.widgets import TextArea, TextInput


class TextEditor(TextArea):
    def __init__(self, *args, **kwargs):
        super(TextEditor, self).__init__()
        self.rows = kwargs.get('rows', 20)
        self.cols = kwargs.get('cols', 20)
        self.css_cls = kwargs.get('css_cls', 'text_editor')
        self.style_ = kwargs.get(
            'style_',
            "margin: 0px; width: 725px; height: 360px;"
        )
        self.editor = kwargs.pop('editor', 'texteditor')

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (self.css_cls, c)
        kwargs['rows'] = self.rows
        kwargs['cols'] = self.cols
        s = kwargs.pop('style', '') or kwargs.pop('style_', '')
        kwargs['style'] = u"%s %s" % (self.style_, s)
        html = super(TextEditor, self).__call__(field, **kwargs)
        html += render_template(
            'admin/texteditor/%s.html' % self.editor,
            theme=current_app.config.get('ADMIN_THEME', 'admin'),
            selector='.' + self.css_cls
        )
        return html


class PrepopulatedText(TextInput):
    def __init__(self, *args, **kwargs):
        self.master = kwargs.pop('master', '')
        super(PrepopulatedText, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        html = super(PrepopulatedText, self).__call__(*args, **kwargs)
        slave = args[0].id
        if self.master:
            html += render_template(
                'admin/custom/prepopulated.html',
                theme=current_app.config.get('ADMIN_THEME', 'admin'),
                master=self.master,
                slave=slave
            )
        return html
