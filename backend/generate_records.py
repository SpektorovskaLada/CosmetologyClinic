import random
from datetime import datetime, timedelta

import psycopg2


DB_NAME = "CosmetologyClinic"
DB_USER = "postgres"
DB_PASSWORD = "Jdty2005"
DB_HOST = "localhost"
DB_PORT = "5432"

ID_USER = 1
ID_DOCTOR = 1

RECORDS_COUNT = 12000

START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2026, 5, 15)


def random_phone():
    codes = ["50", "63", "66", "67", "68", "73", "93", "95", "96", "97", "98", "99"]
    return "+380" + random.choice(codes) + "".join(random.choices("0123456789", k=7))


def weighted_random_date():
    while True:
        days = (END_DATE - START_DATE).days
        date = START_DATE + timedelta(days=random.randint(0, days))
        month = date.month

        if month in [9, 10, 11, 12]:
            weight = 1.45
        elif month in [1, 2, 3]:
            weight = 1.25
        elif month in [6, 7, 8]:
            weight = 0.75
        else:
            weight = 1.0

        if random.random() < weight / 1.45:
            hour = random.randint(9, 18)
            minute = random.choice([0, 15, 30, 45])
            return date.replace(hour=hour, minute=minute, second=0, microsecond=0)


def choose_service_id(service_ids, appointment_date):
    peeling_services = [37, 38, 39, 40]
    cleaning_services = [31, 32, 33]
    care_services = [34, 35, 36, 41]
    injection_services = [1, 2, 3, 4, 8, 9, 10, 11, 14, 15, 16, 17, 18, 20, 21]
    hardware_services = [22, 23, 24, 25, 26, 27, 28, 29, 30]

    month = appointment_date.month
    available = []

    if month in [9, 10, 11, 12, 1, 2]:
        available += peeling_services * 5
        available += injection_services * 3
        available += hardware_services * 3
        available += cleaning_services * 2
        available += care_services * 2
    elif month in [6, 7, 8]:
        available += cleaning_services * 4
        available += care_services * 4
        available += injection_services * 2
        available += hardware_services * 2
        available += peeling_services * 1
    else:
        available += cleaning_services * 3
        available += care_services * 3
        available += injection_services * 3
        available += hardware_services * 2
        available += peeling_services * 2

    available = [s for s in available if s in service_ids]

    if not available:
        return random.choice(service_ids)

    return random.choice(available)

def client_weight(client):
    id_client, first_name, last_name, phone, birth_date, gender = client

    if birth_date is None:
        return 1.0

    age = datetime.today().year - birth_date.year

    # Жінки відвідують частіше
    if gender == "F":
        if 18 <= age <= 25:
            return 3.0
        elif 26 <= age <= 35:
            return 4.8
        elif 36 <= age <= 45:
            return 4.2
        elif age >= 46:
            return 3.2
        else:
            return 0.7

    # Чоловіки відвідують рідше
    if gender == "M":
        if 18 <= age <= 25:
            return 0.9
        elif 26 <= age <= 35:
            return 1.3
        elif 36 <= age <= 45:
            return 1.1
        elif age >= 46:
            return 0.8
        else:
            return 0.2

    return 1.0

def main():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT id_client, first_name, last_name, phone, birth_date, gender
        FROM public.client;
    """)
    clients = cur.fetchall()

    cur.execute("SELECT id_service FROM public.services;")
    service_ids = [row[0] for row in cur.fetchall()]

    if not clients:
        raise Exception("No clients found")

    if not service_ids:
        raise Exception("No services found")

    for _ in range(RECORDS_COUNT):
        weights = [client_weight(client) for client in clients]

        id_client, first_name, last_name, phone, birth_date, gender = random.choices(
            clients,
            weights=weights,
            k=1
        )[0]

        appointment_date = weighted_random_date()
        id_service = choose_service_id(service_ids, appointment_date)

        full_name = f"{first_name} {last_name}"
        request_status = "оброблено"

        record_status = random.choices(
            ["завершено", "заплановано", "скасовано"],
            weights=[78, 12, 10],
            k=1
        )[0]

        if record_status == "скасовано":
            payment_stat = "не оплачено"
        elif record_status == "заплановано":
            payment_stat = random.choices(
                ["не оплачено", "оплачено"],
                weights=[80, 20],
                k=1
            )[0]
        else:
            payment_stat = random.choices(
                ["оплачено", "не оплачено"],
                weights=[88, 12],
                k=1
            )[0]

        comment = random.choice([
            "",
            "Запис створено адміністратором",
            "Клієнт уточнював час",
            "Повторний запис",
            "Первинна консультація",
        ])

        request_date = appointment_date - timedelta(days=random.randint(1, 21))

        cur.execute(
            """
            INSERT INTO public.call_requests
            (id_user, name, phone, comment, request_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_request;
            """,
            (
                ID_USER,
                full_name,
                phone if phone else random_phone(),
                comment,
                request_date,
                request_status,
            )
        )

        id_request = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO public.records
            (id_service, id_client, id_doctor, id_request, id_user, status, "date&time", comment, payment_stat)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                id_service,
                id_client,
                ID_DOCTOR,
                id_request,
                ID_USER,
                record_status,
                appointment_date,
                comment,
                payment_stat,
            )
        )

    conn.commit()
    cur.close()
    conn.close()

    print(f"Created {RECORDS_COUNT} records and call requests")
    print(f"Period: {START_DATE.date()} - {END_DATE.date()}")


if __name__ == "__main__":
    main()