from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm

# CRUD operations
def blog_post_list_view(request):
    # get a of all objects
    qs = BlogPost.objects.published()

    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()

    template_name = "blog/list.html"
    context = {'object_list' : qs}

    return render(request, template_name, context) 

#@login_required
@staff_member_required
def blog_post_create_view(request):
    # Create objects

    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if(form.is_valid()):
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()

    template_name = "form.html"

    context = {'title' : "Create a new blog post",'form' : form}
    
    return render(request, template_name, context)

def blog_post_detail_view(request,slug):
    # returns 1 object or detail view
    obj = get_object_or_404(BlogPost,slug=slug)
    template_name = 'blog/detail.html'
    context = {"object" : obj}
    return render(request, template_name, context) 

@staff_member_required 
def blog_post_update_view(request,slug):
    obj = get_object_or_404(BlogPost,slug=slug)
    form = BlogPostModelForm(request.POST or None,request.FILES or None,instance=obj)

    if form.is_valid():
        form.save()
        form = BlogPostModelForm()
        return redirect('/blog')

    template_name = 'form.html'
    context = {'form' : form, "title" : f"Update {obj.title}"}
    return render(request, template_name, context) 


@staff_member_required
def blog_post_delete_view(request,slug):
    obj = get_object_or_404(BlogPost,slug=slug)
    template_name = 'blog/delete.html'

    if request.method == "POST":
        obj.delete()
        return redirect('/blog')

    context = {"object" : obj,  'form' : None}
    return render(request, template_name, context) 