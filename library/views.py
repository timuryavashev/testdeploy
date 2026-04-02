from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import AuthorForm, BookForm
from .models import Book, Author
from .sevices import BookServices
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden


class ReviewBookView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if not request.user.has_perf("library.can_review_book"):
            return HttpResponseForbidden("У вас нет права для рецензирования книги")
        book.review = request.POST.get("review")
        book.save()
        return redirect("library:book_detail", pk=book_id)


class RecommendBookView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if not request.user.has_perf("library.can_recommend_book"):
            return HttpResponseForbidden("У вас нет права для рекомендации книги")
        book.recommend = True
        book.save()
        return redirect("library:book_detail", pk=book_id)


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "library/author_form.html"
    success_url = reverse_lazy("library:authors_list")


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "library/author_form.html"
    success_url = reverse_lazy("library:authors_list")


class AuthorListView(ListView):
    model = Author
    template_name = "library/authors_list.html"
    context_object_name = "authors"


class BooksListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "library/books_list.html"
    context_object_name = "books"


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "library/book_form.html"
    success_url = reverse_lazy("library:books_list")


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_book_count"] = Book.objects.filter(
            author=self.object.author
        ).count()

        book_id = self.object.id

        context["average_rating"] = BookServices.calculate_average_rating(book_id)
        context["is_popular"] = BookServices.is_popular(book_id)

        return context


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "library/book_form.html"
    success_url = reverse_lazy("library:books_list")


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "library/book_confirm_delete.html"
    success_url = reverse_lazy("library:books_list")
