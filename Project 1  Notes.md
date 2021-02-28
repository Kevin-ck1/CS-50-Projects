# Project 1 : Notes

## Step 1

Setting up the urls, in this case we are to use place holders.

On the views.py

```python
def test(request, title):
    return HttpResponse(f"Hello, {title.capitalize()}!")
```

And on the urls.py

```python
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.test, name="test")
]
```

The above codes are for testing

To display the md files we are to create a `contents.html` template

```django
{% extends "encyclopedia/layout.html" %}

{% block title %}
    {{title}}
{% endblock %}

{% block body %}
    
    {{entry}}

{% endblock %}
```



Since the its okay, we can write the function for displaying the md files

```python
def test(request, title):
    return render(request, "encyclopedia/contents.html", {
        "title": title,
        "entry": util.get_entry(title)
    })

```



## Step 2

**Converting the List of entries to clickable links**

```django
    <ul>
        {% for entry in entries %}
            <li> <a href="{% url 'test' entry %}"> {{ entry }} </a> </li>
        {% endfor %}
    </ul>
```

**Note** in case an element is encased with `{% %}` , if we want to use a variable we can use the name of the variable as it is, adding `{{ }}` to the variable will cause an error.



## Step 3 

Rendering the sample MD files into html

On the views.py

```python
def test(request, title):
    return render(request, "encyclopedia/contents.html", {
        "title": title,
        "entry": markdown2.markdown(util.get_entry(title))
    })
```

On the content template

```django
{% extends "encyclopedia/layout.html" %}

{% block title %}
    {{title}}
{% endblock %}

{% block body %}
    
    {{entry|safe}}

{% endblock %}
```

**Note** ` {{entry|safe}}`, we use `safe` so as to remove the escape characters

## Step 4

Adding a new entry

First, we create a html template for the adding of the page

```django
{% extends "encyclopedia/layout.html" %}

{% block title %}
    {{title}}
{% endblock %}

{% block body %}
    
    <form>
        <label for="entry_title">Title:</label>
        <input class="entry_title" type="text" name="q" placeholder="Title">
        <br>
        <label for="entry_content">Content:</label>
        <input class="entry_content" type="text" name="q" placeholder="Content">
    </form>

{% endblock %}
```



