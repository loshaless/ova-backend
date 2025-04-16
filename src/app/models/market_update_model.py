from pydantic import BaseModel
from typing import Union

class MarketSummary(BaseModel):
    name: str
    value: Union[float, str]

class BIRate(BaseModel):
    tanggal: str
    bi_rate: str
