from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.transaction_model import TransactionModel
from app.schemas.transaction_schema import TransferRequest, TransactionCreate
from app.database.repositories.user_repository import UserRepository
from app.database.repositories.account_repository import AccountRepository
from app.database.repositories.transaction_repository import TransactionRepository

class TransactionService:
    def __init__(self, account_repository: AccountRepository, transaction_repository: TransactionRepository, user_repository: UserRepository):
        self.user_repo = user_repository
        self.account_repo =account_repository
        self.transaction_repo = transaction_repository

    def transfer_money(self, transfer_request: TransferRequest):
        # Get sender account
        sender_account = self.account_repo.get_account_by_number_with_for_update(transfer_request.sender_account_number)
        if not sender_account:
            raise HTTPException(status_code=404, detail="Sender account not found")

        # Get receiver account
        receiver_account = self.account_repo.get_account_by_number_with_for_update(transfer_request.receiver_account_number)
        if not receiver_account:
            raise HTTPException(status_code=404, detail="Receiver account not found")

        # Get sender's user to verify PIN
        sender_user = self.user_repo.get_user_by_id(sender_account.user_id)
        if not sender_user:
            raise HTTPException(status_code=404, detail="Sender user not found")

        # Verify PIN
        if sender_user.pin != transfer_request.pin:
            raise HTTPException(status_code=401, detail="Invalid PIN")

        # Check if sender has enough balance
        if sender_account.balance < transfer_request.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Check if account is active
        if sender_account.status != "ACTIVE" or receiver_account.status != "ACTIVE":
            raise HTTPException(status_code=400, detail="Account not active")

        reference_number = TransactionCreate.generate_reference_number()

        sender_name = sender_user.full_name
        receiver_name = self.user_repo.get_user_by_id(receiver_account.user_id).full_name

        transaction = TransactionModel(
            reference_number=reference_number,
            sender_account_id=sender_account.account_id,
            receiver_account_id=receiver_account.account_id,
            amount=transfer_request.amount,
            message=transfer_request.message,
            transaction_type="transfer via Octo Pay",
            sender_name=sender_name,
            receiver_name=receiver_name,
        )

        sender_account.balance -= transfer_request.amount
        receiver_account.balance += transfer_request.amount

        return self.transaction_repo.save_transaction(transaction)

    def get_account_transactions(self, account_id: int):
        return self.transaction_repo.get_transactions_by_account(account_id)

    def update_transaction_category(self, transaction_id: int, category_main_id: int, category_sub_id: int):
        transaction = self.transaction_repo.update_transaction_category(transaction_id, category_main_id, category_sub_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
