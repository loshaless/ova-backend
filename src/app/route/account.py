from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.account import Account, AccountType
from app.schemas.account import AccountResponse

router = APIRouter(
    prefix="/accounts",
)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/user/{user_id}", response_model=List[AccountResponse])
def get_user_accounts(user_id: int, db: Session = Depends(get_db)):
    accounts = db.query(Account).filter(Account.user_id == user_id).all()
    return accounts

@router.get("/user/{account_type}/{user_id}", response_model=AccountResponse)
def get_user_account(account_type: AccountType, user_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user_id, Account.account_type == account_type).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/number/{account_number}", response_model=AccountResponse)
def get_account_by_number(account_number: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
