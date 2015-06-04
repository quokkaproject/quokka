# coding: utf-8
import sys

from quokka.core.tests import BaseTestCase
from quokka.core.models import Channel

from ..models import Post

if sys.version_info.major == 3:
    unicode = str


class TestPost(BaseTestCase):
    def setUp(self):
        self.channel, new = Channel.objects.get_or_create(title="test channel")
        self.post_dict = {
            "title": "Python Reaches New Levels of Quality",
            "slug": "python-reaches-new-level-of-quality",
            "summary": "Python Surpasses Standards, Reaches New Levels",
            "body": u"testing a nice body",
            "channel": self.channel,
            "tags": ["tag1", "tag2", "tag3"],
            "published": True,
        }
        self.post_dict2 = {
            "title": "This is a nice post",
            "slug": "this-is-a-nice-post",
            "summary": "Another nice post",
            "content_format": "markdown",
            "body": u"## testing a nice body",
            "channel": self.channel,
            "tags": ["tag", "tag3"],
            "published": True
        }
        self.post, new = Post.objects.get_or_create(**self.post_dict)
        self.post2, new = Post.objects.get_or_create(**self.post_dict2)

    def tearDown(self):
        self.post.delete()
        self.post2.delete()
        self.channel.delete()

    def test_post_fields(self):
        self.assertEqual(self.post.title, self.post_dict.get('title'))
        self.assertEqual(self.post.slug, self.post_dict.get('slug'))
        self.assertEqual(self.post.body, self.post_dict.get('body'))
        self.assertEqual(self.post.content_format, 'html')
        self.assertEqual(self.post.tags.count(), 3)
        self.assertEqual(list(self.post.tags), self.post_dict.get('tags'))
        self.assertEqual(self.post.channel, self.channel)

    def test_model_name(self):
        self.assertEqual(self.post.model_name, 'post')

    def test_module_name(self):
        self.assertEqual(self.post.module_name, 'posts')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(),
                         '/test-channel/python-reaches-new-level-of-quality'
                         '.html')

    def test_get_uid(self):
        self.assertEqual(self.post.get_uid(), str(self.post.id))

    def test_get_recommendations(self):
        self.assertEqual(list(self.post.get_recommendations()), [self.post2])

    def test_get_text(self):
        self.assertEqual(self.post2.content_format, 'markdown')
        self.assertEqual(self.post.get_text(), u'testing a nice body')
        self.assertEqual(unicode(self.post2.get_text()),
                         u'<h2>testing a nice body</h2>\n')
