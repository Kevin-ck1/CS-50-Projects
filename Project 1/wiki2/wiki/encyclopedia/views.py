from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from django import forms
import random, secrets

from . import util

class EntryForm(forms.Form):
    entry_title = forms.CharField(
        label="Entry Title", 
        widget=forms.TextInput(attrs={"class":"form-control col-md-8"})
    )  
    entry_content = forms.CharField(
        label="Content", 
        widget=forms.Textarea(
            attrs={"class":"form-control col-md-8" ,'rows': 10, 'cols': 10})
    )
    entry_edit = forms.BooleanField(widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "allPages": True
    })

def entry_page(request, title):
    if util.get_entry(title) is not None :
        return render(request, "encyclopedia/entryPage.html",{
            "title": title,
            "entry_content": markdown2.markdown(util.get_entry(title))
        })
    return render(request, "encyclopedia/errorPage.html",{
        "errorType": 1
    })
def search(request):
    search_query = request.GET.get('q', '')
    query_list = []
    entry_list = util.list_entries()
    for x in search_query.split():
        for y in entry_list:
            for yy in y.split():
                if x[:len(yy)].upper() in yy.upper():
                    query_list.append(y)
    
    if util.get_entry(search_query) is not None:
        return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':search_query}))
    elif len(query_list) > 0:
        return render(request, "encyclopedia/index.html", {
            "entries": query_list,
            "allPages": False,
            "searchMessage": search_query
        })
    return render(request, "encyclopedia/errorPage.html",{
        "errorType": 2,
        "searchMessage": search_query
    })

def add_page(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_content = form.cleaned_data['entry_content']
            entry_edit = form.cleaned_data['entry_edit']

            if (util.get_entry(entry_title) is None):
                util.save_entry(entry_title, entry_content)
                return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':entry_title}))
            
            elif entry_edit:
                util.save_entry(entry_title, entry_content)
                return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title':entry_title}))
            else:
                return render(request, "encyclopedia/addPage.html",{
                    "form": form,
                    "entryTitle": entry_title,
                    "errorMessage": True
                })
        return render(request, "encyclopedia/addPage.html",{
            "form": form
        })

    return render(request, "encyclopedia/addPage.html",{
        "form": EntryForm()
    })

def edit_page(request, title):
    entry_content = util.get_entry(title)
    form = EntryForm()
    form.fields['entry_title'].initial = title
    form.fields['entry_title'].widget.attrs['readonly'] = True
    form.fields['entry_content'].initial = entry_content
    form.fields['entry_edit'].initial = True
    return render(request, "encyclopedia/addPage.html",{
        "form": form,
        "title": title,
        "editing": True
    })
def random(request):
    entry_list = util.list_entries()
    random_entry = secrets.choice(entry_list)
    return HttpResponseRedirect(reverse('wiki:entry_page', kwargs={'title':random_entry}))

