from django.contrib import admin

from ads.models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "user",
        "category",
        "condition",
        "created_at",
    )
    search_fields = ("title", "description")
    list_filter = ("category", "condition")


@admin.register(ExchangeProposal)
class EPAdmin(admin.ModelAdmin):
    list_display = ("pk", "ad_sender", "ad_receiver", "status", "created_at")
    list_filter = ("status",)
