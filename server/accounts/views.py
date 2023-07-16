from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

from .forms import RegisterForm, EditForm


class PasswordChange(PasswordChangeView):
    def form_valid(self, form):
        # Invalidate tokens for the user
        Token.objects.filter(user=form.user).delete()
        return super().form_valid(form)


class PasswordChangeDone(PasswordChangeDoneView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super().get(request, *args, **kwargs)


class PasswordResetConfirm(PasswordResetConfirmView):
    def form_valid(self, form):
        # Invalidate tokens for the user
        Token.objects.filter(user=form.user).delete()
        return super().form_valid(form)


def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.is_active = False
            new_user.save()
            return render(
                request, "registration/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = RegisterForm()

    return render(request, "registration/register.html", {"form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("maintainer_dashboard")
    else:
        form = EditForm(instance=request.user)

    return render(request, "edit.html", {"form": form})
