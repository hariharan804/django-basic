from django import forms


class UserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    age = forms.IntegerField()
    profile_verified = forms.BooleanField(required=False)
    mobile_number = forms.CharField(max_length=25)

