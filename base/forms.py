from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={
            'placeholder': 'Tweet something...',
            'class': 'textarea is-success is-medium',
        }
    ), label="", 
    )

    class Meta:
        model = Tweet
        exclude = ('user',)