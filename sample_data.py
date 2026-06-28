# =====================================================
# ملف: sample_data.py
# الوصف: بيانات تجريبية لمحمصة هدب - يمكن استبدالها ببيانات حقيقية
# =====================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_employees() -> pd.DataFrame:
    """
    توليد بيانات تجريبية للموظفين
    يمكن استبدال هذه الدالة بقراءة ملف Excel: pd.read_excel('employees.xlsx')
    """
    random.seed(42)
    np.random.seed(42)

    names = [
        "أحمد محمد العتيبي", "خالد سعد الغامدي", "فهد عبدالله القحطاني",
        "محمد علي الزهراني", "عبدالرحمن يوسف الشهري", "سعد ناصر العمري",
        "نواف تركي الدوسري", "بندر عمر الحربي", "فيصل سلطان المالكي",
        "عبدالعزيز حمد البقمي", "راجيف كومار", "سانجاي باتيل",
        "محمد عبدالله سيدي", "أمادو دياللو", "جون مواليمو",
        "رامي حسن", "كريم يوسف", "علي حمدان"
    ]

    nationalities = (
        ["سعودي"] * 8 + ["هندي"] * 4 + ["أفريقي"] * 3 + ["مصري"] * 3
    )

    job_titles = [
        "مدير فرع", "مشرف", "باريستا", "محمّص قهوة",
        "كاشير", "موظف مستودع", "سائق توصيل", "موظف مبيعات"
    ]

    contract_types = ["دوام كامل", "دوام جزئي", "مؤقت"]

    today = datetime.today()
    employees = []

    for i, name in enumerate(names):
        start_date = today - timedelta(days=random.randint(30, 1800))
        # بعض الموظفين لديهم إقامات قريبة الانتهاء
        iqama_days = random.choice([20, 45, 90, 180, 365, 500])
        insurance_days = random.choice([15, 50, 100, 200, 400])

        employees.append({
            "EmployeeID": f"EMP{1000 + i}",
            "الاسم": name,
            "الجنسية": nationalities[i],
            "العمر": random.randint(22, 55),
            "المسمى الوظيفي": random.choice(job_titles),
            "نوع العقد": random.choice(contract_types),
            "تاريخ بداية العمل": start_date.strftime("%Y-%m-%d"),
            "تاريخ انتهاء الإقامة": (today + timedelta(days=iqama_days)).strftime("%Y-%m-%d"),
            "حالة التأمين الطبي": random.choice(["نشط", "منتهي", "معلق"]),
            "رقم التأمين": f"INS{random.randint(100000, 999999)}",
            "تاريخ انتهاء التأمين": (today + timedelta(days=insurance_days)).strftime("%Y-%m-%d"),
        })

    return pd.DataFrame(employees)


def generate_work_system(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    توليد بيانات نظام العمل لكل موظف
    يمكن استبدالها بـ: pd.read_excel('work_system.xlsx')
    """
    random.seed(42)
    records = []
    today = datetime.today()

    for _, emp in employees_df.iterrows():
        for week_offset in range(12):  # آخر 12 أسبوع
            week_start = today - timedelta(weeks=week_offset)
            records.append({
                "EmployeeID": emp["EmployeeID"],
                "الاسم": emp["الاسم"],
                "نوع الدوام": emp["نوع العقد"],
                "عدد ساعات العمل": round(random.uniform(20, 48), 1),
                "أيام العمل الأسبوعية": random.randint(3, 6),
                "أيام الإجازة": random.randint(0, 2),
                "أيام الحضور": random.randint(3, 6),
                "أيام الغياب": random.randint(0, 3),
                "الأسبوع": week_start.strftime("%Y-W%U"),
                "تاريخ البداية": week_start.strftime("%Y-%m-%d"),
            })

    return pd.DataFrame(records)


def generate_sales() -> pd.DataFrame:
    """
    توليد بيانات المبيعات
    يمكن استبدالها بـ: pd.read_excel('sales.xlsx')
    """
    random.seed(42)
    branches = ["فرع الرياض - العليا", "فرع الرياض - النخيل", "فرع جدة", "فرع الدمام"]
    products = [
        "قهوة عربية", "إسبريسو", "لاتيه", "كابتشينو",
        "قهوة مختصة", "بن محمص", "هيل", "زعفران"
    ]

    today = datetime.today()
    sales = []

    for i in range(1200):
        sale_date = today - timedelta(days=random.randint(0, 180))
        qty = random.randint(1, 20)
        price = round(random.uniform(15, 150), 2)
        sales.append({
            "SaleID": f"SALE{10000 + i}",
            "التاريخ": sale_date.strftime("%Y-%m-%d"),
            "الشهر": sale_date.strftime("%Y-%m"),
            "اليوم": sale_date.strftime("%A"),
            "الفرع": random.choice(branches),
            "نوع المنتج": random.choice(products),
            "الكمية": qty,
            "سعر البيع": price,
            "إجمالي المبيعات": round(qty * price, 2),
            "الموظف المسؤول": f"EMP{random.randint(1000, 1017)}",
        })

    return pd.DataFrame(sales)
