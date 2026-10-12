from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit: Profile.objects.get_or_create(user=user)
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','avatar_url']
        widgets = {'bio': forms.Textarea(attrs={'rows':3,'placeholder':'A little about you...'}), 'avatar_url': forms.URLInput(attrs={'placeholder':'https://example.com/avatar.jpg'})}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text','image_url']
        widgets = {'text': forms.Textarea(attrs={'rows':3,'placeholder':"What's on your mind?",'maxlength':2000}), 'image_url': forms.URLInput(attrs={'placeholder':'Optional image URL'})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
