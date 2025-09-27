import pytest
from django.urls import reverse

from ads.models import Ad


class TestAdViews:

    @pytest.mark.django_db(transaction=True)
    def test_ad_create(self, auth_client, user):
        create_url = reverse("ads:create")
        ad_data = {
            "title": "Сноуборд",
            "description": "Отличное состояние",
            "image_url": "https://example.com/board.jpg",
            "category": "sport",
            "condition": "new",
            "confirm": "yes",
        }

        try:
            response = auth_client.post(create_url, data=ad_data)
        except Exception as exc:
            assert False, (
                "Страница `/ad/new/` работает неправильно. "
                f"Ошибка: `{exc}`"
            )

        assert response.status_code in (302, 303), (
            "Проверьте, что после создания объявления происходит редирект на список объявлений."
        )
        assert Ad.objects.filter(title="Сноуборд", user=user).exists(), (
            "Проверьте, что объявление сохраняется при отправке корректной формы."
        )
        assert response.headers["Location"] == reverse("ads:list"), (
            "Проверьте, что после создания объявления перенаправляете на страницу со списком."
        )

    @pytest.mark.django_db(transaction=True)
    def test_ad_update(self, auth_client, ad):
        update_url = reverse("ads:edit", args=[ad.pk])
        updated_data = {
            "title": "Городской велосипед",
            "description": ad.description,
            "image_url": ad.image_url,
            "category": ad.category,
            "condition": ad.condition,
        }

        response = auth_client.post(update_url, data=updated_data)
        assert response.status_code in (302, 303), (
            "Проверьте, что после редактирования объявления происходит редирект."
        )

        ad.refresh_from_db()
        assert ad.title == "Городской велосипед", (
            "Проверьте, что новые данные сохраняются после редактирования объявления."
        )

    @pytest.mark.django_db(transaction=True)
    def test_ad_delete(self, auth_client, ad):
        delete_url = reverse("ads:delete", args=[ad.pk])

        response = auth_client.post(delete_url)
        assert response.status_code in (302, 303), (
            "Проверьте, что после удаления объявления происходит редирект."
        )
        assert not Ad.objects.filter(pk=ad.pk).exists(), (
            "Проверьте, что объявление действительно удаляется."
        )

    @pytest.mark.django_db(transaction=True)
    def test_search_ads(self, client, user, another_user):
        Ad.objects.create(
            user=user,
            title="Электровелосипед",
            description="Для города",
            image_url="https://example.com/ebike.jpg",
            category="transport",
            condition="used",
        )
        Ad.objects.create(
            user=another_user,
            title="Ноутбук",
            description="Рабочий ноутбук",
            image_url="https://example.com/laptop.jpg",
            category="electronics",
            condition="used",
        )

        response = client.get(reverse("ads:list"), {"q": "вело"})
        assert response.status_code == 200, (
            "Проверьте, что страница со списком объявлений доступна для поиска."
        )

        titles = {item.title for item in response.context["object_list"]}
        assert "Электровелосипед" in titles, (
            "Проверьте, что объявление, подходящее под критерий поиска, отображается в списке."
        )
        assert "Ноутбук" not in titles, (
            "Проверьте, что поиск не возвращает объявления, не соответствующие запросу."
        )
