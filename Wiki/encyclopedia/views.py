import random
from django import forms
from django.shortcuts import render
from markdown2 import Markdown
from . import util

markdowner = Markdown()


class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}))


class Post(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insert The Post Title'}))
    textarea = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Insert The Content'}))


class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    return render(request, "encyclopedia/entry.html",
                                  {"page": page_converted, "title": item, "form": Search()})
                if item.lower() in i.lower():
                    searched.append(i)
            return render(request, "encyclopedia/search.html", {"searched": searched, "form": Search()})

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form": Search()
        })


def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)
        return render(request, "encyclopedia/entry.html", {"page": page_converted, "title": title, "form": Search()})
    else:
        return render(request, "encyclopedia/error.html", {"message": "Whoops! The requested page was not found.", "form":Search()})


def create(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form": Search(), "message": "Whoops! Page already exist!"})
            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)
                return render(request, "encyclopedia/entry.html",
                              {"form": Search(), "page": page_converted, "title": title})
    else:
        return render(request, "encyclopedia/create.html", {"form": Search(), "post": Post()})


def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",
                      {"form": Search(), "edit": Edit(initial={'textarea': page}), 'title': title})
    else:
        form = Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            page_converted = markdowner.convert(page)
            return render(request, "encyclopedia/entry.html",
                          {"form": Search(), "page": page_converted, "title": title})


def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        page_random = entries[num]
        page = util.get_entry(page_random)
        page_converted = markdowner.convert(page)

        return render(request, "encyclopedia/entry.html",
                      {"form": Search(), "page": page_converted, "title": page_random})
