from django import forms
from .models import Listing, Category


class ListingForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Enter Your Title'}),
                            required=True, max_length=100)

    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Enter Your Description'}),
                                  required=True, max_length=1000)

    price = forms.CharField(label='Price', widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Enter Your Price'}),
                            required=True, max_length=200)

    imageurl = forms.URLField(label='Image URL', widget=forms.URLInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Enter Image Url'}),
                              max_length=200)

    # category = forms.CharField(label='Category', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'imageurl', 'category']
