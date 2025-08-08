from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Advertisement, FavoriteAdvertisement
from .serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer
from .permissions import IsOwnerPermission, IsAdminOROwner
from .filters import AdvertisementFilter
from .filters import FixedDjangoFilterBackend


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    serializer_class = AdvertisementSerializer
    filter_backends = [FixedDjangoFilterBackend]
    filterset_class = AdvertisementFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
    

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "favorite"]:
            return [IsAuthenticated()]
        if self.action in ["delete", "update", "partial_update"]:
            return [IsAuthenticated(), IsAdminOROwner()]
        if self.action == "favorite_instance":
            return [IsAuthenticated(), IsOwnerPermission()]
        return []
    
    def get_queryset(self):
        if not self.request.user.id:
            # Гость не может смотреть черновики
            return Advertisement.objects.filter(~Q(status="DRAFT"))
        if self.request.user.is_staff:
            # Админ смотрит все.
            return Advertisement.objects.all()
        else:
            # Пользователь не может смотреть чужие черновики
            return Advertisement.objects.exclude(
                ~Q(creator=self.request.user.id), status__exact='DRAFT'
            )    

    @action(
        detail=False,
        url_path='favorite'
    )
    def favorite(self, request, *args, **kwargs):
        favorite_queryset = FavoriteAdvertisement.objects.filter(user__exact=self.request.user)
        if not self.request.user.is_staff:
            favorite_queryset = favorite_queryset.select_related('advert').exclude(advert__status__exact="DRAFT")

        queryset = self.filter_queryset(
            Advertisement.objects.filter(id__in=[f.advert.id for f in favorite_queryset])
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='favorite'
    )
    def favorite_instance(self, request, pk, *args, **kwargs):
        if self.request.method == 'POST':
            serializer = FavoriteAdvertisementSerializer(
                data = {
                    "user": self.request.user.id,
                    "advert": pk
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        if self.request.method == 'DELETE':
            queryset = FavoriteAdvertisement.objects.filter(user__exact = self.request.user)
            instance = get_object_or_404(queryset, advert=pk)
            self.check_object_permissions(self.request, instance)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
