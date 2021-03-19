from django.contrib import admin
from main.models import *


class GenreAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'slug')
    list_display_links = ('title',)


admin.site.register(Comment)
admin.site.register(Movie)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(History)
admin.site.register(Genre, GenreAdmin)