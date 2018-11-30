import pytest
import mock
import click
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from quokka.core.content.parsers import (
    block_code,
    HighlightMixin,
    HighlightRenderer
)


#######################################################
#pytest - fixtures                                    #
#######################################################
block = block_code(text="java-debugger-code", lang="pt")

#######################################################
#pytest - Quokka - tests/core/content/test_parsers.py #
#######################################################
def test_block_code():
    assert block == '<pre class="pt"><code>java-debugger-code</code></pre>\n'

def test_class_highlightmixin():
    with pytest.raises(AttributeError) as err:
        high = HighlightMixin()
        block = high.block_code(text="java-debugger-code", lang="pt")
        assert "HighlightMixin object has no attribute options" in str(err.value)

