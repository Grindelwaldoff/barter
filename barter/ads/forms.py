from django import forms

from core.forms import BootstrapFormMixin

from ads.models import Ad, ExchangeProposal


class AdForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["title", "description", "image_url", "category", "condition"]


class ProposalForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ["ad_sender", "ad_receiver", "comment"]
