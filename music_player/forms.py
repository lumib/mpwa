from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms

from .models import AuthUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = AuthUser
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            AuthUser._default_manager.get(username=username)
        except AuthUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text='''Raw passwords are not stored, so there is no way to see this
                                         user's password, but you can change the password using <a href=\"password/\">
                                         this form</a>.''')

    class Meta(UserChangeForm.Meta):
        model = AuthUser
        fields = ("username",
                  "password",
                  "is_active",
                  "is_staff",
                  "is_superuser",
                  "user_permissions")

    def clean_password(self):
        return self.initial['password']
