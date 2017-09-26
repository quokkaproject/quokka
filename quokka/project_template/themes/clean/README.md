# Pelican Clean Blog Theme

Theme based in [Clean Blog layout](http://ironsummitmedia.github.io/startbootstrap-clean-blog/).

## Screenshot

![Screenshot](screenshot.png)

## Basic configuration

All configurations about this theme.

### Header Covers

To define custom header cover, set the property ``HEADER_COVER`` in ``pelicanconf.py``:

```python
HEADER_COVER = 'static/my_image.png'
```

### Header Color

To define a simple header background color, set the property ``HEADER_COLOR`` in ``pelicanconf.py``:

```python
HEADER_COLOR = 'black'
```

you can use any valid css color.

### Social URLs

Github, Twitter and Facebook URLs set these properties:

```python
SOCIAL = (('twitter', 'https://twitter.com/myprofile'),
          ('github', 'https://github.com/myprofile'),
          ('facebook','https://facebook.com/myprofile'),
          ('flickr','https://www.flickr.com/myprofile/'),
          ('envelope','mailto:my@mail.address'))
```

If you have new links add them to SOCIAL. The Name has to be the name of the corresponding FontAwesome icon.
If ``SHOW_SOCIAL_ON_INDEX_PAGE_HEADER`` is set to True social icons will be
shown under site sub-title on the index page.

### External feed URL

You can specify an external feed URL (e.g. FeedBurner) in ``SOCIAL`` using the
``rss`` or ``rss-square`` icons. The icon will be shown in the footer with the
rest of your ``SOCIAL`` accounts. A ``<link>`` tag for the external feed will be
placed in ``<head>`` instead of the default Pelican feeds.

### Code highlights

This theme contains this color schemes:

 - Tomorrow - ``tomorrow.css``;
 - Tomorrow Night - ``tomorrow_night.css``;
 - Monokai - ``monokai.css``;
 - Github - ``github.css``;
 - Github Jekyll (Gray BG Jekyll way) - ``github_jekyll.css``;
 - Darkly (Default) - ``darkly.css``;

To customize, define ``COLOR_SCHEME_CSS`` in ``pelicanconf.py`` with css filename. Example:

```python
COLOR_SCHEME_CSS = 'monokai.css'
```

### User defined CSS

Define ``CSS_OVERRIDE`` in ``pelicanconf.py`` to insert a user defined CSS file
after theme CSS. Example:

```python
CSS_OVERRIDE = 'myblog.css'
```

### Disable theme JavaScript

Set ``DISABLE_CUSTOM_THEME_JAVASCRIPT`` to True if you want to disable
``js/clean-blog.min.js`` in case it affects forms and input fields.

### User defined footer

Define ``FOOTER_INCLUDE`` in ``pelicanconf.py`` to insert a custom footer text
instead the default "Powered by Pelican". The value is a template path. You also
need to define the ``EXTRA_TEMPLATES_PATHS`` setting. If your custom footer
template is stored under the content ``PATH`` then Pelican will try to render
it as regular HTML page and will most likely fail. To prevent Pelican from
trying to render your custom footer add it to ``IGNORE_FILES``. Example:

```python
FOOTER_INCLUDE = 'myfooter.html'
IGNORE_FILES = [FOOTER_INCLUDE]
EXTRA_TEMPLATES_PATHS = [os.path.dirname(__file__)]
```

**WARNING:** avoid using names which duplicate existing templates from the
theme directory, for example ``footer.html``. Due to how Pelican searches the
template directories it will first find the files in the theme directory and you
will not see the desired results.

### Analytics

Accept many analytics:

 - Google Analytics: ``GOOGLE_ANALYTICS``;
 - Gauges: ``GAUGES``
 - Piwik: ``PIWIK_URL`` and ``PIWIK_SITE_ID``.

### Favicon

To define if using a favicon and format:

```python
FAVICON = 'favicon.ico'
```

**WARNING:** Is necessary static_paths configured:

```python
STATIC_PATHS = ['images', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'}
}
```

### Other configuration

 - If ``ADDTHIS_PUBID`` is defined sharing buttons from AddThis will appear
 at the bottom of the article;
 - ``GOOGLE_SITE_VERIFICATION`` - Google site verification token;
 - Set ``SHOW_FULL_ARTICLE`` to True to show full article content on index.html
 instead of summary;
 - Set ``SHOW_SITESUBTITLE_IN_HTML`` to True to make use of the ``SITESUBTITLE``
 variable inside the ``<title>`` HTML tag;
 - Set ``FACEBOOK_ADMINS`` to a list of Facebook account IDs which are
 associated with this blog. For example ``['12345']``. For more info see
 https://developers.facebook.com/docs/platforminsights/domains

### Articles

 - To customize header cover to articles, insert the metadata ``header_cover``.
 - To customize OpenGraph images, insert the metadata ``og_image``, otherwise
 ``header_cover``, ``HEADER_COVER`` or a default image is used.
 - To customize Twitter card images, insert the metadata ``twitter_image``,
 otherwise ``header_cover``, ``HEADER_COVER`` or a default image is used.
 Twitter cards are automatically generated if the ``twitter`` icon is configured
 in ``SOCIAL``!

All image paths are relative from the site root directory. You can also use
absolute URLs for ``og_image`` and ``twitter_image``.

Example:


 - To RST
```rst
My super title
##############

:date: 2010-10-03 10:20
:modified: 2010-10-04 18:40
:tags: thats, awesome
:category: yeah
:slug: my-super-post
:authors: Alexis Metaireau, Conan Doyle
:summary: Short version for index and feeds
:header_cover: /images/posts/super-title/cover.png
:og_image: /images/posts/super-title/facebook_cover.png
:twitter_image: /images/posts/super-title/twitter_cover.png
```

 - To Markdown
```markdown
Title: My super title
Date: 2010-12-03 10:20
Modified: 2010-12-05 19:30
Category: Python
Tags: pelican, publishing
Slug: my-super-post
Authors: Alexis Metaireau, Conan Doyle
Summary: Short version for index and feeds
Header_Cover: /images/posts/super-title/cover.png
Og_Image: http://example.com/facebook_cover.png
Twitter_Image: http://example.com/twitter_cover.png

This is the content of my super blog post.
```

Other metada was created to assign resume of article, with ``headline``:

 - To RST
```rst
My super title
##############

:date: 2010-10-03 10:20
:modified: 2010-10-04 18:40
:tags: thats, awesome
:category: yeah
:slug: my-super-post
:authors: Alexis Metaireau, Conan Doyle
:summary: Short version for index and feeds
:headline: Resume of article
```

 - To Markdown
```markdown
Title: My super title
Date: 2010-12-03 10:20
Modified: 2010-12-05 19:30
Category: Python
Tags: pelican, publishing
Slug: my-super-post
Authors: Alexis Metaireau, Conan Doyle
Summary: Short version for index and feeds
Headline: Resume of article

This is the content of my super blog post.
```

