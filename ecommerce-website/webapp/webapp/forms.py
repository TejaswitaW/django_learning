"""This is forms module, it creats forms for our web application"""
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    """This class is design of contact form."""
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control",
               "id": "form_full_name",
               "placeholder": "Your Full Name"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control",
               "placeholder": "Your Full Email-ID"}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Your Message"}))

    def clean_email(self):
        """This function does email validation"""
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email


class LoginForm(forms.Form):
    """This class is design of login form."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """This class is design of register form."""
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)

    def clean_username(self):
        """Checks duplicate username"""
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is already taken")
        else:
            return username

    def clean_email(self):
        """Checks duplicate Email ID"""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email ID is already taken")
        else:
            return email

    def clean(self):
        """This function does password validation"""
        # it is a dictionary
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError("Passwords must match")
        return data
