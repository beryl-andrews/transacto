from django.urls import path
from .views import (
    create_account,
    account_list,
    user_account_list,
    transaction_list,
    user_transaction_list,
    create_transaction
)

urlpatterns = [
    # admin
    path('create-account/', create_account, name='create_account'),
    path('accounts_list/', account_list, name='account_list'),
    path('transactions/', transaction_list, name='transaction_list'),
    # users
    path('my-accounts/', user_account_list, name='user_account_list'),
    path('my-transactions/', user_transaction_list, name='user_transactions_list'),
    path('transfer/', create_transaction, name='create_transaction'),
]