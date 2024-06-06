from decouple import config
from django.shortcuts import render, redirect
from markdown import Markdown
from random import choice 
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    wiki_page = util.get_entry(title)

    if (not wiki_page):
        return render(request, "encyclopedia/fail.html", {
          "message": "Not Found",
          "status": 404
        })

    markdowner = Markdown()

    html_wiki_page = markdowner.convert(wiki_page)

    return render(request, "encyclopedia/title.html", {
        "title": title,
        "html_page": html_wiki_page
    })


def search(request):
    search_key = request.POST.get("q", "")
    
    entries = util.list_entries()
    exists = search_key in entries
    
    if exists:
        return redirect('title', title=search_key)

    filtered_entries = [entry for entry in entries if not entry.find(search_key) == -1]

    return render(request, "encyclopedia/index.html", {
        "entries": filtered_entries
    })

def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/editor.html")
    
    if request.method == 'POST':
        if not "is-admin" in request.session:
            return render(request, "encyclopedia/fail.html", {
                "message": "Forbidden",
                "description": "You have to connect as an admin",
                "status": 403
            }) 

        file_content = request.POST.get("content","")
        file_title = request.POST.get("title", "")

        if (len(file_content) == 0 or len(file_title) == 0):
            return render(request, "encyclopedia/fail.html", {
                "message": "Bad Request",
                "description": "Title and content cannot be empty",
                "status": 400
            }) 

        if util.get_entry(file_title):
            return render(request, "encyclopedia/fail.html", {
                "message": "Bad Request",
                "description": "This page already exists",
                "status": 400
            }) 

        util.save_entry(file_title, file_content)

        return redirect('title', title=file_title)

def login(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/login.html')

    if request.method == 'POST':
        password = request.POST.get("password", "")
        
        is_admin = password == config("ADMIN_PASSWORD")
        
        if not is_admin:
            return render(request, "encyclopedia/fail.html", {
                "message": "Unauthorized",
                "description": "Wrong password",
                "status": 401
            }) 

    request.session["is-admin"] = True

    return redirect('index')

def logoff(request):
    del request.session["is-admin"]
    return redirect('index')    


def edit(request, title):
    if request.method == 'GET':

        wiki_page = util.get_entry(title)

        if (not wiki_page):
            return render(request, "encyclopedia/fail.html", {
              "message": "Not Found",
              "status": 404
            })

        return render(request, "encyclopedia/editor.html", {
            "title": title,
            "md_page": wiki_page
        })

    if request.method == 'POST':
        if not "is-admin" in request.session:
            return render(request, "encyclopedia/fail.html", {
                "message": "Forbidden",
                "description": "You have to connect as an admin",
                "status": 403
            }) 

        file_content = request.POST.get("content","")
        file_title = request.POST.get("title", "")

        print(file_content)
        print(file_title)

        if (len(file_content) == 0 or len(file_title) == 0):
            return render(request, "encyclopedia/fail.html", {
                "message": "Bad Request",
                "description": "Title and content cannot be empty",
                "status": 400
            }) 

        util.save_entry(file_title, file_content)

        return redirect('title', title=file_title)    

def random(request):
    entries = util.list_entries()
    selected_choice = choice(entries)
    
    return redirect('title', title=selected_choice)
    