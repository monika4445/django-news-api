from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'tags': forms.SelectMultiple(attrs={'size': 5})  # Set the size attribute to show multiple options
        }
