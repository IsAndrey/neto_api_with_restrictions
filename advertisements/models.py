from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField(verbose_name='наименование')
    description = models.TextField(default='', verbose_name='содержание')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN,
        verbose_name='статус'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='дата обновления'
    )
    

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
    
    def __str__(self):
        return f'{self.title} / {self.status} / {self.created_at}'


class FavoriteAdvertisement(models.Model):
    """Избранные объявления."""

    advert = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name='объявление'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )


    class Meta:
        verbose_name = 'Избранное объявление'
        verbose_name_plural = 'Избранные объявления'
        constraints = [
            models.UniqueConstraint(
                fields=['advert', 'user'],
                name='unique_together_advert_user_constraint'
            )
        ]
