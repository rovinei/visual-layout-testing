from django import forms
from ..models import Employee, Customer
from django.core.validators import EmailValidator


class RegistrationForm(forms.ModelForm):

    """
    HTML form for user registration
    """

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'uk-input custom-text-input', 'placeholder': 'Enter a valid email'}),
        validators=[EmailValidator],
        label="Email",
        help_text="Enter your registered email from any provider.",
        error_messages={
            'unique': 'email must a unique in entire application.',
            'required': 'email is required and cannot be blank.',
            'invalid': 'email must be a valid email address.'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'uk-input custom-password-input'}),
        label="Password",
        help_text="password must contain letters, special characters and at least 1 digit.",
        error_messages={
            'required': 'password cannot be blank and not a weak password.'
        }
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Password (Re-type)",
        error_messages={
            'mismatch': 'confirmation password does not matched.'
        }
    )

    class Meta:
        model = Customer
        fields = ('email',)

    def clean(self):
        super(RegistrationForm, self).clean()
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError("Password doesn't match!")
            return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class AccountInformationForm(forms.ModelForm):

    """
    HTML form for customer filling information
    """

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'uk-input custom-text-input', 'placeholder': 'First name'}),
        label="First name",
        help_text="Enter your first name"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'uk-input custom-text-input', 'placeholder': 'Last name'}),
        label="Last name",
        help_text="Enter your last name"
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'uk-input custom-text-input', 'placeholder': 'Username'}),
        label="Username",
        help_text="Enter your username"
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'uk-input custom-date-input date_of_birth',
            }
        ),
        label="Date of birth",
        help_text="Type your date of birth"
    )
    contact_number = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'uk-input custom-text-input phone_number',
                'placeholder': 'Enter your contact phone number'}
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'uk-input custom-text-input address'
        }),
        label="Current address",
        help_text="Enter your current living address."
    )
    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'uk-input custom-text-input',
                'placeholder': 'Enter your living state'
            }
        ),
        label="State",
        help_text="Enter your current living state"
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'uk-input custom-text-input city',
                'placeholder': 'Enter your current city'
            }
        ),
        label="City",
        help_text="Enter your current city"
    )
    country = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': 'uk-input custom-select-input'
            }
        ),
        label="Country",
        help_text="Select your origin/country"
    )

