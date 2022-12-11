from django import forms
from .models import Article


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Article
        fields = ('username','description', 'picture')