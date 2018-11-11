import pytest
from quokka.utils.blocks import (
    get_block, 
    get_blocks, 
    get_block_by_id
)
from quokka.core.template_filters import (
    is_list, configure
)
from quokka import create_app


#######################################################
#pytest - fixtures                                    #
#######################################################
app = create_app(test=True)


#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_configure():
    assert configure(app) is None

