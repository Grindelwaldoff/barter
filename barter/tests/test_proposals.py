import pytest
from django.urls import reverse

class TestProposalViews:

    @pytest.mark.django_db(transaction=True)
    def test_proposals_list_filters_by_status_and_role(
        self,
        auth_client,
        proposal_from_user,
        proposal_to_user,
    ):
        proposal_to_user.status = "accepted"
        proposal_to_user.save(update_fields=["status"])

        response = auth_client.get(
            reverse("ads:proposals_me"),
            {"status": "pending", "who": "sender"},
        )

        assert response.status_code == 200
        proposals = list(response.context["object_list"])
        assert proposal_from_user in proposals
        assert proposal_to_user not in proposals

    @pytest.mark.django_db(transaction=True)
    def test_proposal_actions_accept(self, auth_client, proposal_to_user):
        action_url = reverse("ads:proposal_action", args=[proposal_to_user.pk, "accept"])
        response = auth_client.post(action_url)

        assert response.status_code in (302, 204)
        proposal_to_user.refresh_from_db()
        assert proposal_to_user.status == "accepted"

    @pytest.mark.django_db(transaction=True)
    def test_proposal_actions_reject_by_receiver(self, auth_client, proposal_to_user):
        action_url = reverse("ads:proposal_action", args=[proposal_to_user.pk, "reject"])
        response = auth_client.post(action_url)

        assert response.status_code in (302, 204)
        proposal_to_user.refresh_from_db()
        assert proposal_to_user.status == "rejected"

    @pytest.mark.django_db(transaction=True)
    def test_proposal_action_forbidden_for_other_user(
        self,
        client,
        proposal_to_user,
        another_user,
    ):
        client.force_login(another_user)
        action_url = reverse("ads:proposal_action", args=[proposal_to_user.pk, "accept"])
        response = client.post(action_url)

        assert response.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_proposal_cancel_allowed_for_sender(self, auth_client, proposal_from_user):
        action_url = reverse("ads:proposal_action", args=[proposal_from_user.pk, "cancel"])
        response = auth_client.post(action_url)

        assert response.status_code in (302, 204)
        proposal_from_user.refresh_from_db()
        assert proposal_from_user.status == "rejected"
