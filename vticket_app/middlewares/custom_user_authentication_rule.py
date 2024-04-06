from vticket_app.enums.account_status_enum import AccountStatusEnum
from vticket_app.models.user import User

def custom_user_authentication_rule(user: User) -> bool:
    return user is not None and user.status == AccountStatusEnum.ACTIVED