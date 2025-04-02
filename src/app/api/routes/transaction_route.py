from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repositories.account_repository import AccountRepository
from app.database.repositories.category_repository import CategoryRepository
from app.database.repositories.transaction_repository import TransactionRepository
from app.database.repositories.user_repository import UserRepository
from app.schemas.transaction_schema import TransactionResponse, TransferRequest, CategoryUpdateRequest
from app.services.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
)

def get_transaction_service(db: Session = Depends(get_db)) -> TransactionService:
    return TransactionService(AccountRepository(db), TransactionRepository(db), UserRepository(db), CategoryRepository(db))

@router.post("/transfer", response_model=TransactionResponse)
def transfer_money(
    transfer_request: TransferRequest,
    transaction_service: TransactionService = Depends(get_transaction_service)
):
    return transaction_service.transfer_money(transfer_request)

@router.get("/account/{account_id}", response_model=List[TransactionResponse])
def get_account_transactions(
    account_id: int,
    transaction_service: TransactionService = Depends(get_transaction_service)
):
    return transaction_service.get_account_transactions(account_id)

@router.put("/category/{transaction_id}", response_model=TransactionResponse)
def update_transaction_category(
    transaction_id: int,
    category_update: CategoryUpdateRequest,
    transaction_service: TransactionService = Depends(get_transaction_service)
):
    return transaction_service.update_transaction_category(transaction_id, category_update.category_main, category_update.category_sub)