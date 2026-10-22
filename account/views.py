from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def admin_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        return redirect("user_dashboard")

    products = Product.objects.all()

    return render(
        request,
        "admin_dashboard.html",
        {
            "products": products
        }
    )


def user_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.is_staff:
        return redirect("admin_dashboard")

    products = Product.objects.all()

    return render(
        request,
        "user_dashboard.html",
        {
            "products": products
        }
    )


def add_product(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        return redirect("user_dashboard")

    edit_id = request.GET.get("edit")

    edit_product = None

    if edit_id:
        edit_product = get_object_or_404(
            Product,
            id=edit_id
        )

    if request.method == "POST":

        product_id = request.POST.get("product_id")

        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        product_description = request.POST.get("product_description")
        product_image = request.FILES.get("product_image")

        if product_id:

            product = get_object_or_404(
                Product,
                id=product_id
            )

            product.product_name = product_name
            product.product_price = product_price
            product.product_description = product_description

            if product_image:
                product.product_image = product_image

            product.save()

        else:

            Product.objects.create(
                product_name=product_name,
                product_price=product_price,
                product_image=product_image,
                product_description=product_description
            )

        return redirect("admin_dashboard")

    return render(
        request,
        "add_product.html",
        {
            "edit_product": edit_product
        }
    )


def delete_product(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        return redirect("user_dashboard")

    product = get_object_or_404(
        Product,
        id=id
    )

    product.delete()

    return redirect("admin_dashboard")


def signup_function(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if role == "admin":

            user.is_staff = True
            user.save()

        return redirect("login")

    return redirect("signup")


def login_function(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(
                request,
                user
            )

            if user.is_staff:
                return redirect("admin_dashboard")

            return redirect("user_dashboard")

        return redirect("login")

    return redirect("login")


def logout_function(request):

    logout(request)

    return redirect("login")


class AddProductAPI(APIView):

    authentication_classes = [
        TokenAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        if not request.user.is_staff:

            return Response(
                {
                    "message": "Only admin can add product"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Product added successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )