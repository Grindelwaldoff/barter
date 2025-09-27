import pytest
from django.test import Client

from ads.models import Ad, ExchangeProposal


@pytest.fixture

def user(django_user_model):
    return django_user_model.objects.create_user(
        username="creator",
        email="creator@example.com",
        password="secret",
    )


@pytest.fixture

def another_user(django_user_model):
    return django_user_model.objects.create_user(
        username="reader",
        email="reader@example.com",
        password="secret",
    )


@pytest.fixture

def auth_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture

def ad(user):
    return Ad.objects.create(
        user=user,
        title="Горный велосипед",
        description="Почти не пользовались",
        image_url="https://example.com/bike.jpg",
        category="sport",
        condition="used",
    )


@pytest.fixture

def other_ad(another_user):
    return Ad.objects.create(
        user=another_user,
        title="Смартфон",
        description="Меняю смартфон",
        image_url="https://example.com/phone.jpg",
        category="electronics",
        condition="used",
    )


@pytest.fixture

def proposal_from_user(ad, other_ad):
    return ExchangeProposal.objects.create(
        ad_sender=ad,
        ad_receiver=other_ad,
        comment="Обмен велосипеда на телефон",
        status="pending",
    )


@pytest.fixture

def proposal_to_user(ad, other_ad):
    return ExchangeProposal.objects.create(
        ad_sender=other_ad,
        ad_receiver=ad,
        comment="Предложение обменять телефон на велосипед",
        status="pending",
    )
