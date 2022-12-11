from django.urls import path
from . import views
#from .views import (
 #   ArticleListView,
  #  ArticleUpdateView,
   # ArticleDetailView,
    #ArticleDeleteView,
    #ArticleCreateView,
 #   rate,
  #  index,
   # Review_rate  # new
#)

urlpatterns = [
    
    path("<int:pk>/edit/", views.ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/delete/", views.ArticleDeleteView.as_view(), name="article_delete"),
    path("new/", views.ArticleCreateView.as_view(), name="article_new"),  # new
    path("create/", views.ArticleNewView.as_view(), name="article_create"), 
    path("", views.ArticleListView.as_view(), name="article_list"),
    
    path('review/', views.Review_rate, name='review')
] 
