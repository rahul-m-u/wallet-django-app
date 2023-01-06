from django.contrib import admin

from wallet.models import Wallet
from wallet.models import Transaction

admin.site.register(Wallet)
admin.site.register(Transaction)
