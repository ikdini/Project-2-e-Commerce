from django import forms


# It creates a form with a title, description, starting bid, image, and category
class CreateListing(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={"class": "form-control", "aria-describedby": "passwordHelpBlock"}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control", "aria-describedby": "passwordHelpBlock"}))
    starting_bid = forms.IntegerField(min_value=0, max_value=9999999, widget=forms.NumberInput(
        attrs={'class': 'form-control', "aria-describedby": "passwordHelpInline"}))
    image = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control'}))
    category = forms.CharField(required=False, max_length=64, widget=forms.TextInput(
        attrs={"class": "form-control"}))
