import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight-wrapper">%s</div>\n' % code
        return code
    except BaseException:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )


class HighlightMixin(object):
    def block_code(self, text, lang):
        # renderer has an options
        inlinestyles = self.options.get('inlinestyles', False)
        linenos = self.options.get('linenos', False)
        return block_code(text, lang, inlinestyles, linenos)


class HighlightRenderer(HighlightMixin, mistune.Renderer):
    pass
    # def block_code(self, code, lang):
    #     if not lang:
    #         return '\n<pre><code>%s</code></pre>\n' % \
    #             mistune.escape(code)
    #     lexer = get_lexer_by_name(lang, stripall=True)
    #     formatter = html.HtmlFormatter()
    #     return highlight(code, lexer, formatter)


renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)
