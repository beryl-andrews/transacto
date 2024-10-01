from django.db import models
from uuid import uuid4


class Account(models.Model):
    UAN = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    balance = models.IntegerField(default=10000)
    currency = models.CharField(max_length=3, default='USD')


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('withdrawal', 'Withdrawal'),
        ('deposit', 'Deposit'),
        ('transfer', 'Transfer'),
    ]

    id = models.AutoField(primary_key=True)
    from_acc = models.ForeignKey('accounts.Account', related_name='transactions_made', on_delete=models.CASCADE)
    to_acc = models.ForeignKey('accounts.Account', related_name='transactions_received', on_delete=models.CASCADE)
    amount = models.FloatField()
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    transaction_id = models.UUIDField(default=uuid4, editable=False)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

