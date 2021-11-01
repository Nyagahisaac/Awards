from django.contrib.auth.models import User
from django import forms
from .models import Project_Post,Reviews,Profile




class SignUpForm(User):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )



class ReveiwForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude=[
            'posted_by',
            'posted_on',
            'project_id',
        ]

class Post_projectform(forms.ModelForm):
    class Meta:
        model = Project_Post
        exclude=[
            'posted_by',
            'updated_on',
        ]

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = [
            'updated_on',
            'user',
        ]
class UserUpdateform(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]   