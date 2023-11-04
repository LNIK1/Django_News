from django.urls import path
from django.views.decorators.cache import cache_page  # @cache_page(60)
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, NewsList, NewsSearch, ArticlesList,\
    posts_by_category_list, subscribe_ctg, unsubscribe_ctg,\
    WrongTypeUpdateException

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/', NewsList.as_view(), name='news'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/', ArticlesList.as_view(), name='articles'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update', PostUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
    path('category/<int:id_ctg>', posts_by_category_list, name='posts_by_category_list'),
    path('category/subscribe/<int:id_ctg>', subscribe_ctg, name='subscribe_ctg'),
    path('category/unsubscribe/<int:id_ctg>', unsubscribe_ctg, name='unsubscribe_ctg'),

    path('wrong_type_update/', WrongTypeUpdateException.as_view(), name='wrong_type_update'),
]
