# coding: utf-8
import sys

from . import BaseTestCase

from ..models import Channel, Config
from ..base_models.custom_values import CustomValue

if sys.version_info.major == 3:
    unicode = lambda x: u'{}'.format(x)  # flake8: noqa  # noqa


class TestChannel(BaseTestCase):
    def setUp(self):
        # Create method was not returning the created object with
        # the create() method
        self.parent, new = Channel.objects.get_or_create(
            title=u'Father',
        )
        self.channel, new = Channel.objects.get_or_create(
            title=u'Monkey Island',
            description=u'The coolest pirate history ever',
            parent=self.parent,
            tags=['tag1', 'tag2'],
        )

    def tearDown(self):
        self.channel.delete()
        self.parent.delete()

    def test_channel_fields(self):
        self.assertEqual(self.channel.title, u'Monkey Island')
        self.assertEqual(self.channel.slug, u'monkey-island')
        self.assertEqual(self.channel.long_slug, u'father/monkey-island')
        self.assertEqual(self.channel.mpath, u',father,monkey-island,')
        self.assertEqual(self.channel.description,
                         u'The coolest pirate history ever')
        self.assertEqual(self.channel.tags, ['tag1', 'tag2'])
        self.assertEqual(self.channel.parent, self.parent)
        self.assertEqual(unicode(self.channel), u'father/monkey-island')

    def test_get_ancestors(self):
        self.assertEqual(list(self.channel.get_ancestors()), [self.channel,
                                                              self.parent])

    def test_get_ancestors_slug(self):
        self.assertEqual(self.channel.get_ancestors_slugs(),
                         [u'father/monkey-island', u'father'])

    def test_get_children(self):
        self.assertEqual(list(self.parent.get_children()), [self.channel])

    def test_get_descendants(self):
        self.assertEqual(list(self.parent.get_descendants()),
                         [self.parent, self.channel])

    def test_absolute_urls(self):
        self.assertEqual(self.channel.get_absolute_url(),
                         '/father/monkey-island/')
        self.assertEqual(self.parent.get_absolute_url(),
                         '/father/')

    def test_get_canonical_url(self):
        self.assertEqual(self.channel.get_canonical_url(),
                         '/father/monkey-island/')
        self.assertEqual(self.parent.get_canonical_url(),
                         '/father/')


class TestConfig(BaseTestCase):
    def setUp(self):
        # Create method was not returning the created object with
        # the create() method
        self.config, new = Config.objects.get_or_create(
            group='test',
        )
        self.config.values.append(CustomValue(name='test_config',
                                              rawvalue=u'a nice config',
                                              formatter='text'))

    def tearDown(self):
        self.config.delete()

    def test_config_fields(self):
        self.assertEqual(self.config.group, u'test')
        self.assertEqual(self.config.content_format, 'html')
        self.assertFalse(self.config.published)
        self.assertTrue(self.config.values.count(), 1)
        self.assertEqual(unicode(self.config), u'test')
        self.assertEqual(self.config.values[0].value, u'a nice config')
