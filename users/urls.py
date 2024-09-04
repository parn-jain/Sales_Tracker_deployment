from django.urls import path
from django.contrib.auth import views as authentication_views
from sales_tracker.requirements import min_mining_required
from users import views as user_views



urlpatterns = [
    path("register/", user_views.register, name="register"),
    # path("user/profile", user_views.detail_profile, name="detailprofile"),
    path("detailprofile", user_views.detail_profile, name="detail_profile"),
    path("profile/", user_views.profile, name = "profile"),
    path("forgetpass/", user_views.forget_pass, name="forgetpass"),
    # path("login/", authentication_views.LoginView.as_view(template_name = "users/login.html"), name="login" ),
    path("login/", user_views.manual_login, name = "login"),
    # path("logout/", min_mining_required(user_views.LogoutView.as_view(template_name = "users/logout.html")), name="logout" ),
    path("logout/", user_views.Logout, name="logout" ),
    path("calling-details", user_views.calling_details_view, name = "calling_details"),


    path("password_reset/", authentication_views.PasswordResetView.as_view(template_name = "users/password_reset_form.html"), name="password_reset"),
    path("password_reset_done/", authentication_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>", authentication_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password_reset_complete/", authentication_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_complete.html"), name="password_reset_complete"),
    path("reason/",user_views.Reason , name="reason"),
    path('', user_views.index, name='index'),
    path('heartbeat/', user_views.heartbeat, name='heartbeat'),

]