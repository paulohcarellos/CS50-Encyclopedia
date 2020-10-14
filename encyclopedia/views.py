from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

import re
from . import util
from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "entryURL" : ["wiki/{0}".format(entry) for entry in util.list_entries()]
    })


def entry_page(request, entry):
    if entry.lower() in map(str.lower, util.list_entries()):
        html = util.get_source(entry)
    else:
        return render(request, "errors/notFound.html", {
            "title": " ".join(map(lambda word : word[0].upper() + word[1:], re.split("/[^A-Za-z]/", entry)))
        })

    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "html" : html
    })


def search_page(request):
    empty = True
    query = request.GET.get('q')
    matches = util.search(util.list_entries(), query)

    if len(matches) == 1 and query.lower() == matches[0].lower():
        return HttpResponseRedirect("/wiki/" + matches[0])

    if len(matches) > 0:
        empty = False

    return render(request, "encyclopedia/search.html", {
        "entries": matches, 
        "entryURL" : ["wiki/{0}".format(entry) for entry in matches],
        "empty" : empty
    })


def random_page(request):
    entries = util.list_entries()
    page = entries[randint(0, len(entries) - 1)]

    return HttpResponseRedirect(reverse("entry", args=[page]))

def input_page(request, title, new):
    if request.method == "POST":
        title = request.POST.get('t')
        content = request.POST.get('c')

        if new and title.lower() in map(str.lower, util.list_entries()):
            return render(request, "errors/duplicate.html", {
                "title": " ".join(map(lambda word : word[0].upper() + word[1:], re.split("/[^A-Za-z]/", title)))
            })

        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))

    return render(request, "encyclopedia/input.html", {
        "title": title,
        "newPage": new,
        "content": util.get_entry(title) if not new else ""
    })
