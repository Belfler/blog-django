from django import forms
from django.core.mail import send_mail


class FeedBackForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'autocomplete': 'off'}), label='Your Name:')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off'}), label='Your Email:')
    message = forms.CharField(min_length=100, widget=forms.Textarea, label='Message (min 100 characters):')

    def print_in_console(self):
        data = self.cleaned_data
        print(f'\n{data["name"]} ({data["email"]}) left feedback:\n{data["message"]}\n')
