from typing import Union

from vticket_app.models.user import User
from vticket_app.enums.account_status_enum import AccountStatusEnum
from vticket_app.serializers.user_serializer import UserSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q

class UserService:
    def lock_user(self, user_id: int) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.status = AccountStatusEnum.BLOCKED
            user.save(update_fields=["status"])
            return True
        except Exception as e:
            print(e)
            return False

    def unlock_user(self, user_id: int):
        try:
            user = User.objects.get(id=user_id)
            user.status = AccountStatusEnum.ACTIVED
            user.save(update_fields=["status"])
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_user_by_id(self, user_id: int) -> Union[User | None]:
        try:
            user = User.objects.get(id=user_id)
            data = UserSerializer(user, exclude=["password"]).data
            
            return data
        except:
            return None
        
    def search(self, keyword: str) -> list:
        search_query = SearchQuery(keyword)
        queryset = User.objects.annotate(
            rank_email=SearchRank(SearchVector("email"), search_query),
            rank_name=SearchRank(SearchVector("first_name", "last_name"), search_query)
        ).filter(
            Q(email__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword)
        ).order_by("-rank_email", "-rank_name")

        return UserSerializer(queryset, exclude=["password"], many=True).data