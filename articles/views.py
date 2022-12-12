from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article

from .models import Review
from django.shortcuts import redirect, render
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
        "username",
        "description",
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


class ArticleCreateView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_new.html"

class ArticleNewView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_create.html"
    fields = ('username','description','picture')
    

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

def Review_rate(request):
    if request.method == "GET":
        article_id = request.GET.get('article_id')
        comment = request.GET.get('comment')
        rate = request.GET.get('rate')
        author = request.user
        Review(article_id=article_id,author=author,comment=comment,rate=rate).save()
        return redirect('article_new')

def search_user(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        #users = Article.objects.all(username__contains = searched)
        users = Article.objects.filter(username__contains = searched)
        return render(request, 'search_user.html',{'searched': searched, 'users': users })
    
   