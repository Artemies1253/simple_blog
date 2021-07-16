from django.urls import path
from .views import LoginViews, LogoutViews, RegistrationView, ProfileView, ProfileRedactView

urlpatterns = [
    path("login/", LoginViews.as_view(), name="login"),
    path("logout/", LogoutViews.as_view(), name="logout"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/profile/redact", ProfileRedactView.as_view(), name="profile_redact")
]
