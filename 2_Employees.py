# =====================================================
# ملف: 2_Employees.py
# الوصف: لوحة الموظفين - إدارة وتتبع بيانات الموظفين
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.helpers import days_until, HADAB_COLORS, CHART_PALETTE, card_metric, format_number

st.set_page_config(page_title="هدب - الموظفين", layout="wide", page_icon="👥")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
* { font-family: 'Tajawal', sans-serif !important; direction: rtl; }
</style>
""", unsafe_allow_html=True)

# --- تحميل البيانات ---
employees = st.session_state.get("employees", pd.DataFrame())
if employees.empty:
    st.warning("⚠️ يرجى الانتقال للصفحة الرئيسية أولاً لتحميل البيانات.")
    st.stop()

st.markdown(f"""
<h1 style="color:{HADAB_COLORS['primary']};font-size:32px;margin-bottom:4px">
    👥 لوحة الموظفين — محمصة هدب
</h1>
<hr style="border:1px solid #F3E8DC;margin-bottom:20px">
""", unsafe_allow_html=True)

# ========== حساب الأيام المتبقية ==========
df = employees.copy()
df["أيام انتهاء الإقامة"]  = df["تاريخ انتهاء الإقامة"].apply(days_until)
df["أيام انتهاء التأمين"]  = df["تاريخ انتهاء التأمين"].apply(days_until)

# ========== تنبيهات الانتهاء ==========
iqama_warn    = df[df["أيام انتهاء الإقامة"] <= 60]
insurance_warn = df[df["أيام انتهاء التأمين"] <= 60]

if not iqama_warn.empty:
    st.error(f"🚨 **{len(iqama_warn)} موظف** إقامتهم تنتهي خلال 60 يوماً!")
if not insurance_warn.empty:
    st.warning(f"⚠️ **{len(insurance_warn)} موظف** تأمينهم الطبي ينتهي خلال 60 يوماً!")

st.markdown("<br>", unsafe_allow_html=True)

# ========== بطاقات ملخص ==========
col1, col2, col3, col4 = st.columns(4)
with col1:
    card_metric("👥 إجمالي الموظفين", format_number(len(df)), color=HADAB_COLORS["primary"])
with col2:
    saudis = len(df[df["الجنسية"] == "سعودي"])
    card_metric("🇸🇦 السعوديون", format_number(saudis), color=HADAB_COLORS["secondary"])
with col3:
    card_metric("🚨 إقامات تنتهي قريباً", format_number(len(iqama_warn)), color=HADAB_COLORS["danger"] if len(iqama_warn) > 0 else "#16A34A")
with col4:
    card_metric("⚕️ تأمينات تنتهي قريباً", format_number(len(insurance_warn)), color="#D97706" if len(insurance_warn) > 0 else "#16A34A")

st.markdown("<br>", unsafe_allow_html=True)

# ========== فلاتر التصفية ==========
st.markdown("### 🔍 تصفية الموظفين")
f1, f2, f3, f4 = st.columns(4)

with f1:
    nat_options = ["الكل"] + sorted(df["الجنسية"].unique().tolist())
    sel_nat = st.selectbox("الجنسية", nat_options)

with f2:
    job_options = ["الكل"] + sorted(df["المسمى الوظيفي"].unique().tolist())
    sel_job = st.selectbox("المسمى الوظيفي", job_options)

with f3:
    contract_options = ["الكل"] + sorted(df["نوع العقد"].unique().tolist())
    sel_contract = st.selectbox("نوع العقد", contract_options)

with f4:
    age_range = st.slider("نطاق العمر", int(df["العمر"].min()), int(df["العمر"].max()),
                          (int(df["العمر"].min()), int(df["العمر"].max())))

# تطبيق الفلاتر
filtered = df.copy()
if sel_nat != "الكل":
    filtered = filtered[filtered["الجنسية"] == sel_nat]
if sel_job != "الكل":
    filtered = filtered[filtered["المسمى الوظيفي"] == sel_job]
if sel_contract != "الكل":
    filtered = filtered[filtered["نوع العقد"] == sel_contract]
filtered = filtered[(filtered["العمر"] >= age_range[0]) & (filtered["العمر"] <= age_range[1])]

# ========== تلوين الجدول حسب الانتهاء ==========
def color_row(row):
    """تلوين الصفوف بناءً على أقرب تاريخ انتهاء"""
    iqama   = row["أيام انتهاء الإقامة"]
    insur   = row["أيام انتهاء التأمين"]
    min_days = min(iqama, insur)

    if min_days < 0:
        bg = "background-color: #FFCCCC"   # منتهي - أحمر
    elif min_days <= 30:
        bg = "background-color: #FFB3B3"   # حرج - أحمر فاتح
    elif min_days <= 60:
        bg = "background-color: #FFF3CD"   # تحذير - أصفر
    else:
        bg = ""
    return [bg] * len(row)

st.markdown(f"### 📋 جدول الموظفين ({len(filtered)} موظف)")

display_cols = [
    "EmployeeID", "الاسم", "الجنسية", "العمر",
    "المسمى الوظيفي", "نوع العقد",
    "تاريخ انتهاء الإقامة", "أيام انتهاء الإقامة",
    "حالة التأمين الطبي", "تاريخ انتهاء التأمين", "أيام انتهاء التأمين"
]

styled = (
    filtered[display_cols]
    .style.apply(color_row, axis=1)
    .format({"أيام انتهاء الإقامة": "{:.0f} يوم", "أيام انتهاء التأمين": "{:.0f} يوم"})
)
st.dataframe(styled, use_container_width=True, height=400)

# مفتاح الألوان
st.markdown("""
<div style="display:flex;gap:16px;margin-top:8px;font-size:13px">
  <span>🔴 <b>أحمر:</b> أقل من 30 يوم أو منتهي</span>
  <span>🟡 <b>أصفر:</b> 30-60 يوم</span>
  <span>⚪ <b>عادي:</b> أكثر من 60 يوم</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ========== رسومات الموظفين ==========
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 🌍 الموظفون حسب الجنسية")
    nat_chart = df["الجنسية"].value_counts().reset_index()
    nat_chart.columns = ["الجنسية", "العدد"]
    fig = px.bar(nat_chart, x="الجنسية", y="العدد",
                 color_discrete_sequence=[HADAB_COLORS["primary"]], text="العدد")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                      font_family="Tajawal", yaxis=dict(gridcolor="#F3E8DC"))
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.markdown("### 📄 الموظفون حسب نوع العقد")
    contract_chart = df["نوع العقد"].value_counts().reset_index()
    contract_chart.columns = ["نوع العقد", "العدد"]
    fig2 = px.pie(contract_chart, names="نوع العقد", values="العدد",
                  color_discrete_sequence=CHART_PALETTE, hole=0.4)
    fig2.update_layout(font_family="Tajawal")
    st.plotly_chart(fig2, use_container_width=True)

# ========== قسم التنبيهات التفصيلية ==========
with st.expander("🚨 تفاصيل الموظفين ذوي الإقامات المنتهية قريباً"):
    if iqama_warn.empty:
        st.success("✅ لا توجد إقامات منتهية خلال الـ 60 يوم القادمة")
    else:
        st.dataframe(
            iqama_warn[["الاسم", "الجنسية", "المسمى الوظيفي",
                        "تاريخ انتهاء الإقامة", "أيام انتهاء الإقامة"]],
            use_container_width=True
        )

with st.expander("⚕️ تفاصيل الموظفين ذوي التأمين المنتهي قريباً"):
    if insurance_warn.empty:
        st.success("✅ لا توجد تأمينات منتهية خلال الـ 60 يوم القادمة")
    else:
        st.dataframe(
            insurance_warn[["الاسم", "الجنسية", "المسمى الوظيفي",
                           "حالة التأمين الطبي", "تاريخ انتهاء التأمين", "أيام انتهاء التأمين"]],
            use_container_width=True
        )
