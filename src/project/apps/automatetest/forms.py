from django import forms
from .models import (Project)
from django.utils.translation import gettext_lazy as _

class ProjectCreationForm(forms.ModelForm):
    """
    Model creation form for project
    """
    class Meta:
        model = Project
        fields = ('project_name', 'description')




class ProjectSelectionForm(forms.Form):
    screenshot_quality = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'uk-select custom-select-input'}),
        label=_('Screenshot Quality'),
        help_text=_('Whether to compressed or keep original quality of images.'),
        initial='original'
    )
