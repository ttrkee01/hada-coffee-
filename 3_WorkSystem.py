# =====================================================
# ملف: 3_WorkSystem.py
# الوصف: لوحة نظام العمل - الحضور والغياب وساعات العمل
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.helpers import HADAB_COLORS, CHART_PALETTE, card_metric, format_number

st.set_page_config(page_title="هدب - نظام العمل", layout="wide", page_icon="⏰")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
* { font-family: 'Tajawal', sans-serif !important; direction: rtl; }
</style>
""", unsafe_allow_html=True)

# --- تحميل البيانات ---
work      = st.session_state.get("work", pd.DataFrame())
employees = st.session_state.get("employees", pd.DataFrame())

if work.empty:
    st.warning("⚠️ يرجى الانتقال للصفحة الرئيسية أولاً لتحميل البيانات.")
    st.stop()

st.markdown(f"""
<h1 style="color:{HADAB_COLORS['primary']};font-size:32px;margin-bottom:4px">
    ⏰ لوحة نظام العمل — محمصة هدب
</h1>
<hr style="border:1px solid #F3E8DC;margin-bottom:20px">
""", unsafe_allow_html=True)

# ========== ملخص إجمالي ==========
avg_hours   = work["عدد ساعات العمل"].mean()
avg_attend  = work["أيام الحضور"].mean()
total_absent = work["أيام الغياب"].sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    card_metric("⏱️ متوسط ساعات العمل الأسبوعية", f"{avg_hours:.1f} ساعة", color=HADAB_COLORS["primary"])
with col2:
    card_metric("✅ متوسط أيام الحضور", f"{avg_attend:.1f} يوم", color=HADAB_COLORS["secondary"])
with col3:
    card_metric("❌ إجمالي أيام الغياب", format_number(int(total_absent)), color=HADAB_COLORS["danger"] if total_absent > 50 else "#16A34A")
with col4:
    card_metric("📅 عدد الأسابيع المرصودة", format_number(work["الأسبوع"].nunique()), color=HADAB_COLORS["accent"])

st.markdown("<br>", unsafe_allow_html=True)

# ========== فلتر الأسبوع ==========
weeks = sorted(work["الأسبوع"].unique().tolist(), reverse=True)
sel_week = st.selectbox("🗓️ اختر الأسبوع", ["كل الأسابيع"] + weeks)

filtered_work = work if sel_week == "كل الأسابيع" else work[work["الأسبوع"] == sel_week]

# ========== جدول متوسط ساعات العمل لكل موظف ==========
st.markdown("### 📊 متوسط ساعات العمل لكل موظف")

emp_hours = (
    filtered_work.groupby(["EmployeeID", "الاسم"])
    .agg(
        متوسط_الساعات=("عدد ساعات العمل", "mean"),
        إجمالي_الغياب=("أيام الغياب", "sum"),
        إجمالي_الحضور=("أيام الحضور", "sum"),
    )
    .reset_index()
    .sort_values("متوسط_الساعات", ascending=False)
)
emp_hours["متوسط_الساعات"] = emp_hours["متوسط_الساعات"].round(1)

# تلوين الموظفين ذوي الغياب العالي
def color_absence(val):
    if val > 5:
        return "color: #DC2626; font-weight: bold"
    elif val > 3:
        return "color: #D97706"
    return ""

styled_hours = emp_hours.style.applymap(color_absence, subset=["إجمالي_الغياب"])
st.dataframe(styled_hours, use_container_width=True, height=350)

st.markdown("<br>", unsafe_allow_html=True)

# ========== رسومات ==========
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### ⏱️ توزيع ساعات العمل الأسبوعية")
    fig_hours = px.histogram(
        filtered_work, x="عدد ساعات العمل", nbins=15,
        color_discrete_sequence=[HADAB_COLORS["primary"]],
        labels={"عدد ساعات العمل": "الساعات الأسبوعية", "count": "التكرار"},
    )
    fig_hours.add_vline(
        x=filtered_work["عدد ساعات العمل"].mean(),
        line_dash="dash", line_color=HADAB_COLORS["danger"],
        annotation_text="المتوسط", annotation_position="top right"
    )
    fig_hours.update_layout(plot_bgcolor="white", paper_bgcolor="white", font_family="Tajawal")
    st.plotly_chart(fig_hours, use_container_width=True)

with col_b:
    st.markdown("### 📉 الموظفون الأكثر غياباً")
    top_absent = (
        filtered_work.groupby("الاسم")["أيام الغياب"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig_absent = px.bar(
        top_absent, x="أيام الغياب", y="الاسم",
        orientation="h",
        color_discrete_sequence=[HADAB_COLORS["danger"]],
        text="أيام الغياب",
    )
    fig_absent.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="Tajawal", yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_absent, use_container_width=True)

# ========== اتجاه الحضور والغياب الأسبوعي ==========
st.markdown("### 📅 اتجاه الحضور والغياب الأسبوعي")
weekly_trend = (
    work.groupby("الأسبوع")
    .agg(إجمالي_الحضور=("أيام الحضور", "sum"), إجمالي_الغياب=("أيام الغياب", "sum"))
    .reset_index()
    .sort_values("الأسبوع")
)

fig_trend = go.Figure()
fig_trend.add_trace(go.Bar(
    x=weekly_trend["الأسبوع"], y=weekly_trend["إجمالي_الحضور"],
    name="الحضور", marker_color=HADAB_COLORS["primary"]
))
fig_trend.add_trace(go.Bar(
    x=weekly_trend["الأسبوع"], y=weekly_trend["إجمالي_الغياب"],
    name="الغياب", marker_color=HADAB_COLORS["danger"]
))
fig_trend.update_layout(
    barmode="group",
    plot_bgcolor="white", paper_bgcolor="white",
    font_family="Tajawal",
    xaxis=dict(tickangle=-45),
    yaxis=dict(gridcolor="#F3E8DC"),
    legend=dict(orientation="h", y=1.1),
    margin=dict(t=30, b=30),
)
st.plotly_chart(fig_trend, use_container_width=True)

# ========== نوع الدوام ==========
st.markdown("### 📋 توزيع نوع الدوام")
daw_chart = filtered_work.drop_duplicates("EmployeeID")["نوع الدوام"].value_counts().reset_index()
daw_chart.columns = ["نوع الدوام", "العدد"]
fig_daw = px.pie(daw_chart, names="نوع الدوام", values="العدد",
                 color_discrete_sequence=CHART_PALETTE, hole=0.35)
fig_daw.update_layout(font_family="Tajawal")
col_c, col_d = st.columns([1, 2])
with col_c:
    st.plotly_chart(fig_daw, use_container_width=True)
with col_d:
    st.markdown("""
    <div style="padding:20px;background:#FFF8F2;border-radius:12px;margin-top:20px">
    <h4 style="color:#C2570A">📌 ملاحظات</h4>
    <ul>
      <li>الغياب الزائد عن 5 أيام يظهر باللون الأحمر</li>
      <li>استخدم فلتر الأسابيع للتحقق من أداء أسبوع بعينه</li>
      <li>يمكن ربط هذه البيانات بنظام الحضور الآلي (Fingerprint/Face ID)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
