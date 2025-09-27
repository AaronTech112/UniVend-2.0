# UnivendApp/forms.py
from django import forms
from .models import Listing, CustomUser, Category, Department, Campus, KYC, Message

class ListingForm(forms.ModelForm):
    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixed Price'),
        ('negotiable', 'Negotiable'),
        ('hourly', 'Per Hour'),
        ('free', 'Free')
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like-new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair')
    ]

    listing_type = forms.CharField(required=True)
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter a clear, descriptive title'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, min_value=0)
    price_type = forms.ChoiceField(choices=PRICE_TYPE_CHOICES, required=True)
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your listing in detail...'}), required=True)
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Add tags (comma-separated)'}))
    location = forms.CharField(required=True)
    meeting_preferences = forms.MultipleChoiceField(
        choices=[
            ('in-person', 'In-person'),
            ('virtual', 'Virtual')
        ],
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    availability = forms.CharField(required=False)  # This will be handled by the frontend calendar/time picker

    class Meta:
        model = Listing
        fields = ['listing_type', 'title', 'category', 'price', 'price_type', 'condition',
                  'description', 'tags', 'location', 'meeting_preferences', 'availability']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            return ','.join([tag.strip() for tag in tags.split(',') if tag.strip()])
        return ''

    def clean(self):
        cleaned_data = super().clean()
        listing_type = cleaned_data.get('listing_type')
        condition = cleaned_data.get('condition')
        category = cleaned_data.get('category')

        if listing_type not in ['product', 'service']:
            raise forms.ValidationError('Invalid listing type')

        # Only validate condition for products
        if listing_type == 'product' and not condition:
            raise forms.ValidationError('Condition is required for products')

        # Validate category matches listing type
        if category and listing_type:
            if listing_type == 'product' and not category.is_product:
                raise forms.ValidationError('Selected category is not valid for products')
            elif listing_type == 'service' and category.is_product:
                raise forms.ValidationError('Selected category is not valid for services')

        return cleaned_data

class KYCForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = KYC
        fields = ['student_id', 'interests']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from view
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        kyc = super().save(commit=False)
        kyc.user = self.user
        if commit:
            kyc.save()
            self.save_m2m()  # Save ManyToMany fields (interests)
            # Update CustomUser fields
            self.user.department = self.cleaned_data['department']
            self.user.phone_number = self.cleaned_data['phone_number']
            if self.cleaned_data['profile_picture']:
                self.user.profile_picture = self.cleaned_data['profile_picture']
            self.user.save()
        return kyc

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=40, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'bio', 'profile_picture', 'campus', 'department', 'show_phone', 'email_notifications']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}"
        self.fields['campus'].queryset = Campus.objects.all()
        self.fields['department'].queryset = Department.objects.all()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image']