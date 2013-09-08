
# Quokka CMS Project

#### Definition:

Quokka is a content management system powered by Python, Flask and MongoDB. Using a selection of Flask extensions Quokka also provides a full-stack platform for generic applications.

Quokka is develop for: 
 
- Blogs
- Social websites
- Content portals and magazines
- Intranet
- Simple e-commerce
- Polls, Giveaways, tutorials, courses

In summary, use Quokka for anything using: ```author -> content <- interactions```

#### Objects

- Channels
    - Channels are like directories, you can create many channels and subchannels and include documents in there, channels defines **urls** ```/channel/subchannel/content.html``` by default in Quokka content is always defined by the **.html** extension, but it can be changed.
    - Channels can have alias, example: ```/entertainment/content.html``` is a content endpoint, if you create aliases in **entertainment** channel ```['diversao', 'diversion', 'fun']``` so the same content will be accessible with any alias as the channel unless it do not conflict with another channel real channel name. ```/fun/content.html``` might work and it can be also useful for internationalization. A channel home page will always have the **canonical url** pointing to the real channel.
    - Channels have a type, a type in channel can be anything, by default Quokka provides **blog**, **portal**, **list**, **grid**. You can create your own type by defining its properties.
        - A channel type is (example blog):
            - title: Blog
            - template_suffix: blog
            - inherit: True
            - media files: file_paths

            Basically you are defining the look and feel for that channel.

        - Quokka provides:
            - Blog: a template with blog features, stream of posts, tag cloud, sidebars, widgets.
            - list: a template with a simple list of publications, sorting and search
            - grid: this is a pinterest like template
            - portal: it mixes a **featured** slider with some boxes for grid and listing of posts.
            > Note: In any template type you use blocks and widgets to rearrange the content.

    - Organization of content
        - You can copy/paste content between channels
        - You can program the publication by setting publish data range
    - Settings
        - You can choose some properties for a channel and apply for every subchannel created.
        - include_in_rss: choose if publication will be available in feed
        - rss filters: filter contents which will be available for rss
        - api enabled: choose if that channel will provide its contents api via json or xml
        - api filters: choose filters to be applied in public api 
        > note: This configs are for general public ```get``` api, for REST api take a llok for REST API topic.
    - Content blocks
        - Every channel has its own **namespace** for content blocks, but content blocks are available to be use in any channel
        - a content block is a content aggregator and you can have blocks inside blocks.
        - blocks has a relation with a **Content** + specific fallback attributes like start and end_date, image, title, summary and headline for each content.
        - Blocks have some attributes:
            - order, title, unique_identifier, default_template, block_region
            - custom values to store arbitrary information
        - a block is not stale for a single channel or page, it can be used anywhere so it is generic, the only thing that identify a block is its identifier. But being a Content, every block needs to be inserted in a main channel to be accessible as a bundle, by default quokka defines a **content** channel and every block can be listed in ```/content/blogname```. You can change the **content** with another name in settings.py
        - inside channels you can insert any block and choose its properties, in template will be defined where the block should be included.
        - block_region is a placeholder, defined in the template where blocks will be inserted following its order definition per channel
        - the template will always be the default_template unless specified per_channel, order can also be defined per_channel


- Content
    - A Content is a generic thing that can be inserted in a channel, think this is like a **file** it has some generic attributes defining its title, slug, access url, ownership, control dates, channeling.
    - Everything in Quokka, except a channel, is a Content, even the Content Block is a Content and every content has its own channel and urls.

#### Features

- Channel based document publishing with multi unlimited nested nodes
  - a **content** can be included in many channels, but it needs to be primarily inserted in a master channel, the master channel defined its **canonical** url.
- Multiple authors/collaborators for posts and channels
 

----------


> Written with [StackEdit](http://benweet.github.io/stackedit/).