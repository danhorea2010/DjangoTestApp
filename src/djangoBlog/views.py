from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):

    qs = BlogPost.objects.filter(publish_date__isnull=False)[:5]

    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()

    context = {
        "title" : "Welcome",
        "blog_list" : qs,
    }

  
    return render(request, "home.html", context)

def about_page(request):
    return render(request, "about.html", {"title" : "About us"})


def contact_page(request):

    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()

    context =  {
        "title" : "Contact us",
        "form" : form
    }

    return render(request, "form.html", context)

