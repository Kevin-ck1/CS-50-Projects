from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random, secrets
from django import forms

from . import util

class EntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={"class":"form-control col-md-10 "}))
    #entry_title = forms.CharField()
    #entry_content = forms.CharField()
    entry_content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"class":"form-control col-md-10",'rows': 10, 'cols': 10}))
    entry_edit = forms.BooleanField(widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search":1
    })

def entry_page(request, title):
    #return HttpResponse(f"Hello, {title.capitalize()}!")
    #entry_md = util.get_entry(title)
    #entry_html = markdown2.markdown(entry_md)
    if (util.get_entry(title) is not None):
        return render(request, "encyclopedia/contents.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title))
        })
    #return HttpResponse(f"No search item")
    return render(request, "encyclopedia/errorPage.html",{
        "errorMessage": 1
    })


def search(request):
    search_query = request.GET.get('q', '')
    #print(util.list_entries(search_query))
    #if (util.get_entry(search_query) is not None):
        #return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':search_query}))
    entry_list = util.list_entries()
    search_list = []
    search_list2 = []
    for x in search_query.split():
        for y in entry_list:
            if x.upper() in y.upper():
                search_list.append(y)
            elif x[:len(y)].upper() in y.upper():
                search_list2.append(y)

    print(search_list2)
    list_len = len(search_list)
    #if list_len == 1:
        #return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':search_list[0]}))
    #if len(search_list) > 0:
    #    if (util.get_entry(search_query) is not None):
    #        return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':search_query}))
    #    return render(request, "encyclopedia/index.html", {
    #        "entries": search_list,
    #        "search": 2
    #    })
    #return HttpResponse(f"No search item")

    if (util.get_entry(search_query) is not None):
            return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':search_query}))
    elif  len(search_list) > 0:
        return render(request, "encyclopedia/index.html", {
            "entries": search_list,
            "search": 2
        })

    elif len(search_list2) > 0:
        return render(request, "encyclopedia/index.html", {
            "entries": search_list2,
            "search": 2
    })
    return render(request, "encyclopedia/errorPage.html",{
        "errorMessage": 2,
        "errorDisplay": search_query
    })

def add_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_content = form.cleaned_data['entry_content']
            entry_edit = form.cleaned_data['entry_edit']

            if entry_title not in util.list_entries():
                util.save_entry(entry_title, entry_content)
                return HttpResponseRedirect(reverse("wiki:index"))
            elif entry_edit:
                util.save_entry(entry_title, entry_content)
                return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':entry_title}))
            else:
                return render(request, "encyclopedia/add_entry.html",{
                    "form": form,
                    "entry": entry_title,
                    "errorMessage": True
                })

        return render(request, "encyclopedia/add_entry.html",{
            "form": form
        })

    return render(request, "encyclopedia/add_entry.html",{
        "form": EntryForm()
    })

def add(request):
    if request.method == "POST":
        #form = request.POST
        form = EntryForm(request.POST)
        print(form)
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_content = form.cleaned_data['entry_content']
            util.save_entry(entry_title, entry_content)
            return HttpResponseRedirect(reverse("wiki:index"))

        return render(request, "encyclopedia/add.html")
        #print(form)
        #util.save_entry(form['entry_title'], form['entry_content'] )
        #return HttpResponseRedirect(reverse("wiki:index"))
        #if add.is_valid():
            #entry_title = form.cleaned_data['entry_title']
            #entry_content = form.cleaned_data['entry_content']
            #util.save_entry(entry_title, entry_content)

            #return HttpResponseRedirect(reverse("wiki:index"))
        #else:
           #return render(request, "encyclopedia/add.html", {
               #"form": form
               #})

    return render(request, "encyclopedia/add.html")

def edit_entry(request, title):
        content = util.get_entry(title)
        #print(content)
        form1 = EntryForm()
        form1.fields["entry_content"].initial = content
        form1.fields["entry_title"].initial = title
        form1.fields["entry_edit"].initial = True
        #print(form1.entry_content)
        return render(request, "encyclopedia/add_entry.html",{
            "form": form1,
            "title": title,
            "edit": True
    })

def random(request):
    list_entries = util.list_entries()
    #random_page = random.choice(list_entries)
    # random.choice -- not working
    random_page = secrets.choice(util.list_entries())
    print(random_page)
    return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':random_page}))
