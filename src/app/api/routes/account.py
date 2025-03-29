from typing import List, Optional, Type
from fastapi import APIRouter, Depends
from app.database.connection import get_db
from app.models.account_model import AccountModel, AccountType
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountResponse
from app.services.account_service import AccountService

router = APIRouter(
    prefix="/accounts",
)

def get_account_service(db=Depends(get_db)):
    return AccountService(AccountRepository(db))

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
        account_id: int,
        account_service: AccountService = Depends(get_account_service)
) -> Optional[AccountModel]:
    return account_service.get_account_by_account_id(account_id)

@router.get("/user/{user_id}", response_model=List[AccountResponse])
def get_user_accounts(
        user_id: int,
        account_service: AccountService = Depends(get_account_service)
) -> list[Type[AccountModel]]:
    return account_service.get_account_by_user_id(user_id)

@router.get("/user/{account_type}/{user_id}", response_model=AccountResponse)
def get_account_by_user_id_and_account_type(
        account_type: AccountType,
        user_id: int,
        account_service: AccountService = Depends(get_account_service)
) -> Optional[AccountModel]:
    return account_service.get_account_by_user_id_and_account_type(user_id, account_type)

@router.get("/number/{account_number}", response_model=AccountResponse)
def get_account_by_number(
    account_number: str,
    account_service: AccountService = Depends(get_account_service)
) -> Optional[AccountModel]:
    return account_service.get_account_by_account_number(account_number)
