from django.urls import path

from wallet.views import InitializeWallet
from wallet.views import EnableMyWallet
from wallet.views import ViewBalance
from wallet.views import TransactionList
from wallet.views import WalletDepositAPIView
from wallet.views import WalletWithdrawAPIView
from wallet.views import DisableMyWallet


urlpatterns = [
    path('initialize/wallet/', InitializeWallet.as_view(), name='initialize-wallet'),
    path('enable/my-wallet/', EnableMyWallet.as_view(), name='enable-my-wallet'),

    path('my-wallet/view-balance/', ViewBalance.as_view(), name='my-wallet-view-balance'),
    path('my-wallet/transactions/', TransactionList.as_view(), name='my-wallet-transactions'),
    path('my-wallet/deposit/', WalletDepositAPIView.as_view(), name='my-wallet-deposit'),
    path('my-wallet/withdrawal/', WalletWithdrawAPIView.as_view(), name='my-wallet-withdrawal'),

    path('disable/my-wallet/', DisableMyWallet.as_view(), name='disable-my-wallet'),
]
