from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms 
from store.models import Profile

class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = None
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username","email"]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Add Bootstrap class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 100%;'
            field.label = ""
        # placehoder the fields with suitable vals
        self.fields["first_name"].widget.attrs["placeholder"] = "Your First name..."
        self.fields["last_name"].widget.attrs["placeholder"] = "Your Last name..."
        self.fields["username"].widget.attrs["placeholder"] = "Enter a sername..."
        self.fields["email"].widget.attrs["placeholder"] = "Enter an Email..."
        # focus on first name   
        self.fields['first_name'].widget.attrs['autofocus'] = True


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username","email","password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 100%;'
            field.label = ""

        self.fields["first_name"].widget.attrs["placeholder"] = "Your First name..."
        self.fields["last_name"].widget.attrs["placeholder"] = "Your Last name..."
        self.fields["username"].widget.attrs["placeholder"] = "Enter a sername..."
        self.fields["email"].widget.attrs["placeholder"] = "Enter an Email..."
        self.fields["password1"].widget.attrs["placeholder"] = "Enter a Password..."
        self.fields["password2"].widget.attrs["placeholder"] = "confirm Your Password..."

        
        self.fields['first_name'].widget.attrs['autofocus'] = True

class UpdatePasswordForm(SetPasswordForm):

    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]
    
    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        # Add Bootstrap class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 100%;'
            field.label = ""
        # placehoder the fields with suitable vals
        self.fields["new_password1"].widget.attrs["placeholder"] = "Enter New Password..."
        self.fields["new_password2"].widget.attrs["placeholder"] = "confirm Your New Password..."

        # focus on first name   
        self.fields['new_password1'].widget.attrs['autofocus'] = True

class UpdateInfoForm(forms.ModelForm):
    phone = forms.CharField( label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Phone"}), required=False)
    address_1 = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Address 1"}), required=False)
    address_2 = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Address 2"}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "City"}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "State"}), required=False)
    zip_code = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "ZipCode"}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Country"}), required=False)

    class Meta:
        model =  Profile
        fields = ["phone", 'address_1', "address_2", "city", "state", "zip_code", "country"]