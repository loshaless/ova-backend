from sqlalchemy.orm import Session
from app.models.transaction_model import TransactionModel

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_transaction(self, transaction: TransactionModel):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_transactions_by_account(self, account_id: int):
        return self.db.query(TransactionModel).filter(
            (TransactionModel.sender_account_id == account_id) |
            (TransactionModel.receiver_account_id == account_id)
        ).order_by(TransactionModel.transaction_time.desc()).all()

    def update_transaction_category(self, transaction_id: int, category_main_id: int, category_sub_id: int):
        transaction = self.db.query(TransactionModel).filter(TransactionModel.transaction_id == transaction_id).first()
        if transaction:
            transaction.category_main_id = category_main_id
            transaction.category_sub_id = category_sub_id
            self.db.commit()
            self.db.refresh(transaction)
        return transaction
