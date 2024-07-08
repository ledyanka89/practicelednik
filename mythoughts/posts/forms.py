from django import forms
from .models import Posts, Comments
class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'body']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']