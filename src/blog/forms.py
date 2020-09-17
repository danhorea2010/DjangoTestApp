from django import forms
from .models import BlogPost

class BlogPostForm(forms.Form):
    title   = forms.CharField()
    slug    = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)


class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'content', 'publish_date','image','fileDownload']

    def clean_title(self, *args, **kwargs):

        title = self.cleaned_data.get("title")
        qs = BlogPost.objects.filter(title__iexact=title)
        
        # Don't get validation error on instance we are changing 
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("This title has already been used")
        return title

