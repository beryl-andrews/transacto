from django import forms
from django.contrib.auth import get_user_model
from .models import Account, Transaction

User = get_user_model()


class AccountCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='user'),
        label="Select User",
        empty_label="Choose a user",
    )
    first_name = forms.CharField(max_length=255, label="First Name")
    last_name = forms.CharField(max_length=255, label="Last Name")
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={
            'type': 'date'
        })
    )
    address = forms.CharField(max_length=255, label="Address")

    class Meta:
        model = Account
        fields = ['user', 'first_name', 'last_name', 'date_of_birth', 'address']


class TransactionCreationForm(forms.ModelForm):
    from_account = forms.ModelChoiceField(queryset=Account.objects.none(), label="Sender Account")
    recipient_account = forms.CharField(label="Recipient Account")
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea, required=False, label="Transaction Description")
    currency = forms.ChoiceField(choices=[('USD', 'USD'), ('GBP', 'GBP'), ('EUR', 'EUR')], label="Currency")

    class Meta:
        model = Transaction
        fields = ['from_account', 'recipient_account', 'amount', 'description', 'currency']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionCreationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['from_account'].queryset = Account.objects.filter(user=user)