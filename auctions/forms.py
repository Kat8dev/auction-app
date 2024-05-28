# forms.py
from django import forms
from .models import AuctionListing, Category, Bid

class ListingForms(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'category'}),
        required=False  
    )

    class Meta:
        model = AuctionListing
        fields = ['title', 'desc', 'starting_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'desc': 'Description',
            'starting_bid': 'Starting Bid',
            'image_url': 'Image URL',
            'category': 'Category'
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'bid': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'bid': 'Place a bid',
        }
        
        
class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment'}),
        label=''
    )        