from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from decimal import Decimal

from app.database.connection import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransferRequest, CategoryUpdate

router = APIRouter(
    prefix="/transactions",
)

@router.post("/transfer", response_model=TransactionResponse)
def transfer_money(transfer_request: TransferRequest, db: Session = Depends(get_db)):
    # Start a transaction (database transaction, not our business transaction)
    try:
        # Get sender account
        sender_account = db.query(Account).filter(
            Account.account_number == transfer_request.sender_account_number
        ).with_for_update().first()  # Lock the row for update

        if not sender_account:
            raise HTTPException(status_code=404, detail="Sender account not found")

        # Get receiver account
        receiver_account = db.query(Account).filter(
            Account.account_number == transfer_request.receiver_account_number
        ).with_for_update().first()  # Lock the row for update

        if not receiver_account:
            raise HTTPException(status_code=404, detail="Receiver account not found")

        # Get sender's user to verify PIN
        sender_user = db.query(User).filter(User.user_id == sender_account.user_id).first()
        if not sender_user:
            raise HTTPException(status_code=404, detail="Sender user not found")

        # Verify PIN
        if sender_user.pin != transfer_request.pin:
            raise HTTPException(status_code=401, detail="Invalid PIN")

        # Check if sender has enough balance
        if sender_account.balance < transfer_request.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Check if account is active
        if sender_account.status != "ACTIVE":
            raise HTTPException(status_code=400, detail="Sender account is not active")

        if receiver_account.status != "ACTIVE":
            raise HTTPException(status_code=400, detail="Receiver account is not active")

        # Create a reference number
        reference_number = TransactionCreate.generate_reference_number()

        # Find sender name and receiver name
        sender_name = sender_user.full_name
        receiver_name = db.query(User).get(receiver_account.user_id).full_name

        # Create transaction record
        transaction = Transaction(
            reference_number=reference_number,
            sender_account_id=sender_account.account_id,
            receiver_account_id=receiver_account.account_id,
            amount=transfer_request.amount,
            message=transfer_request.message,
            transaction_type="transfer via Octo Pay",
            sender_name=sender_name,
            receiver_name=receiver_name,
        )

        # Update account balances
        sender_account.balance -= transfer_request.amount
        receiver_account.balance += transfer_request.amount

        # Save transaction and account updates
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

@router.get("/account/{account_id}", response_model=List[TransactionResponse])
def get_account_transactions(account_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        or_(
            Transaction.sender_account_id == account_id,
            Transaction.receiver_account_id == account_id
        )
    ).order_by(Transaction.transaction_time.desc()).all()
    return transactions

@router.put("/category/{transaction_id}", response_model=TransactionResponse)
def update_transaction_category(
    transaction_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction.category_main = category_update.category_main
    transaction.category_sub = category_update.category_sub
    db.commit()
    db.refresh(transaction)
    return transaction