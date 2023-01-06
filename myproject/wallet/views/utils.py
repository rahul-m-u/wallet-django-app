

def wallet_data(record, status=None):
    data = {
        'id': record.id,
        'owned_by': record.owned_by.customer_id,
        'balance': record.balance,
        'status': record.status,


        'created_at': record.created_at,
    }

    if status == 'Enabled':
        data.update({'enabled_at': record.enabled_at})

    elif status == 'Disabled':
        data.update({'disabled_at': record.disabled_at})

    else:
        data.update({
            'enabled_at': record.enabled_at,
            'disabled_at': record.disabled_at
        })

    return data


def transaction_data(record, status=None):
    data = {
        'transaction_id': record.transaction_id,
        'status': record.status,
        'transacted_at': record.transacted_at,
        'transaction_type': record.transaction_type,
        'amount': record.amount,
        'reference_id': record.reference_id,
    }

    if status == 'Deposit':
        data.update({
            'deposited_by': record.deposited_by.customer_id,
            'deposited_at': record.deposited_at
        })

    if status == 'Withdrawal':
        data.update({
            'withdrawn_by': record.withdrawn_by.customer_id,
            'withdrawn_at': record.withdrawn_at,
        })

    # else:
    #     data.update({
    #         'deposited_by': record.deposited_by,
    #         'deposited_at': record.deposited_at,
    #         'withdrawn_by': record.withdrawn_by,
    #         'withdrawn_at': record.withdrawn_at,
    #     })

    return data





