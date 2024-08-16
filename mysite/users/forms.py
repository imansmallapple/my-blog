from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=32,widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': 'Username/Email'
    }))
    password = forms.CharField(label='password', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'Password'
    }))

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username == password:
            raise forms.ValidationError("Username can't same as password!")
        return password


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='email', max_length=32, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': 'Username/Email'
    }))
    password = forms.CharField(label='password', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'Password'
    }))
    repeat = forms.CharField(label='repeat', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'Type Password Again'
    }))

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("User already exists!")
        return email

    def clean_repeat(self):
        if self.cleaned_data['password'] != self.cleaned_data['repeat']:
            raise forms.ValidationError("Passwords not same!")
        return self.cleaned_data['password']


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(
        label='email', max_length=32, widget=forms.EmailInput(attrs={
            'class': 'input', 'placeholder': 'Username/Email'
    })
    )


class ModifyPwdForm(forms.Form):
    password = forms.CharField(label='enter new password', min_length=6,
        widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'Enter the password'}))
