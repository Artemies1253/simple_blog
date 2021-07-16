from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import RegistrationForm, ProfileForm
from django.http import HttpResponseRedirect


class LoginViews(LoginView):
    template_name = "users/login.html"


class LogoutViews(LogoutView):
    template_name = "users/logout.html"


class RegistrationView(views.View):
    def get(self, request):
        registration_form = RegistrationForm()
        return render(request, "users/registration.html",
                      {"registration_form": registration_form})

    def post(self, request):
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            phone = registration_form.cleaned_data["phone"]
            city = registration_form.cleaned_data["city"]
            Profile.objects.create(
                user=user,
                phone=phone,
                city=city
            )
            user_name = registration_form.cleaned_data["username"]
            raw_password = registration_form.cleaned_data["password1"]
            user = authenticate(username=user_name, password=raw_password)
            login(request, user)
            return HttpResponseRedirect("/")
        return render(request, "users/registration.html",
                      {"registration_form": registration_form})


class ProfileView(LoginRequiredMixin, views.View):
    def get(self, request):
        return render(request, "users/profile.html", {})


class ProfileRedactView(LoginRequiredMixin, views.View):
    def get(self, request):
        user = request.user
        data = {"first_name": f"{user.first_name}",
                "last_name": f"{user.last_name}",
                "phone": f"{user.profile.phone}",
                "city": f"{user.profile.city}"}
        profile_form = ProfileForm(data)
        return render(request, "users/profile_redact.html", {"profile_form": profile_form})

    def post(self, request):
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            user = request.user
            user.first_name = profile_form.cleaned_data["first_name"]
            user.last_name = profile_form.cleaned_data["last_name"]
            user.profile.phone = profile_form.cleaned_data["phone"]
            user.profile.city = profile_form.cleaned_data["city"]
            user.save()
            user.profile.save()
            return redirect('profile')
        return render(request, "users/profile_redact.html", {"profile_form": profile_form})
