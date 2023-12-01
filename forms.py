from django import forms
from django.contrib.auth.models import User
from .models import Room, Review,  Agent, RealEstateAgent, HouseData
#from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Reset

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter first name',
        'class': 'form-control'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter last name',
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter username',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email',
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Enter password',
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Repeat password',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('password1'),
            Field('password2'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary'),
                Reset('reset', 'Reset', css_class='btn btn-secondary')
            )
        )

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter username',
        'class': 'form-control',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        'class': 'form-control',
    }))


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'image', 'social_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'social_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['created_at', 'is_booked','created_by']

        widgets = {
            'house': forms.Select(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amenities': forms.CheckboxSelectMultiple(),
            'cover_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'video': forms.FileInput(attrs={'class': 'form-control-file'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'proximal_services': forms.CheckboxSelectMultiple(),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathroom': forms.NumberInput(attrs={'class': 'form-control'}),  # Corrected field name
            'bedroom': forms.NumberInput(attrs={'class': 'form-control'}),   # Corrected field name
            'latitude': forms.HiddenInput(attrs={'class': 'form-control', 'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'class': 'form-control', 'id': 'id_longitude'}),
        }



class RatingForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'




class AgentRequestForm(forms.ModelForm):
    class Meta:
        model = RealEstateAgent
        fields = [
            'full_name',
            'contact_number',
            'email',
            'address',
            'years_of_experience',
            'license_number',
            'previous_companies',
            'additional_skills',
            'references',
        ]
        widgets = {
            'references': forms.Textarea(attrs={'rows': 3}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
        }

        # Add Bootstrap classes to the form elements
        def __init__(self, *args, **kwargs):
            super(AgentRequestForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'description']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'description': forms.Textarea()
        }

class EditReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['rating', 'description']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'description': forms.Textarea()
        }



class HouseDataForm(forms.ModelForm):
    class Meta:
        model = HouseData
        exclude = ['id']

        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'stories': forms.NumberInput(attrs={'class': 'form-control'}),
            'mainroad': forms.NumberInput(attrs={'class': 'form-control'}),
            'guestroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'basement': forms.NumberInput(attrs={'class': 'form-control'}),
            'hotwaterheating': forms.NumberInput(attrs={'class': 'form-control'}),
            'airconditioning': forms.NumberInput(attrs={'class': 'form-control'}),
            'parking': forms.NumberInput(attrs={'class': 'form-control'}),
        }
