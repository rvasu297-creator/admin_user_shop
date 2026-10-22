from django.urls import path
from .views import *

urlpatterns = [

    path("", login, name="home"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("login_function/", login_function, name="login_function"),
    path("signup_function/", signup_function, name="signup_function"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("user-dashboard/", user_dashboard, name="user_dashboard"),
    path("add-product/", add_product, name="add_product"),
    path("delete-product/<int:id>/", delete_product, name="delete_product"),
    path("logout/", logout_function, name="logout"),
    path("api/add-product/", AddProductAPI.as_view(), name="add_product_api"),

]