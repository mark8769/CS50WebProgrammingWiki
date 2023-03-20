# https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from random import randint

from . import util

def index(request):

    if request.method == "POST":
        # https://stackoverflow.com/questions/64222525/how-to-execute-url-passed-key-value-pairs-from-django-httprequest-object
        query = request.POST.get("q")
        list_entries = util.list_entries()
        # create an empty list for possible entries
        is_this_what_you_meant = []

        for entry in list_entries:

            if query.lower() == entry.lower():
                return HttpResponse(markdown2.markdown(util.get_entry(query)))

            if query.lower() in entry.lower():
                is_this_what_you_meant.append(entry)
        
        return render(request, "encyclopedia/search_results.html",{
            "possible_entries": is_this_what_you_meant
        })

    # if request method was a get method (click on link, redirect)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, TITLE):
    if TITLE not in util.list_entries():
        # render html file from templates/encyclopedia folder
        return render(request, "encyclopedia/404.html")
    else:
        return render(request, f"encyclopedia/generic_entry.html",{
            "context": markdown2.markdown(util.get_entry(TITLE)),
            "title": TITLE
        })

def new_page(request):

    if request.method == "POST":
        # Submitting form through POST request
        # get form entry from 
        # name="user_entry" inside textarea inside new_page.html
        user_markdown = request.POST.get("user_entry")
        # name="user_title" inside input field inside new_page.html
        user_title = request.POST.get("user_title")

        if user_title in util.list_entries():
            return render(request, "encyclopedia/page_not_saved.html",
                          {"context": "Entry already exists. Consider editing instead."})
        else:
            # Else if title does not exist, you can save entry.
            util.save_entry(user_title, user_markdown)
            # Redirect user to wiki route.
            return redirect(f"wiki/{user_title}")

    return render(request, "encyclopedia/new_page.html")


def random(request):
    
    entries_list = util.list_entries()
    random_int = randint(0, len(entries_list) - 1)
    entry = entries_list[random_int]

    return redirect(f"wiki/{entry}")

def edit_page(request, TITLE):

    # user submitted their changes through submit entry button
    if request.method == "POST":
        # get entry information (<textarea> id)
        new_entry = request.POST.get("user_entry")
        util.save_entry(TITLE, new_entry)
        
        # return redirect(f"http://localhost:8000/wiki/{TITLE}") # this is fine, but would rather not hard code url either
        return redirect(f"../wiki/{TITLE}") # this is relative, so if paths change it will be a pain, works for now though.
        # return HttpResponseRedirect(reverse(f"encyclopedia:wiki/{TITLE}"))
        
    else:
        return render(request, "encyclopedia/edit_page.html", {
            "title": TITLE,
            "entry_info": util.get_entry(TITLE)
        })
    