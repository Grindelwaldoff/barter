from django.urls import path

from ads import views

app_name = "ads"
urlpatterns = [
    path("", views.AdList.as_view(), name="list"),
    path("ad/<int:pk>/", views.AdDetail.as_view(), name="detail"),
    path("ad/new/", views.AdCreate.as_view(), name="create"),
    path("ad/<int:pk>/edit/", views.AdUpdate.as_view(), name="edit"),
    path("ad/<int:pk>/delete/", views.AdDelete.as_view(), name="delete"),
    path(
        "proposals/new/", views.ProposalCreate.as_view(), name="proposal_create"
    ),
    path("proposals/", views.ProposalList.as_view(), name="proposals_me"),
    path("proposals/<int:pk>/<str:action>/", views.ProposalActionView.as_view(), name="proposal_action"),
]
