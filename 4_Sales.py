# =====================================================
# ملف: 4_Sales.py
# الوصف: لوحة المبيعات - تحليل شامل للمبيعات والمنتجات والفروع
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.helpers import HADAB_COLORS, CHART_PALETTE, card_metric, format_number

st.set_page_config(page_title="هدب - المبيعات", layout="wide", page_icon="💰")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
* { font-family: 'Tajawal', sans-serif !important; direction: rtl; }
</style>
""", unsafe_allow_html=True)

# --- تحميل البيانات ---
sales = st.session_state.get("sales", pd.DataFrame())
if sales.empty:
    st.warning("⚠️ يرجى الانتقال للصفحة الرئيسية أولاً لتحميل البيانات.")
    st.stop()

sales["التاريخ"] = pd.to_datetime(sales["التاريخ"])

st.markdown(f"""
<h1 style="color:{HADAB_COLORS['primary']};font-size:32px;margin-bottom:4px">
    💰 لوحة المبيعات — محمصة هدب
</h1>
<hr style="border:1px solid #F3E8DC;margin-bottom:20px">
""", unsafe_allow_html=True)

# ========== فلاتر ==========
st.markdown("### 🔍 فلاتر البحث")
f1, f2, f3, f4 = st.columns(4)

with f1:
    branch_options = ["الكل"] + sorted(sales["الفرع"].unique().tolist())
    sel_branch = st.selectbox("الفرع", branch_options)

with f2:
    product_options = ["الكل"] + sorted(sales["نوع المنتج"].unique().tolist())
    sel_product = st.selectbox("نوع المنتج", product_options)

with f3:
    min_date = sales["التاريخ"].min().date()
    max_date = sales["التاريخ"].max().date()
    date_range = st.date_input("نطاق التاريخ", [min_date, max_date])

with f4:
    view_by = st.selectbox("عرض المبيعات حسب", ["اليوم", "الأسبوع", "الشهر"])

# تطبيق الفلاتر
filtered = sales.copy()
if sel_branch != "الكل":
    filtered = filtered[filtered["الفرع"] == sel_branch]
if sel_product != "الكل":
    filtered = filtered[filtered["نوع المنتج"] == sel_product]
if len(date_range) == 2:
    filtered = filtered[
        (filtered["التاريخ"].dt.date >= date_range[0]) &
        (filtered["التاريخ"].dt.date <= date_range[1])
    ]

# ========== بطاقات ملخص ==========
col1, col2, col3, col4 = st.columns(4)
total   = filtered["إجمالي المبيعات"].sum()
orders  = len(filtered)
avg_ord = total / orders if orders > 0 else 0
top_p   = filtered.groupby("نوع المنتج")["إجمالي المبيعات"].sum().idxmax() if not filtered.empty else "-"

with col1:
    card_metric("💰 إجمالي المبيعات", format_number(total, currency=True), color=HADAB_COLORS["primary"])
with col2:
    card_metric("📦 عدد الطلبات", format_number(orders), color=HADAB_COLORS["secondary"])
with col3:
    card_metric("📊 متوسط قيمة الطلب", format_number(avg_ord, currency=True), color=HADAB_COLORS["accent"])
with col4:
    card_metric("🏆 أفضل منتج", top_p, color="#78350F")

st.markdown("<br>", unsafe_allow_html=True)

# ========== رسم المبيعات الزمنية ==========
st.markdown(f"### 📈 المبيعات حسب {view_by}")

if view_by == "اليوم":
    time_group = filtered.groupby(filtered["التاريخ"].dt.date)["إجمالي المبيعات"].sum().reset_index()
    time_group.columns = ["الفترة", "المبيعات"]
elif view_by == "الأسبوع":
    filtered["الأسبوع"] = filtered["التاريخ"].dt.to_period("W").astype(str)
    time_group = filtered.groupby("الأسبوع")["إجمالي المبيعات"].sum().reset_index()
    time_group.columns = ["الفترة", "المبيعات"]
else:
    time_group = filtered.groupby("الشهر")["إجمالي المبيعات"].sum().reset_index()
    time_group.columns = ["الفترة", "المبيعات"]

fig_time = px.area(
    time_group, x="الفترة", y="المبيعات",
    color_discrete_sequence=[HADAB_COLORS["primary"]],
    labels={"الفترة": "الفترة", "المبيعات": "المبيعات (ريال)"},
)
fig_time.update_layout(
    plot_bgcolor="white", paper_bgcolor="white",
    font_family="Tajawal",
    xaxis=dict(showgrid=False, tickangle=-45),
    yaxis=dict(gridcolor="#F3E8DC"),
    margin=dict(t=10, b=30),
)
st.plotly_chart(fig_time, use_container_width=True)

# ========== أفضل المنتجات + مقارنة الفروع ==========
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 🏆 أفضل المنتجات مبيعاً")
    prod_sales = (
        filtered.groupby("نوع المنتج")["إجمالي المبيعات"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_prod = px.bar(
        prod_sales, x="إجمالي المبيعات", y="نوع المنتج",
        orientation="h",
        color="نوع المنتج",
        color_discrete_sequence=CHART_PALETTE,
        text_auto=".2s",
    )
    fig_prod.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="Tajawal",
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_prod, use_container_width=True)

with col_b:
    st.markdown("### 🏪 مقارنة المبيعات بين الفروع")
    branch_sales = (
        filtered.groupby("الفرع")["إجمالي المبيعات"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_branch = px.pie(
        branch_sales, names="الفرع", values="إجمالي المبيعات",
        color_discrete_sequence=CHART_PALETTE, hole=0.4,
    )
    fig_branch.update_layout(font_family="Tajawal")
    st.plotly_chart(fig_branch, use_container_width=True)

# ========== مقارنة الفروع بالأشهر - Heatmap ==========
st.markdown("### 🗺️ خريطة حرارية - مبيعات الفروع عبر الأشهر")
filtered["شهر_نصي"] = filtered["التاريخ"].dt.strftime("%Y-%m")
pivot = filtered.pivot_table(
    index="الفرع", columns="شهر_نصي",
    values="إجمالي المبيعات", aggfunc="sum", fill_value=0
)
fig_heat = px.imshow(
    pivot,
    color_continuous_scale=["#FFF8F2", "#E07820", "#8B3A00"],
    labels={"color": "المبيعات (ريال)", "x": "الشهر", "y": "الفرع"},
    aspect="auto",
)
fig_heat.update_layout(
    font_family="Tajawal",
    margin=dict(t=10, b=10),
    coloraxis_colorbar=dict(title="المبيعات"),
)
st.plotly_chart(fig_heat, use_container_width=True)

# ========== جدول المبيعات التفاعلي ==========
st.markdown("### 📋 جدول المبيعات التفصيلي")
display_sales = filtered.copy()
display_sales["التاريخ"] = display_sales["التاريخ"].dt.strftime("%Y-%m-%d")
display_sales["إجمالي المبيعات"] = display_sales["إجمالي المبيعات"].apply(
    lambda x: f"{x:,.2f} ريال"
)
display_sales["سعر البيع"] = display_sales["سعر البيع"].apply(
    lambda x: f"{x:,.2f} ريال"
)
st.dataframe(
    display_sales[[
        "SaleID", "التاريخ", "الفرع", "نوع المنتج",
        "الكمية", "سعر البيع", "إجمالي المبيعات"
    ]],
    use_container_width=True,
    height=400,
)

# زر تحميل البيانات
csv = filtered.to_csv(index=False, encoding="utf-8-sig")
st.download_button(
    "⬇️ تحميل البيانات CSV",
    data=csv,
    file_name="hadab_sales.csv",
    mime="text/csv",
)
