import pandas as pd
import numpy as np
from datetime import date, timedelta

CLIENTS_COUNT = 3000
RANDOM_STATE = 42

np.random.seed(RANDOM_STATE)

# =========================
# ЗЧИТУВАННЯ CSV
# =========================

df = pd.read_csv(
    "clients.csv",
    sep=None,
    engine="python",
    encoding="cp1251"
)

# =========================
# ВИПАДКОВІ 3000 ЛЮДЕЙ
# =========================

df = df.sample(
    CLIENTS_COUNT,
    random_state=RANDOM_STATE
).reset_index(drop=True)

# =========================
# ПЕРЕЙМЕНУВАННЯ КОЛОНОК
# =========================

df = df.rename(columns={
    "name": "first_name",
    "surname": "last_name"
})

# =========================
# ВИДАЛЯЄМО id_client
# (він auto increment)
# =========================

if "id_client" in df.columns:
    df = df.drop(columns=["id_client"])

# =========================
# РОЗПОДІЛ ГРУП
# =========================

groups = (
    ["adult_female"] * 2160 +   # 72%
    ["teen_female"] * 360 +     # 12%
    ["child_female"] * 180 +    # 6%

    ["adult_male"] * 240 +      # 8%
    ["teen_male"] * 45 +        # 1.5%
    ["child_male"] * 15         # 0.5%
)

np.random.shuffle(groups)

# =========================
# ГЕНЕРАЦІЯ ДАТ НАРОДЖЕННЯ
# =========================

def random_birth_date(min_age, max_age):
    today = date.today()

    age = np.random.randint(min_age, max_age + 1)

    start = date(today.year - age, 1, 1)
    end = date(today.year - age, 12, 31)

    random_days = np.random.randint(
        0,
        (end - start).days + 1
    )

    return start + timedelta(days=random_days)

# =========================
# УКРАЇНСЬКІ ТЕЛЕФОНИ
# =========================

def generate_ukrainian_phone():
    operator_codes = [
        "50", "63", "66", "67",
        "68", "73", "93", "95",
        "96", "97", "98", "99"
    ]

    code = np.random.choice(operator_codes)

    number = "".join(
        np.random.choice(list("0123456789"), size=7)
    )

    return f"+380{code}{number}"

phones = set()

while len(phones) < CLIENTS_COUNT:
    phones.add(generate_ukrainian_phone())

phones = list(phones)

# =========================
# GENDER + BIRTH DATE
# =========================

birth_dates = []
genders = []

for group in groups:

    if group == "adult_female":
        genders.append("F")
        birth_dates.append(
            random_birth_date(18, 65)
        )

    elif group == "teen_female":
        genders.append("F")
        birth_dates.append(
            random_birth_date(12, 17)
        )

    elif group == "child_female":
        genders.append("F")
        birth_dates.append(
            random_birth_date(0, 11)
        )

    elif group == "adult_male":
        genders.append("M")
        birth_dates.append(
            random_birth_date(18, 65)
        )

    elif group == "teen_male":
        genders.append("M")
        birth_dates.append(
            random_birth_date(12, 17)
        )

    elif group == "child_male":
        genders.append("M")
        birth_dates.append(
            random_birth_date(0, 11)
        )

# =========================
# ЗАПОВНЕННЯ ПОЛІВ
# =========================

df["gender"] = genders
df["birth_date"] = birth_dates
df["phone"] = phones

# якщо NOT NULL
df["id_user"] = 1

# =========================
# ЛИШЕ ПОТРІБНІ КОЛОНКИ
# =========================

needed_columns = [
    "first_name",
    "last_name",
    "patronymic",
    "phone",
    "birth_date",
    "id_user",
    "gender"
]

df = df[needed_columns]

# =========================
# ЗБЕРЕЖЕННЯ
# =========================

df.to_csv(
    "clients_clean.csv",
    index=False,
    encoding="utf-8"
)

# =========================
# СТАТИСТИКА
# =========================

print("clients_clean.csv created")
print()

print("Gender stats:")
print(df["gender"].value_counts())

print()

birth_series = pd.to_datetime(df["birth_date"])

today_year = date.today().year

ages = today_year - birth_series.dt.year

print("Children (<12):", (ages < 12).sum())
print("Teenagers (12-17):", ((ages >= 12) & (ages < 18)).sum())
print("Adults (18+):", (ages >= 18).sum())