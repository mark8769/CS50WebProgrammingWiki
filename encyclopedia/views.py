# https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/
# render only works with rendering html from our templates directory!!!!! Wont wont work with some of the urls inside urls.py file!!!!!! TIL (Today I learned)
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
        # using GET instead of POST will get you no key value pairs
        # because we are making the form request as POST
        # Here we are getting the value for the q named input in our form
        query = request.POST.get("q")
        list_entries = util.list_entries()
        # create an empty list for possible entries
        is_this_what_you_meant = []

        for entry in list_entries:

            if query.lower() == entry.lower():
                return HttpResponse(markdown2.markdown(util.get_entry(query)))

            if query.lower() in entry.lower():
                is_this_what_you_meant.append(entry)
        
        # this is working, but when I pass in the list it doesnt? (I guess you have to cast this as a string)
        # return HttpResponse(str(is_this_what_you_meant))
        return render(request, "encyclopedia/search_results.html",{
            "possible_entries": is_this_what_you_meant
        })

    # if request method was a get method, meaning they clicked on a link
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# def wiki(request, TITLE):
#     # TITLE will contain anything appearing 
#     # after localhost:8000/wiki/some_random_string

#     # Check if title passed in by user is in our list_entries
#     # This is kinda of a slow way to do it
#     # Since it the background it is probably 
#     # iterating over the entire list
#     if TITLE not in util.list_entries():
#         return render(request, "wiki/404.html")
#     else:
#         # Provide some additional context, eg. Title of page
#         # so we can change title of page with Django templating (jinja)
#         return render(request, f"wiki/{util.get_entry(TITLE)}",{
#             "title": TITLE
#         })


def wiki(request, TITLE):
    if TITLE not in util.list_entries():
        # haha not sure why templates/ doesn't have to be
        # include in path name, that's ok, but I hate this magic stuff
        return render(request, "encyclopedia/404.html")
    else:
        # return HttpResponse(util.get_entry(TITLE))
        # return render(request, "encyclopedia/generic_entry.html",{
        #     "markdown_entry":markdown2.markdown(util.get_entry(TITLE)),
        #     "title": TITLE
        # })

        # Maybe figure out a way to get 
        # it to work with the commented out version.
        # Would optimally want it to be alongside the sidebar,
        # but when we return the dictionary as context for the html page
        # jinja views the whole markdown as one string rather than html
        # maybe use some jinja filter?
        # return HttpResponse(markdown2.markdown(util.get_entry(TITLE)))
        return render(request, f"encyclopedia/generic_entry.html",{
            "context": markdown2.markdown(util.get_entry(TITLE)),
            "title": TITLE
        })

def new_page(request):

    if request.method == "POST":
        # Submitting form through POST request
        # get form entry from 
        # name="user_entry" inside textarea inside html
        user_markdown = request.POST.get("user_entry")
        # name="user_title" inside inputer field inside html
        user_title = request.POST.get("user_title")

        if user_title in util.list_entries():
            return render(request, "encyclopedia/page_not_saved.html")
        else:
            # else if title does not exist, you can save entry
            util.save_entry(user_title, user_markdown)
            
            # redirect user to our wiki url, since it is on the same page, it is valid
            return redirect(f"wiki/{user_title}")

    return render(request, "encyclopedia/new_page.html")


# use this function, when url follows http://localhost:8000/random
def random(request):
    
    entries_list = util.list_entries()
    # endpoint for range is already exclusive
    # nevermind, not exclusive
    # dont care about being truly random here either
    random_int = randint(0, len(entries_list) - 1)

    entry = entries_list[random_int]

    return redirect(f"wiki/{entry}")

def edit_page(request, TITLE):
    # return HttpResponse(request.POST.get("name"))
    # return render(request, "encyclopedia/edit_page.html")

    # means user finished editing an entry on the edit page
    if request.method == "POST":
        # get entry information (<textarea> id)
        new_entry = request.POST.get("user_entry")
        util.save_entry(TITLE, new_entry)
        
        # return render(request, "encyclopedia/generic_entry.html",{
        #     "title": TITLE,
        #     "context": util.get_entry(TITLE)
        # })

        # Since this route is inside a "folder" edit_page/
        # When you do a redirect, it will append the path to the
        # end of the current url http://localhost:8000/edit_page/

        # The case is different in our new_page route, there we don't go inside
        # another folder, we stay at the root and just render a html page.
        # So when we do a redirect, where just going to a different file in the
        # current folder. E.g http://localhost:8000

        # Maybe fix routes, or try to remove the .. dots. I would rather
        # have wiki handle rendering of the page since thats why it's there.
        # return redirect(f"http://localhost:8000/wiki/{TITLE}") # this is fine, but would rather not hard code url either
        return redirect(f"../wiki/{TITLE}") # this is relative, so if paths change it will be a pain, works for now though.
        # return HttpResponseRedirect(reverse(f"encyclopedia:wiki/{TITLE}"))

    else:
        return render(request, "encyclopedia/edit_page.html", {
            "title": TITLE,
            "entry_info": util.get_entry(TITLE)
        })
    