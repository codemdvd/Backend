from django.urls import path
from hello import views
from .views import LoginUser

urlpatterns = [
    path("", LoginUser.as_view(), name="home"),
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("choice/", views.choice, name ="choice"),
    path("tasks/", views.tasks, name ="tasks"),
    path("clients/", views.clients, name ="clients"),
    path("new_emp/", views.new_emp, name ="new_emp"),
    path("register/", views.register, name="register"),
    path("new_task/", views.new_task, name="new_task"),
    path("all_tasks/", views.all_tasks, name="all_tasks"),
    path("detail_view/", views.detail_view, name="detail_view"),
    path("permission/", views.new_task, name="permision"),
    path("download_file/", views.download_file, name="download_file"),
    path("update_order/", views.update_order, name="update_order"),
    path("status_classifier/", views.status_classifier, name="status_classifier"),
    path("delivery_classifier/", views.delivery_classifier, name="delivery_classifier"),
    path("income/", views.income, name="income"),
    path("income_product/", views.income_product, name="income_product"),
    path("order_product", views.order_product, name="order_product"),
    path("logout/", views.logout_user, name="logout_user"),
    path("login_redirect/", views.login_redirect, name="login_redirect"),
    path("product/", views.product, name="product"),
    path("new_order_product/", views.new_order_product, name="new_order_product"),
    path("employees", views.employees, name="employees"),
    path("role_classifier", views.role_classifier, name="role_classifier"),
    path("cars", views.cars, name="cars")


]