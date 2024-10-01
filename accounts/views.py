from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AccountCreationForm, TransactionCreationForm
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from decimal import Decimal


from .utils import get_exchange_rates


@login_required
def create_account(request):
    if request.user.user_type != 'admin':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            address = form.cleaned_data['address']

            account = Account.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                address=address,
                balance=10000,
                currency="USD"
            )
            account.save()
            messages.success(request, "Account created successfully!")
            return redirect('create_account')
    else:
        form = AccountCreationForm()

    return render(request, 'create_account.html', {'form': form})


@login_required
def account_list(request):
    if request.user.user_type != 'admin':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    accounts = Account.objects.all()

    return render(request, 'account_list.html', {'accounts': accounts})


@login_required
def user_account_list(request):
    if request.user.user_type == 'user':
        accounts = Account.objects.filter(user=request.user)
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    return render(request, 'user_account_list.html', {'accounts': accounts})


@login_required
def transaction_list(request):
    if request.user.user_type != 'admin':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    transaction_type = request.GET.get('type', '')

    if transaction_type in ['deposit', 'withdrawal']:
        transactions = Transaction.objects.filter(transaction_type=transaction_type)
    else:
        transactions = Transaction.objects.all()

    return render(request, 'transaction_list.html', {'transactions': transactions})


@login_required
def user_transaction_list(request):
    if request.user.user_type == 'user':
        user_accounts = Account.objects.filter(user=request.user)

        transactions = Transaction.objects.filter(
            Q(to_acc__in=user_accounts, transaction_type='deposit') |
            Q(from_acc__in=user_accounts, transaction_type='withdrawal')
        )
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    return render(request, 'user_transaction_list.html', {'transactions': transactions})


@login_required
def create_transaction(request):
    if request.user.user_type != 'user':
        messages.error(request, "Only regular users can create transactions.")
        return redirect('home')

    if request.method == 'POST':
        form = TransactionCreationForm(request.POST, user=request.user)
        print(form.is_valid())

        if form.is_valid():
            currency = form.cleaned_data['currency']
            amount = form.cleaned_data['amount']
            usd_amount = form.cleaned_data['amount']
            if currency != "USD":
                try:
                    rates = get_exchange_rates(base_currency="USD")
                    usd_amount = Decimal(amount) / Decimal(rates["conversion_rates"][currency])
                except Exception as e:
                    messages.error(request, f"Error fetching exchange rates: {str(e)}")
                    return render(request, 'create_transaction.html', {'form': form})


            transaction = form.save(commit=False)
            sender_account = form.cleaned_data['from_account']
            if sender_account.balance < usd_amount:
                messages.error(request, "Insufficient funds in your account.")
                return render(request, 'create_transaction.html', {'form': form})

            if usd_amount < 0:
                messages.error(request, "Invalid Funds Entered")
                return render(request, 'create_transaction.html', {'form': form})

            try:
                withdrawal_transaction = Transaction(
                    from_acc_id=str(form.cleaned_data['from_account'].UAN),
                    to_acc_id=form.cleaned_data['recipient_account'],
                    currency=form.cleaned_data['currency'].upper(),
                    amount=amount,
                    transaction_type='withdrawal',
                    description=form.cleaned_data['description'],
                )
                withdrawal_transaction.save()

                # update reciever balance
                sender_account.balance -= usd_amount
                sender_account.save()

            except Account.DoesNotExist:
                messages.error(request, "Error creating transaction: withdrawal")
                return render(request, 'create_transaction.html', {'form': form})



            # deposit transaction
            try:
                recipient_account = Account.objects.get(UAN=form.cleaned_data['recipient_account'])
                deposit_transaction = Transaction(
                    from_acc_id=str(form.cleaned_data['from_account'].UAN),
                    to_acc_id=form.cleaned_data['recipient_account'],
                    currency=form.cleaned_data['currency'].upper(),
                    amount=amount,
                    transaction_type='deposit',
                    description=form.cleaned_data['description'],
                )
                deposit_transaction.save()

                # update reciever balance
                recipient_account.balance += usd_amount
                recipient_account.save()

            except Account.DoesNotExist:
                messages.error(request, "Error creating transaction: deposit")
                return render(request, 'create_transaction.html', {'form': form})




            messages.success(request, "Transaction created successfully!")
            return redirect('create_transaction')
    else:
        form = TransactionCreationForm(user=request.user)

    return render(request, 'create_transaction.html', {'form': form})