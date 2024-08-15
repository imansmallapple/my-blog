from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=15,widget=forms.TextInput(attrs={
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
