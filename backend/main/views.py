import json
import pandas as pd

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from .models import Reviews, Client, Records, Doctor, Products, ProductCategories, Services, ServiceCategories
from django.contrib.admin.views.decorators import staff_member_required
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import date
from .models import Records


def is_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):

    review_error = request.session.pop("review_error", None)
    review_success = request.session.pop("review_success", None)

    reviews = Reviews.objects.all().order_by("-daterec", "-id_review")

    home_care = ProductCategories.objects.get(name="Домашній догляд")

    child_categories = ProductCategories.objects.filter(
        id_category_parent=home_care
    ).values_list("id_category", flat=True)

    home_products = Products.objects.filter(
        id_category__in=child_categories
    ).order_by("id_product")[:3]

    dermatology_categories = ServiceCategories.objects.filter(
        id_category_parent=5
    ).values_list("id_category", flat=True)

    has_dermatology_services = Services.objects.filter(
        id_category__in=dermatology_categories
    ).exists()

    context = {
        "review_error": review_error,
        "review_success": review_success,
        "reviews": reviews,
        "home_products": home_products,
        "has_dermatology_services": has_dermatology_services,
    }

    return render(request, "index.html", context)

def add_review(request):
    if request.method != "POST":
        return redirect("/#reviews")

    name = request.POST.get("name")
    email = request.POST.get("email")
    text = request.POST.get("text", "")
    rating = request.POST.get("rating")

    client = Client.objects.filter(email=email).first()

    if not client:
        request.session["review_error"] = "Клієнта з таким email не знайдено"
        return redirect("/#reviews")

    record = (
        Records.objects
        .filter(
            id_client=client,
            status="завершено"
        )
        .order_by("-date_time")
        .first()
    )

    if not record:
        request.session["review_error"] = "У клієнта немає завершених записів"
        return redirect("/#reviews")

    Reviews.objects.create(
        id_record=record,
        id_user=client.id_user,
        name=name,
        text=text,
        rating=int(rating),
        daterec=record.date_time.date()
    )

    request.session["review_success"] = "Відгук успішно додано"
    return redirect("/#reviews")

def get_services_by_parent_category(parent_id):
    child_categories = ServiceCategories.objects.filter(
        id_category_parent=parent_id
    ).order_by("id_category")

    services_by_category = []

    for category in child_categories:
        services = Services.objects.filter(
            id_category=category.id_category
        ).order_by("id_service")

        if services.exists():
            services_by_category.append({
                "category": category,
                "services": services
            })

    return services_by_category

def doctor_info(request):
    doctor = Doctor.objects.first()

    diplomas = []
    if doctor and doctor.diplomas:
        diplomas = [item.strip() for item in doctor.diplomas.split(",")]

    context = {
        "doctor": doctor,
        "diplomas": diplomas,
    }

    return render(request, "partials/doctor_info.html", context)


def shop(request):
    home_care = ProductCategories.objects.get(name="Домашній догляд")

    child_categories = ProductCategories.objects.filter(
        id_category_parent=home_care
    ).values_list("id_category", flat=True)

    products = Products.objects.filter(
        id_category__in=child_categories
    ).order_by("id_product")

    return render(request, "partials/shop.html", {
        "products": products
    })

def services_aesthetic(request):
    services_by_category = get_services_by_parent_category(3)

    return render(request, "partials/services/services_page.html", {
        "page_title": "Естетична косметологія",
        "services_by_category": services_by_category,
    })


def services_hardware(request):
    services_by_category = get_services_by_parent_category(1)

    return render(request, "partials/services/services_page.html", {
        "page_title": "Апаратна косметологія",
        "services_by_category": services_by_category,
    })


def services_inject(request):
    services_by_category = get_services_by_parent_category(2)

    return render(request, "partials/services/services_page.html", {
        "page_title": "Інʼєкційна косметологія",
        "services_by_category": services_by_category,
    })


