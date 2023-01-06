import uuid
import datetime
from django.db import models
from home.models import User


WalletStatus = (
    ('Enabled', 'Enabled'),
    ('Disabled', 'Disabled')
)

TransactionType = (
    ('Deposit', 'Deposit'),
    ('Withdrawal', 'Withdrawal'),
    ('Transfer', 'Transfer'),
)

TransactionStatus = (
    ('Success', 'Success'),
    ('Failed', 'Failed'),
)


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    status = models.CharField(max_length=45, choices=WalletStatus, default='Initialized')

    enabled_at = models.DateTimeField(blank=True, null=True)
    disabled_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_user_wallet(cls, user):
        return cls.objects.get(owned_by_id=user.id)

    def enable_wallet(self):
        self.status = 'Enabled'
        self.enabled_at = datetime.datetime.now()
        self.save()
        return self

    def disable_wallet(self):
        self.status = 'Disabled'
        self.disabled_at = datetime.datetime.now()
        self.save()
        return self


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_type = models.CharField(max_length=45, choices=TransactionType, default='')

    wallet_owner = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    amount = models.IntegerField(default=0)

    status = models.CharField(max_length=45, choices=TransactionStatus, default='Initialized')

    reference_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    deposited_by = models.ForeignKey(User, related_name='deposited_user', on_delete=models.CASCADE, null=True)
    deposited_at = models.DateTimeField(blank=True, null=True)

    withdrawn_by = models.ForeignKey(User, related_name='withdrawn_user', on_delete=models.CASCADE, null=True)
    withdrawn_at = models.DateTimeField(blank=True, null=True)

    transacted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.wallet_owner)

    @classmethod
    def make_deposit(cls, wallet, amount):
        obj = cls()
        obj.transaction_type = 'Deposit'
        obj.wallet_owner_id = wallet.id
        obj.amount = amount
        obj.status = 'Success'
        obj.deposited_by_id = wallet.owned_by.id
        obj.deposited_at = datetime.datetime.now()
        obj.save()

        return obj

    @classmethod
    def make_withdrawal(cls, wallet, amount):
        obj = cls()
        obj.transaction_type = 'Withdrawal'
        obj.wallet_owner_id = wallet.id
        obj.amount = amount
        obj.status = 'Success'
        obj.withdrawn_by_id = wallet.owned_by.id
        obj.withdrawn_at = datetime.datetime.now()
        obj.save()

        return obj

    def update_wallet(self):
        if self.transaction_type == 'Deposit':
            wallet = self.wallet_owner
            balance = wallet.balance + self.amount
            wallet.balance = balance
            wallet.save()

        if self.transaction_type == 'Withdrawal':
            wallet = self.wallet_owner
            balance = wallet.balance - self.amount
            wallet.balance = balance
            wallet.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.update_wallet()
        models.Model.save(self, force_insert=False, force_update=False, using=None, update_fields=None)



