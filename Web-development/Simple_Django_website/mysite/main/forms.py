from django import forms 


class CreateNewList(forms.Form): 
    name = forms.CharField(label="Name:", max_length=200)
    password = forms.CharField(label="Password:", max_length=200)
    check = forms.BooleanField(label="Get free stuff? ",required=False)


