from django_filters import rest_framework as filters
from django_filters import ChoiceFilter, DateFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Advertisement
from .models import AdvertisementStatusChoices


class FixedDjangoFilterBackend(DjangoFilterBackend):
    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": "status",
                "in": "parameters",
                "required": False,
                "description": "Фильтр по статусу",
                "schema": {
                    "type": "string"
                }
            },
            {
                "name": "date_after",
                "in": "parameters",
                "required": False,
                "description": "Фильтр по по дате больше или равно",
                "schema": {
                    "type": "date"
                }
            },
            {
                "name": "date_before",
                "in": "parameters",
                "required": False,
                "description": "Фильтр по по дате меньше или равно",
                "schema": {
                    "type": "date"
                }
            }
        ]

class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    status = ChoiceFilter(
        choices=AdvertisementStatusChoices.choices
    )
    date = DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Advertisement
        fields = ['status', 'date']
