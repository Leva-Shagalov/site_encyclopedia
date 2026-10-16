from django.urls import path

from .views import index, game_updates_page, community, page_article, add_article, add_article_content, reserch_article_not_checked, edit_article, get_data_form

urlpatterns = [
    path("", index),
    path("updates", game_updates_page, name="updates"),
    path("community", community, name="community"),
    path("article/<int:article_id>", page_article, name="article"),
    path("add_article", add_article, name="add_article"),
    path("add_article/<int:article_id>", add_article_content, name="add_article_content"),
    path("reserch_article_not_checked/<int:article_id>", reserch_article_not_checked, name="reserch_article_not_checked"),
    path("edit_article/<int:content_id>", edit_article, name="edit_article"),
    path("api/content/<int:content_id>", get_data_form, name="api_for_edit_article")
]
