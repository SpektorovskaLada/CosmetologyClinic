from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import (
    Client,
    Doctor,
    Products,
    ProductCategories,
    Records,
    Reviews,
    Services,
    ServiceCategories,
    UsedProducts,
    CallRequests,
)


admin.site.site_header = "Cosmetology Clinic Admin"
admin.site.site_title = "Clinic Admin"
admin.site.index_title = ""


class DashboardLinkAdminMixin:
    class Media:
        css = {
            "all": ("css/admin_custom.css",)
        }


@admin.register(Client)
class ClientAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_client", "first_name", "last_name", "phone", "birth_date", "gender", "email")
    search_fields = ("first_name", "last_name", "phone", "email")
    list_filter = ("gender",)
    ordering = ("id_client",)

    fields = (
        "first_name",
        "last_name",
        "patronymic",
        "phone",
        "birth_date",
        "id_user",
        "gender",
        "email",
    )


@admin.register(Doctor)
class DoctorAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_doctor", "fisrt_name", "last_name", "specialization", "phone", "email")
    search_fields = ("fisrt_name", "last_name", "specialization", "phone", "email")


@admin.register(ServiceCategories)
class ServiceCategoriesAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_category", "name", "type", "id_user")
    search_fields = ("name", "type")
    list_filter = ("type",)


@admin.register(Services)
class ServicesAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_service", "name", "id_category", "price", "duration")
    search_fields = ("name", "description")
    list_filter = ("id_category",)
    ordering = ("id_service",)


@admin.register(ProductCategories)
class ProductCategoriesAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_category", "name", "description", "id_user")
    search_fields = ("name", "description")


@admin.register(Products)
class ProductsAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_product", "name", "id_category", "price", "quantity")
    search_fields = ("name", "description")
    list_filter = ("id_category",)
    ordering = ("id_product",)


@admin.register(CallRequests)
class CallRequestsAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_request", "name", "phone", "request_date", "status")
    search_fields = ("name", "phone", "comment")
    list_filter = ("status", "request_date")
    ordering = ("-request_date",)

    fields = (
        "name",
        "phone",
        "comment",
        "status",
    )


@admin.register(Records)
class RecordsAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = (
        "id_record",
        "id_client",
        "id_service",
        "id_doctor",
        "status",
        "date_time",
        "payment_stat",
    )
    search_fields = (
        "id_client__first_name",
        "id_client__last_name",
        "id_client__phone",
        "id_service__name",
    )
    list_filter = ("status", "payment_stat", "id_service", "date_time")
    ordering = ("-date_time",)


@admin.register(Reviews)
class ReviewsAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_review", "id_record", "rating", "daterec")
    search_fields = ("text",)
    list_filter = ("rating", "daterec")
    ordering = ("-daterec",)


@admin.register(UsedProducts)
class UsedProductsAdmin(DashboardLinkAdminMixin, admin.ModelAdmin):
    list_display = ("id_used", "id_record", "id_product", "quantity")
    search_fields = ("id_product__name",)