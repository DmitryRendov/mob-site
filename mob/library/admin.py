from django.contrib import admin
from django.urls import reverse

from .models import Article, Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    view_on_site = False
admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display  = ('title', 'display_categories', 'publish', 'status')
    list_filter   = ('publish', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    def view_on_site(self, obj):
        url = reverse('library:article_detail', kwargs={'slug': obj.slug})
        return url
admin.site.register(Article, ArticleAdmin)
