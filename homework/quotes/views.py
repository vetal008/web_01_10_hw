from bson import ObjectId
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from .forms import AuthorForm, QuoteForm
from .utils import get_mongodb


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


from . import migration
from . import add_quotes


def load_sql(request):
    add_quotes.add_quotes()
    migration.make_migrate()
    return redirect('quotes:root')


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:root')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {"form": form})


def author_detail(request, author_id):
    db = get_mongodb()
    author = db.authors.find_one({"_id": ObjectId(author_id)})
    if not author:
        raise Http404("Author not found")
    return render(request, 'quotes/author_detail.html', {"author": author})


# def author_detail(request, author_id):
#     author = get_object_or_404(Author, id=author_id)
#     return render(request, 'quotes/author_detail.html', {"author": author})


@login_required
def add_author(request):
    db = get_mongodb()
    authors = [author['author_fullname'] for author in db.authors.find()]
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            # після збереження можна перенаправити на список авторів або головну
            return redirect('quotes:root')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {"form": form})
