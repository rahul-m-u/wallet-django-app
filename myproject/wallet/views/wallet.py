from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication

from wallet.forms import InitializeWalletForm
from wallet.forms import WalletDeposit
from wallet.forms import WalletWithdraw
from wallet.forms import DisableWallet
from wallet.models import Wallet
from wallet.models import Transaction
from wallet.views.utils import wallet_data
from wallet.views.utils import transaction_data


class WalletAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    form_class = None

    def get_form(self, request, need_wallet=False):
        args = (request.POST, request.FILES)
        kwargs = {}

        if need_wallet:
            kwargs['wallet'] = self.get_user_wallet(request)

        form = self.form_class(*args, **kwargs)

        return form

    def get_user_wallet(self, request):
        wallet = Wallet.get_user_wallet(request.user)
        return wallet, True if wallet.status == 'Enabled' else False


class InitializeWallet(WalletAPIView):
    authentication_classes = []
    permission_classes = []
    form_class = InitializeWalletForm

    def post(self, request):
        form = self.get_form(request)

        if form.is_valid():
            user = form.cleaned_data.get('customer_id')

            token, created = Token.objects.get_or_create(user=user)

            wallet, new = Wallet.objects.get_or_create(owned_by=user)

            data = {
                'token': token.key
            }

            response = {
                'status': 'success',
                'data': data,
            }

            return Response(response)

        else:
            response = {
                'status': 'fail',
                'data': {
                    'error': form.errors
                }
            }
            return Response(response)


class EnableMyWallet(WalletAPIView):
    def post(self, request):

        wallet, active = self.get_user_wallet(request)

        if not active:
            wallet.enable_wallet()

            response = {
                'status': 'success',
                'data': {
                    'wallet': wallet_data(wallet, 'Enabled')
                }
            }

        else:
            response = {
                'status': 'fail',
                'data': {
                    'error': 'Already enabled'
                }
            }

        return Response(response)


class ViewBalance(WalletAPIView):
    def get(self, request):

        wallet, active = self.get_user_wallet(request)

        if not active:
            response = {
                'status': 'fail',
                'data': {
                    'error': 'Wallet disabled'
                }
            }

        else:
            data = wallet_data(wallet, 'Enabled')

            response = {
                'status': 'success',
                'data': {
                    'wallet': data
                }
            }

        return Response(response)


class TransactionList(WalletAPIView):
    def get(self, request):
        wallet, active = self.get_user_wallet(request)

        if not active:
            response = {
                'status': 'fail',
                'data': {
                    'error': 'Wallet disabled'
                }
            }

        else:
            transaction = Transaction.objects.filter(wallet_owner_id=wallet.id)

            transactions = [transaction_data(record) for record in transaction]

            response = {
                'status': 'success',
                'data': {
                    'transactions': transactions
                }
            }

        return Response(response)


class WalletDepositAPIView(WalletAPIView):
    form_class = WalletDeposit

    def post(self, request):
        form = self.get_form(request)

        if not form.is_valid():
            response = {
                'status': 'fail',
                'data': {
                    'error': form.errors
                }
            }

        else:
            wallet, active = self.get_user_wallet(request)

            if active:
                amount = form.cleaned_data.get('amount')

                deposit = Transaction.make_deposit(wallet, amount)

                response = {
                    'status': 'success',
                    'data': {
                        'deposit': transaction_data(deposit, 'Deposit')
                    }
                }

            else:
                response = {
                    'status': 'fail',
                    'data': {
                        'error': 'Wallet disabled'
                    }
                }

        return Response(response)


class WalletWithdrawAPIView(WalletAPIView):
    form_class = WalletWithdraw

    def post(self, request):
        form = self.get_form(request, need_wallet=True)

        if not form.is_valid():
            response = {
                'status': 'fail',
                'data': {
                    'error': form.errors
                }
            }

        else:
            wallet, active = self.get_user_wallet(request)

            if active:
                amount = form.cleaned_data.get('amount')

                withdraw = Transaction.make_withdrawal(wallet, amount)

                response = {
                    'status': 'success',
                    'data': {
                        'withdrawal': transaction_data(withdraw, 'Withdrawal')
                    }
                }

            else:
                response = {
                    'status': 'fail',
                    'data': {
                        'error': 'Wallet disabled'
                    }
                }

        return Response(response)


class DisableMyWallet(WalletAPIView):
    form_class = DisableWallet

    def patch(self, request):
        form = self.get_form(request)

        if not form.is_valid():
            response = {
                'status': 'fail',
                'data': {
                    'error': form.errors
                }
            }
            return Response(response)

        wallet, active = self.get_user_wallet(request)

        if active:
            wallet.disable_wallet()

            response = {
                'status': 'success',
                'data': {
                    'wallet': wallet_data(wallet, 'Disabled')
                }
            }

        else:
            response = {
                'status': 'fail',
                'data': {
                    'error': 'Already disabled'
                }
            }

        return Response(response)



