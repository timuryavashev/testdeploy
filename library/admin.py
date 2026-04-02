from django.contrib import admin
from .models import Author, Book, Review

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_day")
    search_fields = (
        "first_name",
        "last_name",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "publication_data", "author")
    list_filter = ("publication_data", "author")
    search_fields = ("title", "author__first_name", "author__last_name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "rating")
