from django.contrib import admin
from .models import Article, Comment, Review


class CommentInline(admin.TabularInline):  # new
    model = Review
    


class ArticleAdmin(admin.ModelAdmin):  # new
    inlines = [
        CommentInline,
    ]
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['ud','user','rate','created_at']
    readonly_fields = ['created_at',]

admin.site.register(Article, ArticleAdmin)  # new
admin.site.register(Comment)
admin.site.register(Review)

