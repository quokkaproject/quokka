# coding: utf-8
import logging

from quokka.core.models import Channel, ChannelType, SubContentPurpose, \
    Config, CustomValue
from quokka.modules.accounts.models import User, Role
from quokka.modules.posts.models import Post

logger = logging.getLogger()


class Populate(object):
    def __init__(self, db, *args, **kwargs):
        self.db = db
        self.args = args
        self.kwargs = kwargs
        self.roles = {}
        self.users = {}
        self.channels = {}
        self.channel_types = {}
        self.purposes = {}
        self.custom_values = {}

    def __call__(self, *args, **kwargs):
        self.load_existing_users()
        self.create_users()
        self.create_configs()
        self.create_channel_types()
        self.create_base_channels()
        self.create_channels()
        self.create_purposes()
        self.create_posts()

    def role(self, name):
        if not name in self.roles:
            role, created = Role.objects.get_or_create(name=name)
            self.roles[name] = role
            if created:
                logger.info("Created role: {0}".format(name))
        return self.roles.get(name)

    def load_existing_users(self):
        users = User.objects.all()
        for user in users:
            self.users[user.name] = user

    def create_users(self):
        self.users_data = [
            {
                "name": "admin",
                "email": "admin@example.com",
                "password": "admin",
                "roles": [self.role('admin')]
            },
            {
                "name": "moderator",
                "email": "moderator@example.com",
                "password": "moderator",
                "roles": [self.role('moderator')]
            },
            {
                "name": "editor",
                "email": "editor@example.com",
                "password": "editor",
                "roles": [self.role('editor')]
            },
            {
                "name": "user",
                "email": "user@example.com",
                "password": "user",
                "roles": [self.role('user'), self.role('viewer')]
            },
        ]

        for data in self.users_data:
            name = data.get('name')
            pwd = data.get("password")
            if not name in self.users:
                user = User.createuser(**data)
                self.users[name] = user
                logger.info(
                    "Created: User: mail:{o.email} pwd:{pwd}".format(o=user,
                                                                     pwd=pwd)
                )
            else:
                logger.info("Exist: User: mail:{o[email]}".format(o=data))

    def create_config(self, data):
        try:
            return Config.objects.get(group=data.get('group'))
        except:
            return Config.objects.create(**data)

    def custom_value(self, **data):
        if data.get('name') in self.custom_values:
            return self.custom_values[data.get('name')]

        value = CustomValue(**data)
        self.custom_values[value.name] = value
        return value

    def create_configs(self):
        self.configs_data = [
            {
                "group": "site",
                "description": "Preferences for website",
                "values": [
                    self.custom_value(name="site_name",
                                      rawvalue="Quokka website",
                                      formatter="text"),
                    self.custom_value(name="site_keywords",
                                      rawvalue="cms,quokka,flask,mongo,python",
                                      formatter="text"),
                    self.custom_value(name="site_description",
                                      rawvalue="A Quokka CMS website",
                                      formatter="text"),
                    self.custom_value(name="site_author",
                                      rawvalue="Bruno Rocha",
                                      formatter="text"),
                    self.custom_value(name="site_logo",
                                      rawvalue="/static/img/logo_white.png",
                                      formatter="text")
                ]
            },
            {
                "group": "comments",
                "description": ("Comment system can be: "
                                "internal, disqus, facebook, google\n"
                                "requires_login: 0 or 1"),
                "values": [
                    self.custom_value(name="system",
                                      rawvalue="internal",
                                      formatter="text"),
                    self.custom_value(name="disqus_script",
                                      rawvalue="",
                                      formatter="text"),
                    self.custom_value(name="requires_login",
                                      rawvalue="0",
                                      formatter="int"),
                ]
            },
            {
                "group": "channels",
                "description": "Global preferences for channels",
                "values": [
                    self.custom_value(name="default_channel_type",
                                      rawvalue="list",
                                      formatter="text"),
                    self.custom_value(
                        name="global_content_filters",
                        rawvalue='{"model__not__startswith": "media."}',
                        formatter="json"
                    )
                ]
            },
            {
                "group": "settings",
                "description": "App settings override CAUTION!!!",
                "values": [
                    self.custom_value(name="DEFAULT_THEME",
                                      rawvalue="default",
                                      formatter="text"),
                    self.custom_value(name="ADMIN_THEME",
                                      rawvalue="cosmo",
                                      formatter="text")
                ]
            }
        ]
        for config in self.configs_data:
            self.create_config(config)

    def create_channel(self, data):

        if 'childs' in data:
            childs = data.pop('childs')
        else:
            childs = []

        data['created_by'] = data['last_updated_by'] = self.users.get('admin')

        try:
            channel = Channel.objects.get(slug=data.get('slug'))
            created = False
        except:
            channel, created = Channel.objects.get_or_create(**data)

        if created:
            logger.info("Created channel:{0}".format(channel.title))
        else:
            logger.info("Channel get: {0}".format(channel.title))

        for child in childs:
            child['parent'] = channel
            self.create_channel(child)

        if not channel.slug in self.channels:
            self.channels[channel.slug] = channel

        return channel

    def create_channel_type(self, data):
        try:
            channel_type = ChannelType.objects.get(
                identifier=data.get('identifier'))
            created = False
        except:
            channel_type, created = ChannelType.objects.get_or_create(
                **data
            )

        if created:
            logger.info("Created channel_type:{0}".format(channel_type.title))
        else:
            logger.info("ChannelType get: {0}".format(channel_type.title))

        if not channel_type.identifier in self.channel_types:
            self.channel_types[channel_type.identifier] = channel_type

        return channel_type

    def create_base_channels(self):
        self.channel_data = [
            {
                "title": "Home",
                "slug": "home",
                "description": "Home page",
                "show_in_menu": True,
                "is_homepage": True,
                "include_in_rss": True,
                "published": True,
                "indexable": True,
                "order": 0,
                "channel_type": self.channel_types.get('portal'),
                "content_filters": {"model__not__startswith": "media."},
                "canonical_url": "/"
            },
            {
                "title": "media",
                "slug": "media",
                "description": "Multi Media",
                "show_in_menu": False,
                "is_homepage": False,
                "include_in_rss": False,
                "published": True,
                "channel_type": self.channel_types.get('grid'),
                "canonical_url": "/media",
                "order": 4,
                "childs": [
                    {
                        "title": media,
                        "slug": media.lower(),
                        "description": "{} channel".format(media),
                        "include_in_rss": False,
                        "show_in_menu": False,
                        "published": True,
                        "channel_type": self.channel_types.get('grid'),
                        "is_homepage": False,
                        "canonical_url": "/media/{}".format(media.lower()),
                        "indexable": True,
                        "order": 4
                    }
                    for media in ['Images', 'Videos', 'Audios',
                                  'Files', 'Galleries']
                ]
            },
        ]

        for data in self.channel_data:
            self.create_channel(data)

    def create_channels(self):
        self.channel_data = [
            {
                "title": "Articles",
                "slug": "articles",
                "description": "My articles",
                "show_in_menu": True,
                "is_homepage": False,
                "published": True,
                "order": 1,
                "channel_type": self.channel_types.get('list'),
                "childs": [
                    {
                        "title": "Technology",
                        "slug": "technology",
                        "description": "Technology Articles",
                        "show_in_menu": True,
                        "is_homepage": False,
                        "published": True,
                        "channel_type": self.channel_types.get('grid'),
                        "childs": [
                            {
                                "title": "Mobile",
                                "slug": "mobile",
                                "description": "Technology Mobile Articles",
                                "show_in_menu": True,
                                "is_homepage": False,
                                "channel_type": self.channel_types.get('list'),
                                "published": True,
                            },
                            {
                                "title": "Programming",
                                "slug": "programming",
                                "description": "Programming Articles",
                                "show_in_menu": True,
                                "is_homepage": False,
                                "channel_type": self.channel_types.get('list'),
                                "published": True,
                            },
                        ]
                    },
                    {
                        "title": "Science",
                        "slug": "science",
                        "description": "Science articles",
                        "show_in_menu": True,
                        "is_homepage": False,
                        "channel_type": self.channel_types.get('list'),
                        "published": True,
                        "order": 2
                    },
                ]
            },
            {
                "title": "Blog",
                "slug": "blog",
                "description": "Blog posts",
                "show_in_menu": True,
                "is_homepage": False,
                "channel_type": self.channel_types.get('blog'),
                "published": True,
                "order": 3
            },
        ]

        for data in self.channel_data:
            self.create_channel(data)

    def create_channel_types(self):
        self.channel_type_data = [
            {
                "title": "list",
                "identifier": "list",
                "template_suffix": "default",
            },
            {
                "title": "blog",
                "identifier": "blog",
                "template_suffix": "blog",
            },
            {
                "title": "grid",
                "identifier": "grid",
                "template_suffix": "grid",
            },
            {
                "title": "portal",
                "identifier": "portal",
                "template_suffix": "portal",
            },
        ]

        for data in self.channel_type_data:
            self.create_channel_type(data)

    def create_purpose(self, data):
        if data.get('identifier') in self.purposes:
            return self.purposes[data.get('identifier')]

        purpose, created = SubContentPurpose.objects.get_or_create(
            title=data.get('title'),
            identifier=data.get('identifier'),
            module=data.get('module')
        )

        self.purposes[purpose.identifier] = purpose

        return purpose

    def create_purposes(self):
        self.purpose_data = [
            {
                "title": "General",
                "identifier": "general",
                "module": "Content",
            },
            {
                "title": "Related",
                "identifier": "related",
                "module": "Content",
            },
            {
                "title": "Main Image",
                "identifier": "mainimage",
                "module": "Media",
            },
            {
                "title": "Image",
                "identifier": "image",
                "module": "Media",
            },
            {
                "title": "Video",
                "identifier": "video",
                "module": "Media",
            },
            {
                "title": "Audio",
                "identifier": "audio",
                "module": "Media",
            },
            {
                "title": "Attachment",
                "identifier": "attachment",
                "module": "Media",
            },
            {
                "title": "Link",
                "identifier": "link",
                "module": "Content",
            },
        ]
        for purpose in self.purpose_data:
            self.create_purpose(purpose)

    def create_post(self, data):
        data['created_by'] = data['last_updated_by'] = self.users.get('editor')
        data['published'] = True
        try:
            post = Post.objects.get(slug=data.get('slug'))
            logger.info("Post get: {0}".format(post.title))
        except Exception:
            post = Post.objects.create(**data)
            logger.info("Post created: {0}".format(post.title))

        return post

    def create_posts(self):
        self.post_data = [
            {
                "title": "Python Reaches New Levels of Quality",
                "slug": "python-reaches-new-level-of-quality",
                "summary": """Python Surpasses Standards, Reaches New Levels
                           of Quality""",
                "channel": self.channels.get('programming'),
                "tags": ['quality', 'python', 'coverity'],
                "body": """<p>Throughout Python's 20-plus year history,
                its quality has been in the hands of the volunteers around the
                world openly contributing to it. Thanks to Coverity, those
                volunteers have been pointed to many quality and security
                issues via Coverity Scan, a service which finds defects in
                 C/C++ and Java projects at no cost.</p>
                <p>
                 As the CPython project includes over 370,000 lines of C code*,
                accounting for 42% of the codebase, a lot of it lies outside
                of the analysis tools our community has created to work with
                Python code. Since 2006, Coverity's scans of that code have
                found nearly 1,000 defects, 860 of which our contributors
                have fixed.</p>
                <p>
                In an industry where the standard defect density is a rate of
                 1 per 1,000 lines of code, CPython has attained a rate of
                 0.005 defects per 1,000 lines, and "introduces a new level
                 of quality for open source software," said Coverity.</p>
               <p>
               “Python is the model citizen of good code quality practices,
               and we applaud their contributors and maintainers for their
               commitment to quality,” said Jennifer Johnson, chief marketing
               officer for Coverity.</p>
               <p>
               The PSF and the rest of the community join Coverity in
               applauding all of those who have contributed their time
               and effort to make CPython a better project, along with
               the countless others who contribute to a powerful landscape
               of Python interpreters.</p>"""
            },
            {
                "title": "Google taking Android mainstream with KitKat",
                "slug": "google-taking-android-mainstream-with-kitkat",
                "summary": """Google has been using desserts as codenames
                for major Android versions since the beginning. In a surprise
                move, Google has teamed with the KitKat candy bar for the
                next version""",
                "channel": self.channels.get('mobile'),
                "tags": ['mobile', 'android', 'google'],
                "body": """
                <figure class="alignRight"><img title="KitKat Android"
                alt="KitKat Android"
src="http://cdn-static.zdnet.com/i/r/story/70/00/020234/kitkat-android-
200x136.jpg?hash=ZmSuLmRkZT&amp;upscale=1"
                height="136" width="200"><figcaption>Image credit: Nestle
                </figcaption></figure>
                <p>Amidst all the fury following the announcement of the
                Microsoft/Nokia deal, Google quietly shook up the Android
                space with the unveiling of its affiliation with the KitKat
                candy bar. While Key Lime Pie was long expected to be the next
                major version of Android (4.4),
                <a
href="http://www.zdnet.com/google-readies-android-kitkat-amid-1-billion-
device-activations-milestone-7000020183/">
                ZDNet's Rachel King reports</a> that it will now be known as
                KitKat.</p>
                <p>KitKat is a popular candy bar in the US and more
                importantly is well-known and iconic. Everyone recognizes
                the KitKat and Google is positioning Android to benefit
                from that recognition. While no money changed hands according
                to Google, a <a href="http://kitkat.com/#/acloserlook">new
                promotional video from the KitKat </a>people (Nestle) makes
                it plain that Android is going to be quietly pushed in
                advertising for the candy.</p>
                <p>The clever video pushes the candy bar as a very high-tech
                product (KitKat 4.4) designed to meet customer's needs and
                desires. It's not a coincidence that the candy bar's version
                number, 4.4, also happens to be the Android version it
                represents. It is brilliantly done and seems to take a
                shot at Apple while quietly promoting Android. There is
                even an Android tablet shown in the production.</p>
                <!-- Parsed pinbox:"10126430" -->
                <div class="relatedContent alignRight">
                <h3>What's Hot on ZDNet</h3><ul>
                <li>
                <a
href="http://www.zdnet.com/mac-mini-transition-week-two-mini-mizing-problems-
7000020170/">
                Wanted: Real convergence, not more gear </a></li>

                <li><a
href="http://www.zdnet.com/7-things-i-wish-ios-7-could-do-7000019784/">
                7 things I wish iOS 7 could do</a></li>

                <li><a
href="http://www.zdnet.com/lenovo-doubles-down-on-convertible-pc-bet-
yoga-tizes-lineup-7000020187/">
                Lenovo doubles down on convertible PC bet</a></li>

                <li><a
href="http://www.zdnet.com/nokia-is-dead-newkia-rises-from-its-ashes-
7000020271/">
                Nokia is dead, Newkia rises from its ashes</a></li>
                </ul></div>
                <p>This collaboration between Google and Nestle with the
                 KitKat brand positions the former to put the Android
                 brand front and center with mainstream consumers.
                 That's not been done before as phone partner branding
                 is usually the OEM brand only. There have been phone
                 launch events recently that don't even mention Android,
                 and Google must have been concerned about that.</p>
                <p>Don't be surprised to see more KitKat promotional
                materials that quietly push Android to the non-tech world.
                It's already started with both the video mentioned above and
                the special packages of KitKat bars that have Willy
                Wonka-style tickets inside to give Nexus 7 tablets to
                lucky recipients. It's clear Google is taking the Android
                brand mainstream with the KitKat affiliation.</p>
                <p>As clever as this partnership with KitKat may be, some
                folks are not happy that Key Lime Pie was dropped in favor
                of KitKat. Twitter folk were buzzing about the name switch,
                including Bridget Carey and Tim Stevens of CNET:</p>
                <figure><img title="KitKat Twitter" alt="KitKat Twitter"
src="http://cdn-static.zdnet.com/i/r/story/70/00/020234/kitkat-twitter-
332x396.jpg?hash=MzMvMQRlMw&amp;upscale=1"
                height="396" width="332">
                </figure>
                """
            },
            {
                "title": "Welcome to Quokka CMS",
                "slug": "welcome-to-quokka-cms",
                "summary": """Quokka is a flexible content management
                           platform powered by Python, Flask and MongoDB.""",
                "channel": self.channels.get('home'),
                "tags": ['quokka', 'python', 'flask'],
                "body": """<p>Quokka provides a "full-stack"
            Flask application plus a bunch of selected extensions
            to provide all the needed CMS admin features and a
            flexible-easy way to extend the platform with
            <strong>quokka-modules</strong> built following
            the Flask <strong>Blueprints</strong> pattern.</p>
            <p align="center">
            <a
            href="https://raw.github.com/pythonhub/quokka/master/docs/logo.png"
            target="_blank">
            <img
            src="https://raw.github.com/pythonhub/quokka/master/docs/logo.png"
            alt="quokka cms" style="max-width:100%;"></a></p>"""
            },

        ]

        for data in self.post_data:
            try:
                self.create_post(data)
            except:
                self.create_channels()
                self.create_post(data)
