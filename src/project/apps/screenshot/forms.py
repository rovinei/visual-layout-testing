from django import forms
from .data.form_field_tuples import (MAC_RESOLUTION_SCREEN, WINDOW_RESOLUTION_SCREEN, SCREENSHOT_QUALITY)
from django.utils.translation import ugettext_lazy as _


class ScreenshotAPIForm(forms.Form):
    page_url = forms.URLField(
        widget=forms.TextInput(attrs={'class': 'uk-input custom-text-input', 'placeholder': 'Enter or paste URL here'}),
        label='Page URL',
        required=True,
        help_text='Web page url that need to take screenshot.'
    )
    mac_res = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'uk-select custom-select-input'}),
        label='OSX Resolution',
        help_text='MAC OSX browser responsive screen to take screenshot.',
        choices=MAC_RESOLUTION_SCREEN,
        initial='1149x768'
    )
    win_res = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'uk-select custom-select-input'}),
        label='Windows Resolution',
        help_text='Windows browser responsive screen to take screenshot.',
        choices=WINDOW_RESOLUTION_SCREEN,
        initial='1149x768'
    )
    screenshot_quality = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'uk-select custom-select-input'}),
        label=_('Screenshot Quality'),
        help_text=_('Whether to compressed or keep original quality of images.'),
        choices=SCREENSHOT_QUALITY,
        initial='original'
    )


