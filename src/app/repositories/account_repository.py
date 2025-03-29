from sqlalchemy.orm import Session
from typing import Type, Optional

from app.models.account_model import AccountModel


class AccountRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_account_by_account_id(self, account_id: int) -> Optional[AccountModel]:
        return self.session.query(AccountModel).filter(AccountModel.account_id == account_id).first()

    def get_account_by_account_number(self, account_number: str) -> Optional[AccountModel]:
        return self.session.query(AccountModel).filter(AccountModel.account_number == account_number).first()

    def get_account_by_user_id_and_account_type(self, user_id: int, account_type: str) -> Optional[AccountModel]:
        return (self.session
                .query(AccountModel)
                .filter(AccountModel.user_id == user_id,AccountModel.account_type == account_type)
                .first())

    def get_accounts_by_user_id(self, user_id: int) -> list[Type[AccountModel]]:
        return self.session.query(AccountModel).filter(AccountModel.user_id == user_id).all()