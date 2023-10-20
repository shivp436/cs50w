import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown

from . import forms

markdowner = Markdown()


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(
        sorted(
            re.sub(r"\.md$", "", filename)
            for filename in filenames
            if filename.endswith(".md")
        )
    )


def get_search_results(query):
    """
    Returns a list of items, which either match or are a superstring of the given query
    """
    results = []
    all_entries = list_entries()
    for entry in all_entries:
        if query.lower() in entry.lower():
            results.append(entry)
    return results


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def get_form_content(title):
    """
    gets the title file content
    """
    filename = f"entries/{title}.md"
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    form = forms.newEntryForm(initial={"title": title, "content": content})
    return form
