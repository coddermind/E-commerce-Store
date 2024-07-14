from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.index,name="index"),
    path("<int:id>",views.details,name="details"),
    path("addcart/<int:id>",views.add_to_cart,name="add_to_cart"),
    path("addcartprodredirect/<int:id>",views.add_to_cart_product_redirect,name="add_to_cart_product_redirect"),
    path("removecartproductredirect/<int:id>",views.remove_from_cart_product_redirect,name="remove_from_cart_product_redirect"),
    path("removecartredirectcart/<int:id>",views.remove_from_cart_redirect_cart,name="remove_from_cart_redirect_cart"),
    path("update_cart/<int:id>",views.update_cart,name="update_cart"),
    path("updatecartredirectcart/<int:id>",views.update_cart_redirect_cart,name="update_cart_redirect_cart"),
    path("removecart/<int:id>",views.remove_from_cart,name="remove_from_cart"),
    path("cart/",views.cart,name="cart"),
    path("order_summary/",views.order_summary,name="order_summary"),
    path("order_summary_new/",views.order_summary_new,name="order_summary_new"),
    path("delivery_details/",views.delivery_details,name="delivery_details"),
    path("all_prev_orders/",views.all_prev_orders,name="all_prev_orders"),
    path("ord/<int:id>",views.one_prev_order,name="one_prev_order"),

    path("register_user/",views.register_user,name="register_user"),
    path("registration_confirmation/",views.registration_confirmation,name="registration_confirmation"),
    path("otp_failed/",views.otp_failed,name="otp_failed"),
    path("login_user/",views.login_user,name="login_user"),
    path("logout_user/",views.logout_user,name="logout_user"),

    path("about_us/",views.about,name="about"),

    path("password_change/",auth_views.PasswordChangeView.as_view(template_name="password_change.html"),name="password_change"),
    path("password_change_done/",auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"),name="password_change_done"),

    path("password_reset/",auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="password_reset"),
    path("passwrod_reset/done",auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
    path("password_reset_complete/",auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),
]