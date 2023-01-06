# Wallet Django App

## Project Setup
```
1. Create a virtualenviroment
2. Activate the virtualenviroment
3. Install the packages from requirement.txt
```

## DB
```
1. Migrate the DB By giving "python manage.py migrate"
```

## Create User
```
1. Use command "python manage.py createsuperuser: to create a user
```

## Run Project
```
1. Use command "python manage.py runserver" to run the project
```

## URLS
```
1. Login and get Customer ID
    url : http://127.0.0.1:8000/home/login/

2. Initialize my account for wallet
    url : http://127.0.0.1:8000/wallet/initialize/wallet/

3. Enable my wallet
    url : http://127.0.0.1:8000/wallet/enable/my-wallet/

4. View my wallet balance
    url : http://127.0.0.1:8000/wallet/my-wallet/view-balance/

5. View my wallet transactions
    url : http://127.0.0.1:8000/wallet/my-wallet/transactions/

6. Add virtual money to my wallet
    url : http://127.0.0.1:8000/wallet/my-wallet/deposit/

7. Use virtual money from my wallet
    url : http://127.0.0.1:8000/wallet/my-wallet/withdrawal/

8. Disable my wallet
    url : http://127.0.0.1:8000/wallet/disable/my-wallet/
```



