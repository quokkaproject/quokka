from flask import current_app, render_template
from flask.views import MethodView
from .models import make_model


class DetailView(MethodView):
    def get(self, slug):
        category, _, slug = slug.rpartition('/')
        content = current_app.db.get_with_content(slug=slug, category=category)
        article = make_model(content)
        return render_template(
            'article.html',
            article=article,
            category=article.category,
            author=article.author,
            tags=article.tags,
        )
