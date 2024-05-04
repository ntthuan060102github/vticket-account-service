from dataclasses import dataclass
import datetime

from vticket_app.enums.gender_enum import GenderEnum

@dataclass
class UpdateProfileDTO():
    first_name: str = None
    last_name: str = None
    gender: GenderEnum = None
    birthday: datetime.date = None
    phone_number: str = None

    def __post_init__(self):
        self.gender = (GenderEnum)(self.gender)