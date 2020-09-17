from django.http import HttpResponse,Http404
from django.shortcuts import render
from django.template.loader import get_template
from django.conf import settings

import os
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

def download_page(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print("File Path: " + file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    return Http404

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

