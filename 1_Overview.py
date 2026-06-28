# =====================================================
# ملف: 1_Overview.py
# الوصف: لوحة النظرة العامة - ملخص شامل للمحمصة
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.helpers import card_metric, HADAB_COLORS, CHART_PALETTE, format_number

st.set_page_config(page_title="هدب - النظرة العامة", layout="wide", page_icon="☕")

# --- استدعاء البيانات من الجلسة ---
employees = st.session_state.get("employees", pd.DataFrame())
sales     = st.session_state.get("sales", pd.DataFrame())
work      = st.session_state.get("work", pd.DataFrame())

if employees.empty:
    st.warning("⚠️ يرجى الانتقال للصفحة الرئيسية أولاً لتحميل البيانات.")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
* { font-family: 'Tajawal', sans-serif !important; direction: rtl; }
.stMetric { background: white; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<h1 style="color:{HADAB_COLORS['primary']};font-size:32px;margin-bottom:4px">
    ☕ لوحة النظرة العامة — محمصة هدب
</h1>
<p style="color:{HADAB_COLORS['muted']};margin-top:0">تحديث مباشر للمؤشرات الرئيسية</p>
<hr style="border:1px solid #F3E8DC;margin-bottom:20px">
""", unsafe_allow_html=True)

# ========== بطاقات الإحصاءات الرئيسية ==========
col1, col2, col3, col4 = st.columns(4)
total_sales = sales["إجمالي المبيعات"].sum() if not sales.empty else 0
total_emp   = len(employees)
today_sales = sales[sales["التاريخ"] == pd.Timestamp.today().strftime("%Y-%m-%d")]["إجمالي المبيعات"].sum() if not sales.empty else 0

with col1:
    card_metric("👥 إجمالي الموظفين", format_number(total_emp), color=HADAB_COLORS["primary"])
with col2:
    card_metric("💰 إجمالي المبيعات", format_number(total_sales, currency=True), color=HADAB_COLORS["secondary"])
with col3:
    card_metric("📦 إجمالي الطلبات", format_number(len(sales)), color=HADAB_COLORS["accent"])
with col4:
    branches = sales["الفرع"].nunique() if not sales.empty else 0
    card_metric("🏪 عدد الفروع", format_number(branches), color="#78350F")

st.markdown("<br>", unsafe_allow_html=True)

# ========== المبيعات اليومية - Line Chart ==========
st.markdown(f"### 📈 المبيعات اليومية")
daily = (
    sales.groupby("التاريخ")["إجمالي المبيعات"]
    .sum()
    .reset_index()
    .sort_values("التاريخ")
)
fig_line = px.area(
    daily, x="التاريخ", y="إجمالي المبيعات",
    color_discrete_sequence=[HADAB_COLORS["primary"]],
    labels={"التاريخ": "التاريخ", "إجمالي المبيعات": "المبيعات (ريال)"},
)
fig_line.update_layout(
    plot_bgcolor="white", paper_bgcolor="white",
    font_family="Tajawal",
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor="#F3E8DC"),
    margin=dict(t=20, b=20),
)
st.plotly_chart(fig_line, use_container_width=True)

# ========== رسومات بيانية للموظفين ==========
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 🌍 توزيع الموظفين حسب الجنسية")
    nat_counts = employees["الجنسية"].value_counts().reset_index()
    nat_counts.columns = ["الجنسية", "العدد"]
    fig_pie = px.pie(
        nat_counts, names="الجنسية", values="العدد",
        color_discrete_sequence=CHART_PALETTE,
        hole=0.4,
    )
    fig_pie.update_layout(font_family="Tajawal", margin=dict(t=10, b=10))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_b:
    st.markdown("### 📊 توزيع الموظفين حسب الفئة العمرية")
    bins   = [18, 25, 35, 45, 60]
    labels = ["18-25", "26-35", "36-45", "46-60"]
    employees["الفئة العمرية"] = pd.cut(employees["العمر"], bins=bins, labels=labels)
    age_counts = employees["الفئة العمرية"].value_counts().sort_index().reset_index()
    age_counts.columns = ["الفئة العمرية", "العدد"]
    fig_bar = px.bar(
        age_counts, x="الفئة العمرية", y="العدد",
        color_discrete_sequence=[HADAB_COLORS["primary"]],
        text="العدد",
    )
    fig_bar.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="Tajawal",
        yaxis=dict(gridcolor="#F3E8DC"),
        margin=dict(t=10, b=10),
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

# ========== المبيعات الشهرية ==========
st.markdown("### 📅 المبيعات الشهرية")
monthly = (
    sales.groupby("الشهر")["إجمالي المبيعات"]
    .sum()
    .reset_index()
    .sort_values("الشهر")
)
fig_monthly = px.bar(
    monthly, x="الشهر", y="إجمالي المبيعات",
    color_discrete_sequence=[HADAB_COLORS["secondary"]],
    text_auto=".2s",
    labels={"الشهر": "الشهر", "إجمالي المبيعات": "المبيعات (ريال)"},
)
fig_monthly.update_layout(
    plot_bgcolor="white", paper_bgcolor="white",
    font_family="Tajawal",
    yaxis=dict(gridcolor="#F3E8DC"),
    margin=dict(t=10, b=10),
)
st.plotly_chart(fig_monthly, use_container_width=True)
