from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article
from .models import Rating
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

class ArticleListView(LoginRequiredMixin, ListView):  # new
    model = Article
    template_name = "article_list.html"



class ArticleDetailView(LoginRequiredMixin, DetailView):  # new
    model = Article
    template_name = "article_detail.html"


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # new
    model = Article
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # new
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_new.html"
    fields = (
        "title",
        "body",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def index(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.all()
    for article in articles:
        rating = Rating.objects.filter(article=article, user=request.user).first()
        article.user_rating = rating.rating if rating else 0
    return render(request, "templates/article_list.html", {"articles": articles})

def rate(request: HttpRequest, article_id: int, rating: int) -> HttpResponse:
    article = Article.objects.get(id=article_id)
    Rating.objects.filter(article=article, user=request.user).delete()
    article.rating_set.create(user=request.user, rating=rating)
    return index(request)