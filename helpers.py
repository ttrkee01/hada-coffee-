# =====================================================
# ملف: helpers.py
# الوصف: دوال مساعدة مشتركة للداشبورد
# =====================================================

import pandas as pd
from datetime import datetime, timedelta
import streamlit as st


def days_until(date_str: str) -> int:
    """حساب عدد الأيام المتبقية حتى تاريخ معين"""
    try:
        target = datetime.strptime(str(date_str), "%Y-%m-%d")
        return (target - datetime.today()).days
    except Exception:
        return 9999


def highlight_expiry(row: pd.Series, col: str, days_warn: int = 60) -> list:
    """
    تلوين الصفوف بناءً على قرب انتهاء الصلاحية
    - أحمر: أقل من 30 يوم
    - برتقالي: أقل من 60 يوم
    - أخضر: أكثر من 60 يوم
    """
    days = days_until(row[col])
    if days < 0:
        color = "background-color: #FFCCCC"   # منتهي
    elif days <= 30:
        color = "background-color: #FF9999"   # حرج
    elif days <= 60:
        color = "background-color: #FFE0A3"   # تحذير
    else:
        color = ""
    return [color] * len(row)


def format_number(n: float, currency: bool = False) -> str:
    """تنسيق الأرقام بالفواصل"""
    if currency:
        return f"{n:,.2f} ريال"
    return f"{n:,}"


def card_metric(title: str, value: str, delta: str = None, color: str = "#B45309"):
    """عرض بطاقة إحصائية"""
    delta_html = f"<p style='color:#16a34a;font-size:13px;margin:0'>{delta}</p>" if delta else ""
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 5px solid {color};
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 8px;
    ">
        <p style="color:#6B7280;font-size:13px;margin:0;font-family:'Tajawal',sans-serif">{title}</p>
        <h2 style="color:#1F2937;font-size:28px;margin:4px 0;font-weight:700">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


HADAB_COLORS = {
    "primary":   "#C2570A",   # برتقالي محمصة هدب
    "secondary": "#E07820",
    "accent":    "#8B3A00",
    "bg":        "#FFF8F2",
    "card":      "#FFFFFF",
    "text":      "#1F2937",
    "muted":     "#6B7280",
    "success":   "#16A34A",
    "warning":   "#D97706",
    "danger":    "#DC2626",
}

CHART_PALETTE = [
    "#C2570A", "#E07820", "#8B3A00",
    "#F59E0B", "#92400E", "#FCD34D",
    "#78350F", "#FBBF24",
]
