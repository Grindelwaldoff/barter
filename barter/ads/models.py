from django.conf import settings
from django.db import models


# verbose_name и help_text - иишкой сгенерены на базе прописанных мной моделей
class Ad(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name="Пользователь",
        help_text="Владелец объявления",
    )
    title = models.CharField(
        max_length=settings.MAX_TITLE_LENGTH,
        verbose_name="Заголовок",
        help_text="Краткий заголовок объявления",
    )
    description = models.TextField(
        max_length=settings.MAX_DESCRIPTION_LENGTH,
        verbose_name="Описание",
        help_text="Подробное описание предмета обмена",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Изображение (URL)",
        help_text="Ссылка на изображение предмета",
    )
    category = models.CharField(
        max_length=settings.MAX_CATEGORY_LENGTH,
        db_index=True,
        verbose_name="Категория",
        help_text="Категория товара или услуги",
    )
    condition = models.CharField(
        choices=settings.CONDITION_CHOICES,
        db_index=True,
        verbose_name="Состояние",
        help_text="Состояние предмета (новый или б/у)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время публикации объявления",
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f"{self.title} ({self.user})"


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="sent_proposals",
        verbose_name="Отправитель",
        help_text="Объявление, с которого сделано предложение",
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="received_proposals",
        verbose_name="Получатель",
        help_text="Объявление, которому адресовано предложение",
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
        help_text="Дополнительное сообщение к предложению",
    )
    status = models.CharField(
        choices=settings.STATUS_CHOICES,
        default="pending",
        db_index=True,
        verbose_name="Статус",
        help_text="Текущий статус предложения",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время отправки предложения",
    )

    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(ad_sender=models.F("ad_receiver")),
                name="check_user",
            ),
        ]

    def __str__(self):
        return f"Предложение {self.ad_sender} → {self.ad_receiver} [{self.status}]"
