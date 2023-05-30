from django import forms
from django.conf import settings
from .models import Rating, RatingStar, Review
from src.profiles.models import UserNet

class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""

    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ("star",)
    
class ReviewForm(forms.ModelForm):
    """Форма добавления отзыва"""
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # author = forms.CharField(widget=forms.Textarea(attrs={'class': 'hidden',}), required=False),
    # text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your review'}), required=False),
    class Meta:
        model = Review
        fields = ('text',)