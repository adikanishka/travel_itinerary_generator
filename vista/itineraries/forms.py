from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comments', 'rating']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your feedback here...'}),
            'rating': forms.Select(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')])
            }