from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from ads.forms import AdForm, ProposalForm
from ads.models import Ad, ExchangeProposal
from ads.utils import get_action_config, get_allowed_actions, user_can_perform_action


class IsOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user


class AdList(ListView):
    model = Ad
    paginate_by = 12

    def get_queryset(self):
        search_query = self.request.GET.get("q")
        category_filter = self.request.GET.get("category")
        condition_filter = self.request.GET.get("condition")

        filters = {}
        if category_filter:
            filters["category__iexact"] = category_filter
        if condition_filter:
            filters["condition"] = condition_filter

        ads = Ad.objects.filter(**filters).order_by("-created_at")
        if search_query:
            ads = ads.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
            )
        return ads

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["condition_choices"] = settings.CONDITION_CHOICES
        return context


class AdDetail(DetailView):
    model = Ad


class AdCreate(LoginRequiredMixin, CreateView):
    model, form_class, success_url = Ad, AdForm, reverse_lazy("ads:list")
    confirm_template_name = "ads/ad_form_confirm.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        if request.POST.get("edit"):
            form = self.get_form()
            return self.render_to_response(self.get_context_data(form=form))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.POST.get("confirm") != "yes":
            preview = form.save(commit=False)
            return self.render_confirm(form, preview)
        messages.success(self.request, "Объявление создано")
        return super().form_valid(form)

    def render_confirm(self, form, preview):
        context = self.get_context_data(form=form, preview=preview)
        return TemplateResponse(self.request, self.confirm_template_name, context)


class AdUpdate(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model, form_class, success_url = Ad, AdForm, reverse_lazy("ads:list")

    def form_valid(self, form):
        messages.success(self.request, "Объявление обновлено")
        return super().form_valid(form)


class AdDelete(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model, success_url = Ad, reverse_lazy("ads:list")


class ProposalCreate(LoginRequiredMixin, CreateView):
    model, form_class, success_url = (
        ExchangeProposal,
        ProposalForm,
        reverse_lazy("ads:proposals_me"),
    )

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Предложение отправлено")
        return super().form_valid(form)


class ProposalList(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    paginate_by = 12
    template_name = "ads/proposal_list.html"

    def get_queryset(self):
        proposals = ExchangeProposal.objects.select_related(
            "ad_sender", "ad_receiver"
        )
        who_filter = self.request.GET.get("who")
        status_filter = self.request.GET.get("status")
        current_user = self.request.user

        participant_filter = Q(ad_sender__user=current_user) | Q(ad_receiver__user=current_user)
        if who_filter == "sender":
            participant_filter = Q(ad_sender__user=current_user)
        elif who_filter == "receiver":
            participant_filter = Q(ad_receiver__user=current_user)
        proposals = proposals.filter(participant_filter)
        if status_filter:
            proposals = proposals.filter(status=status_filter)
        return proposals.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        for proposal in context["object_list"]:
            proposal.actions = get_allowed_actions(proposal, current_user)
        context["status_choices"] = settings.STATUS_CHOICES
        return context


class ProposalActionView(LoginRequiredMixin, View):

    def post(self, request, pk, action):
        action_config = get_action_config(action)
        if not action_config:
            return HttpResponseBadRequest("unknown action")

        proposal = self._get_proposal(pk)

        if proposal.status != "pending":
            return HttpResponse(status=409)

        if not user_can_perform_action(proposal, action_config, request.user):
            raise PermissionDenied

        proposal.status = action_config["status"]
        proposal.save(update_fields=["status"])

        if request.headers.get("Hx-Request") == "true":
            return HttpResponse(status=204)

        return redirect("ads:proposals_me")

    def _get_proposal(self, pk):
        return get_object_or_404(
            ExchangeProposal.objects.select_related("ad_sender__user", "ad_receiver__user"),
            pk=pk,
        )
