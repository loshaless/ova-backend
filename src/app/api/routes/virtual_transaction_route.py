from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repositories.account_repository import AccountRepository
from app.database.repositories.transaction_repository import TransactionRepository
from app.database.repositories.user_repository import UserRepository
from app.database.repositories.virtual_transaction_repository import VirtualTransactionRepository
from app.schemas.virtual_transaction_schema import VirtualTransactionCreate, VirtualTransactionResponse
from app.services.virtual_transaction_service import VirtualTransactionService

router = APIRouter(
    prefix="/virtual-transactions"
)


def get_virtual_transaction_service(db: Session = Depends(get_db)) -> VirtualTransactionService:
    return VirtualTransactionService(
        AccountRepository(db),
        UserRepository(db),
        VirtualTransactionRepository(db)
    )


@router.post("/", response_model=List[VirtualTransactionResponse])
def create_virtual_transactions(
    request: VirtualTransactionCreate,
    virtual_transaction_service: VirtualTransactionService = Depends(get_virtual_transaction_service)
):
    return virtual_transaction_service.create_virtual_transactions(request)