@login_required
@staff_member_required
def admin_panel(request):
    return render(request, "admin_panel.html")
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    records_from = request.GET.get("records_from")
    records_to = request.GET.get("records_to")

    services_from = request.GET.get("services_from")
    services_to = request.GET.get("services_to")

    categories_from = request.GET.get("categories_from")
    categories_to = request.GET.get("categories_to")

    forecast_months = int(request.GET.get("forecast_months", 12))

    # тільки завершені записи
    records_qs = Records.objects.filter(status="завершено")

    if records_from:
        records_qs = records_qs.filter(date_time__date__gte=records_from)

    if records_to:
        records_qs = records_qs.filter(date_time__date__lte=records_to)

    records_by_month = (
        records_qs
        .annotate(month=TruncMonth("date_time"))
        .values("month")
        .annotate(count=Count("id_record"))
        .order_by("month")
    )

    month_labels = [item["month"].strftime("%Y-%m") for item in records_by_month]
    month_counts = [item["count"] for item in records_by_month]
    # дохід по місяцях
    income_by_month = (
        records_qs
        .annotate(month=TruncMonth("date_time"))
        .values("month")
        .annotate(income=Sum("id_service__price"))
        .order_by("month")
    )

    income_labels = [item["month"].strftime("%Y-%m") for item in income_by_month]
    income_values = [item["income"] or 0 for item in income_by_month]
    # прогноз доходу
    income_forecast_labels = []
    income_forecast_values = []
    income_forecast_lower = []
    income_forecast_upper = []

    if len(income_values) >= 24:
        try:
            income_ts = pd.Series(
                income_values,
                index=pd.to_datetime(income_labels)
            )

            income_ts = income_ts.asfreq("MS")

            income_model = SARIMAX(
                income_ts,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12),
                enforce_stationarity=False,
                enforce_invertibility=False
            )

            income_results = income_model.fit(disp=False)

            income_forecast = (
                income_results
                .get_forecast(steps=forecast_months)
                .predicted_mean
            )

            income_forecast_labels = [
                d.strftime("%Y-%m")
                for d in income_forecast.index
            ]

            income_forecast_values = [
                max(0, round(float(v)))
                for v in income_forecast.values
            ]
            income_forecast_lower = [round(v * 0.9) for v in income_forecast_values]
            income_forecast_upper = [round(v * 1.1) for v in income_forecast_values]

        except Exception:
            income_forecast_labels = []
            income_forecast_values = []
            income_forecast_lower = []
            income_forecast_upper = []
   
    # SARIMA + confidence interval
    forecast_labels = []
    forecast_values = []
    forecast_lower = []
    forecast_upper = []
    if len(month_counts) >= 24:
        try:
            ts = pd.Series(month_counts, index=pd.to_datetime(month_labels))
            ts = ts.asfreq("MS")

            model = SARIMAX(
                ts,
                order=(0, 1, 1),
                seasonal_order=(1, 1, 1, 12),
                enforce_stationarity=False,
                enforce_invertibility=False
            )

            results = model.fit(disp=False)
            forecast_result = results.get_forecast(steps=forecast_months)

            forecast = forecast_result.predicted_mean
            conf_int = forecast_result.conf_int()

            forecast_labels = [d.strftime("%Y-%m") for d in forecast.index]
            forecast_values = [max(0, round(float(v))) for v in forecast.values]
            forecast_lower = [ round(v * 0.9) for v in forecast_values]
            
            forecast_upper = [ round(v * 1.1) for v in forecast_values]
            
        except Exception:
            forecast_labels = []
            forecast_values = []
            forecast_lower = []
            forecast_upper = []

    # популярність послуг
    services_qs = Records.objects.filter(status="завершено")

    if services_from:
        services_qs = services_qs.filter(date_time__date__gte=services_from)

    if services_to:
        services_qs = services_qs.filter(date_time__date__lte=services_to)

    services_popularity = (
        services_qs
        .values("id_service__name")
        .annotate(count=Count("id_record"))
        .order_by("-count")[:10]
    )

    service_labels = [item["id_service__name"] for item in services_popularity]
    service_counts = [item["count"] for item in services_popularity]

    # популярність категорій
    categories_qs = Records.objects.filter(status="завершено")

    if categories_from:
        categories_qs = categories_qs.filter(date_time__date__gte=categories_from)

    if categories_to:
        categories_qs = categories_qs.filter(date_time__date__lte=categories_to)

    categories_popularity = (
        categories_qs
        .values("id_service__id_category__name")
        .annotate(count=Count("id_record"))
        .order_by("-count")
    )

    category_labels = [item["id_service__id_category__name"] for item in categories_popularity]
    category_counts = [item["count"] for item in categories_popularity]
  
    """
    # розподіл клієнтів за статтю

    gender_distribution = (
        Client.objects
        .values("gender")
        .annotate(count=Count("id_client"))
    )

    gender_labels = [
        item["gender"] or "Невідомо"
        for item in gender_distribution
    ]

    gender_counts = [
        item["count"]
        for item in gender_distribution
    ]"""
    # середня частота відвідувань дорослих клієнтів за статтю

    adult_clients = []

    for client in Client.objects.exclude(birth_date__isnull=True):
        age = date.today().year - client.birth_date.year

        if age >= 18:
            adult_clients.append(client.id_client)

    gender_clients = (
        Client.objects
        .filter(id_client__in=adult_clients)
        .values("gender")
        .annotate(client_count=Count("id_client"))
    )

    gender_records = (
        Records.objects
        .filter(
            status="завершено",
            id_client__in=adult_clients
        )
        .values("id_client__gender")
        .annotate(record_count=Count("id_record"))
    )

    gender_records_dict = {
        item["id_client__gender"] or "Невідомо": item["record_count"]
        for item in gender_records
    }

    gender_labels = []
    gender_counts = []

    for item in gender_clients:
        gender = item["gender"] or "Невідомо"
        client_count = item["client_count"]
        record_count = gender_records_dict.get(gender, 0)

        avg_frequency = record_count / client_count if client_count else 0

        gender_labels.append(gender)
        gender_counts.append(round(avg_frequency, 2))

    # популярність послуг залежно від статі

    services_gender = (
        Records.objects
        .filter(status="завершено")
        .values(
            "id_service__name",
            "id_client__gender"
        )
        .annotate(count=Count("id_record"))
    )

    service_gender_dict = {}

    for item in services_gender:

        service = item["id_service__name"]
        gender = item["id_client__gender"]
        count = item["count"]

        if service not in service_gender_dict:
            service_gender_dict[service] = {
                "M": 0,
                "F": 0
            }

        service_gender_dict[service][gender] = count


    gender_service_labels = list(service_gender_dict.keys())

    male_services_counts = [
        service_gender_dict[s]["M"]
        for s in gender_service_labels
    ]

    female_services_counts = [
        service_gender_dict[s]["F"]
        for s in gender_service_labels
    ]
    
    # популярність категорій за віком
    """
    records_with_age = (
        Records.objects
        .filter(status="завершено")
        .select_related("id_client", "id_service__id_category")
    )

    age_groups = {
        "18-25": 0,
        "26-35": 0,
        "36-45": 0,
        "46+": 0,
    }

    for record in records_with_age:

        if not record.id_client.birth_date:
            continue

        age = (
            date.today().year
            - record.id_client.birth_date.year
        )

        if 18 <= age <= 25:
            age_groups["18-25"] += 1

        elif 26 <= age <= 35:
            age_groups["26-35"] += 1

        elif 36 <= age <= 45:
            age_groups["36-45"] += 1

        elif age >= 46:
            age_groups["46+"] += 1"""
    # середня частота відвідувань клієнтів за віковими групами

    age_group_clients = {
        "18-25": 0,
        "26-35": 0,
        "36-45": 0,
        "46+": 0,
    }

    age_group_records = {
        "18-25": 0,
        "26-35": 0,
        "36-45": 0,
        "46+": 0,
    }

    clients_with_age = Client.objects.exclude(birth_date__isnull=True)

    for client in clients_with_age:
        age = date.today().year - client.birth_date.year

        if 18 <= age <= 25:
            age_group_clients["18-25"] += 1

        elif 26 <= age <= 35:
            age_group_clients["26-35"] += 1

        elif 36 <= age <= 45:
            age_group_clients["36-45"] += 1

        elif age >= 46:
            age_group_clients["46+"] += 1


    records_with_age = (
        Records.objects
        .filter(status="завершено")
        .select_related("id_client")
    )

    for record in records_with_age:
        if not record.id_client.birth_date:
            continue

        age = date.today().year - record.id_client.birth_date.year

        if 18 <= age <= 25:
            age_group_records["18-25"] += 1

        elif 26 <= age <= 35:
            age_group_records["26-35"] += 1

        elif 36 <= age <= 45:
            age_group_records["36-45"] += 1

        elif age >= 46:
            age_group_records["46+"] += 1


    age_groups = {}

    for group in age_group_clients:
        clients_count = age_group_clients[group]
        records_count = age_group_records[group]

        avg_frequency = records_count / clients_count if clients_count else 0

        age_groups[group] = round(avg_frequency, 2)

    context = {
        "records_from": records_from or "",
        "records_to": records_to or "",

        "services_from": services_from or "",
        "services_to": services_to or "",

        "categories_from": categories_from or "",
        "categories_to": categories_to or "",

        "forecast_months": forecast_months,

        "month_labels": json.dumps(month_labels, ensure_ascii=False),
        "month_counts": json.dumps(month_counts),

        "forecast_labels": json.dumps(forecast_labels, ensure_ascii=False),
        "forecast_values": json.dumps(forecast_values),
        "forecast_lower": json.dumps(forecast_lower),
        "forecast_upper": json.dumps(forecast_upper),

        "service_labels": json.dumps(service_labels, ensure_ascii=False),
        "service_counts": json.dumps(service_counts),

        "category_labels": json.dumps(category_labels, ensure_ascii=False),
        "category_counts": json.dumps(category_counts),
        "income_labels": json.dumps(income_labels, ensure_ascii=False),
        "income_values": json.dumps(income_values),
        "income_forecast_labels": json.dumps(income_forecast_labels, ensure_ascii=False),
        "income_forecast_values": json.dumps(income_forecast_values),
        "income_forecast_lower": json.dumps(income_forecast_lower),
        "income_forecast_upper": json.dumps(income_forecast_upper),
        "gender_labels": json.dumps(gender_labels, ensure_ascii=False),
        "gender_counts": json.dumps(gender_counts),

        "gender_service_labels": json.dumps(gender_service_labels),
        "male_services_counts": json.dumps(male_services_counts),
        "female_services_counts": json.dumps(female_services_counts),

        "age_group_labels": json.dumps(list(age_groups.keys()), ensure_ascii=False),
        "age_group_counts": json.dumps(list(age_groups.values())),
    }

    return render(request, "dashboard.html", context)