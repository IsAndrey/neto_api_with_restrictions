from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, FavoriteAdvertisement

MAX_OPEN_ADVERTS = 10


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
        
    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию       
        
        if "status" not in data.keys():
            data["status"] = "OPEN"

        if (data["status"] == "OPEN" and
            Advertisement.objects.filter(
                creator__exact=self.context["request"].user,
                status__exact="OPEN"
            ).count() >= MAX_OPEN_ADVERTS
        ):
            raise ValidationError(
                detail = "The number of open ads should not exceed '%s'." % MAX_OPEN_ADVERTS
            )
        
        return super().validate(data)


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для валидации избранных объявлений."""

    class Meta:
        model = FavoriteAdvertisement
        fields = ['advert', 'user']

    def validate(self, data):

        if data["user"] == data["advert"].creator:
            # Пользователь может добавлять в избранное только чужие объявления.
            raise ValidationError(
                detail = "User cannot add own ads to favorite"
            )
        return super().validate(data)
