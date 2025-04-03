from sqlalchemy.orm import Session
from app.models.transaction_model import TransactionModel


class VirtualTransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_transaction(self, transaction: TransactionModel):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
