from django.conf import settings
from django.utils.translation import gettext_lazy as _

PROPOSAL_ACTION_LABELS = {
    "accept": _("Принять"),
    "reject": _("Отклонить"),
    "cancel": _("Отменить"),
}


def user_can_perform_action(proposal, action_config, user):
    if action_config["role"] == "receiver":
        return proposal.ad_receiver.user_id == user.id
    return proposal.ad_sender.user_id == user.id


def get_allowed_actions(proposal, user):
    if proposal.status != "pending":
        return []

    allowed_actions = []
    for action_name, action_label in PROPOSAL_ACTION_LABELS.items():
        action_config = settings.PROPOSAL_ACTIONS.get(action_name)
        if not action_config:
            continue
        if not user_can_perform_action(proposal, action_config, user):
            continue
        allowed_actions.append({"name": action_name, "label": action_label})
    return allowed_actions


def get_action_config(action_name):
    return settings.PROPOSAL_ACTIONS.get(action_name)
