from typing import Optional, Type

from app.models.account_model import AccountModel
from app.repositories.account_repository import AccountRepository
from fastapi import HTTPException

class AccountService:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def get_account_by_account_id(self, account_id: int) -> Optional[AccountModel]:
        account = self.account_repository.get_account_by_account_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def get_account_by_account_number(self, account_number: str) -> Optional[AccountModel]:
        account = self.account_repository.get_account_by_account_number(account_number)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def get_account_by_user_id_and_account_type(self, user_id: int, account_type: str) -> Optional[AccountModel]:
        account =  self.account_repository.get_account_by_user_id_and_account_type(user_id, account_type)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def get_account_by_user_id(self, user_id: int) -> list[Type[AccountModel]]:
        return self.account_repository.get_accounts_by_user_id(user_id)