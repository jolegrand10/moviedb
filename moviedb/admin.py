from django.contrib import admin
from .models import Movie, Director
# Register your models here.


class MovieInline(admin.TabularInline):
    model=Movie
    fieldsets=[
        (None,{'fields':['title', 'comment']})
        ]

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    inlines= [MovieInline,]

admin.site.register(Movie)
