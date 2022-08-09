from django import forms


class AuthForm(forms.Form):

    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
        'class': 'fadeIn second',
        'placeholder': 'username'
        }
    ))

    password = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'fadeIn third',
               'placeholder': 'password'
               }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'username'})


class UserRegisterForm(forms.Form):

    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    user_id = forms.CharField(max_length=15)
