from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, NewsList, NewsSearch, ArticlesList, WrongTypeUpdateException

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

    path('wrong_type_update/', WrongTypeUpdateException.as_view(), name='wrong_type_update'),
]
