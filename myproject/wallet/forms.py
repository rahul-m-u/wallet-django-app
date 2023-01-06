from django import forms

from home.models import User


class InitializeWalletForm(forms.Form):
    customer_id = forms.UUIDField()

    def clean_customer_id(self):
        customer_id = self.cleaned_data['customer_id']

        try:
            user = User.objects.get(customer_id=customer_id)
            return user
        except User.DoesNotExist:
            raise forms.ValidationError('invalid customer id')


class WalletDeposit(forms.Form):
    amount = forms.IntegerField()


class WalletWithdraw(forms.Form):
    amount = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.wallet, self.active = kwargs.pop('wallet')
        forms.Form.__init__(self, *args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if not self.active:
            raise forms.ValidationError("Your wallet is disabled")

        if amount > self.wallet.balance:
            raise forms.ValidationError("You don't have enough balance")

        return amount


class DisableWallet(forms.Form):
    is_disabled = forms.BooleanField(required=True)





