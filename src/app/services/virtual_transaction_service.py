from fastapi import HTTPException
from datetime import timedelta
import random

from app.database.repositories.virtual_transaction_repository import VirtualTransactionRepository
from app.database.repositories.user_repository import UserRepository
from app.database.repositories.account_repository import AccountRepository
from app.models.transaction_model import TransactionModel
from app.schemas.virtual_transaction_schema import VirtualTransactionCreate


class VirtualTransactionService:
    def __init__(
        self,
        account_repository: AccountRepository,
        user_repository: UserRepository,
        virtual_transaction_repository: VirtualTransactionRepository
    ):
        self.account_repo = account_repository
        self.user_repo = user_repository
        self.transaction_repo = virtual_transaction_repository

    def create_virtual_transactions(self, request: VirtualTransactionCreate):
        sender_account = self.account_repo.get_account_by_account_id(request.sender_account_id)
        if not sender_account:
            raise HTTPException(status_code=404, detail="Sender account not found")

        sender_user = self.user_repo.get_user_by_id(sender_account.user_id)
        if not sender_user:
            raise HTTPException(status_code=404, detail="Sender user not found")

        transactions = []
        current_date = request.start_date

        while current_date <= request.end_date:
            receiver_account_id = random.choice(request.receiver_account_ids)
            receiver_account = self.account_repo.get_account_by_account_id(receiver_account_id)

            if not receiver_account:
                continue

            receiver_user = self.user_repo.get_user_by_id(receiver_account.user_id)
            if not receiver_user:
                continue

            amount = VirtualTransactionCreate.random_amount(request.min_amount, request.max_amount)
            reference_number = VirtualTransactionCreate.generate_reference_number()

            location = random.choice(request.location) if request.location else "Jakarta"
            message = random.choice(request.dummy_messages) if request.dummy_messages else "Dummy Transaction"

            transaction = TransactionModel(
                reference_number=reference_number,
                sender_account_id=sender_account.account_id,
                receiver_account_id=receiver_account.account_id,
                amount=amount,
                currency=request.currency,
                transaction_time=current_date + timedelta(hours=random.randint(8, 20)),  # Random jam transaksi
                message=message,
                transaction_type="VIRTUAL_TRANSFER",
                sender_name=sender_user.full_name,
                receiver_name=receiver_user.full_name,
                receiver_location=location
            )

            self.transaction_repo.save_transaction(transaction)
            transactions.append(transaction)

            current_date += timedelta(days=random.randint(1, 5))  # Simulasi transaksi terjadi dalam selang waktu

        return transactions
