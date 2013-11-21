# coding: utf-8
from . import BaseTestCase

from ..models import Channel


class TestCoreModels(BaseTestCase):
    def setUp(self):
        # Create method was not returning the created object with
        # the create() method
        self.channel, new = Channel.objects.get_or_create(
            title=u'Monkey Island',
            description=u'The coolest pirate history ever',
        )

    def tearDown(self):
        self.channel.delete()

    def test_channel_fields(self):
        self.assertEqual(self.channel.title, u'Monkey Island')
        self.assertEqual(self.channel.slug, u'monkey-island')
        self.assertEqual(self.channel.description,
                         u'The coolest pirate history ever')
