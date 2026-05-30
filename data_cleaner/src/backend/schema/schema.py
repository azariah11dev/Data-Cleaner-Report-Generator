from pydantic import BaseModel
from typing import Dict, Union


class CleaningRequest(BaseModel):
    fill_value: Union[str, float, int, None] = None
    columns: list[str]
    missing_strategy: str
    file_name: str


class Stats(BaseModel):
    strategy: str
    missing_before: Dict[str, int]
    missing_after: Dict[str, int]
    rows_before: int
    rows_after: int
    fill_value: Union[str, float, int, None] = None