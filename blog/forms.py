# blog/forms.py
from blog.models import CustomUser, Comment
from django import forms


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age', 'password')


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=25)
    email = forms.EmailField(label='Email Address')
    contact_number = forms.IntegerField(label='Contact Number', required=False)
    location = forms.CharField(max_length=20, required=False)
    short_message = forms.CharField(label='Message', max_length=100, required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post', 'body',)