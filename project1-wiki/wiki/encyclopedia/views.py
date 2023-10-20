import random

from django.db.models.expressions import NoneType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import forms, util

markdowner = Markdown()


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {
            "entries": util.list_entries(),
        },
    )


def content_page(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(
            request,
            "encyclopedia/not_found.html",
            {
                "title": title,
            },
        )

    return render(
        request,
        "encyclopedia/content_page.html",
        {
            "title": title,
            "content": markdowner.convert(content),
        },
    )


def random_page(request):
    """
    open a random wiki page
    """
    print("View Exec")
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(
        reverse("encyclopedia:content_page", kwargs={"title": entry})
    )


def show_search_results(request):
    results = []
    query = ""
    if request.method == "POST":
        query = request.POST.get("q")
        results = util.get_search_results(query)

    if len(results) == 1 and query.lower() in [result.lower() for result in results]:
        # only redirect to a wiki page if the search query exactly(case-insensitive) matches the wiki page title
        return HttpResponseRedirect(
            reverse("encyclopedia:content_page", kwargs={"title": results[0]})
        )
    return render(
        request,
        "encyclopedia/search_results.html",
        {"results": results},
    )


def add_entry(request):
    """
    adds a new entry to local disk
    """
    form = forms.newEntryForm()
    if request.method == "POST":
        form = forms.newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            existing_entries = util.list_entries()
            if title in existing_entries:
                form.add_error("title", "Title already exists, choose a different one")
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(
                    reverse(
                        "encyclopedia:content_page",
                        kwargs={
                            "title": title,
                        },
                    )
                )
    return render(
        request,
        "encyclopedia/add_entry.html",
        {
            "form": form,
        },
    )


def edit_entry(request):
    """
    edits an existing entry
    """
    if request.method == "POST":
        form = forms.newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(
                reverse(
                    "encyclopedia:content_page",
                    kwargs={
                        "title": title,
                    },
                )
            )
        return render(
            request,
            "encyclopedia/edit_entry.html",
            {
                "form": form,
            },
        )

    title = request.GET.get("title")
    return render(
        request,
        "encyclopedia/edit_entry.html",
        {
            "form": util.get_form_content(title),
        },
    )
