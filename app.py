# =====================================================
# ملف: app.py
# الوصف: الصفحة الرئيسية لداشبورد محمصة هدب
# يعمل كنقطة تحميل البيانات المركزية للتطبيق
# =====================================================

import streamlit as st
import pandas as pd
import sys, os

# إضافة مسار المشروع للاستيراد
sys.path.append(os.path.dirname(__file__))
from data.sample_data import generate_employees, generate_work_system, generate_sales
from utils.helpers import HADAB_COLORS

# ========== إعدادات الصفحة ==========
st.set_page_config(
    page_title="محمصة هدب — داشبورد",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========== CSS مخصص ==========
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap');

/* تطبيق الخط العربي على كل العناصر */
* {{
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
}}

/* الشريط الجانبي */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {HADAB_COLORS['accent']} 0%, {HADAB_COLORS['primary']} 100%);
}}
[data-testid="stSidebar"] * {{
    color: white !important;
}}

/* خلفية التطبيق */
.stApp {{
    background-color: {HADAB_COLORS['bg']};
}}

/* أزرار */
.stButton > button {{
    background-color: {HADAB_COLORS['primary']};
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Tajawal', sans-serif;
    font-weight: 600;
}}
.stButton > button:hover {{
    background-color: {HADAB_COLORS['accent']};
}}
</style>
""", unsafe_allow_html=True)

# ========== تحميل البيانات في الذاكرة المشتركة ==========
@st.cache_data
def load_data():
    """
    تحميل جميع البيانات مرة واحدة وتخزينها مؤقتاً
    لاستبدال البيانات الحقيقية: عدّل هذه الدالة لقراءة Excel أو قاعدة بيانات
    
    مثال للاستخدام مع Excel:
        employees = pd.read_excel("data/employees.xlsx")
        work      = pd.read_excel("data/work_system.xlsx")
        sales     = pd.read_excel("data/sales.xlsx")
    """
    employees = generate_employees()
    work      = generate_work_system(employees)
    sales     = generate_sales()
    return employees, work, sales

employees, work, sales = load_data()

# حفظ البيانات في الجلسة لتكون متاحة في جميع الصفحات
st.session_state["employees"] = employees
st.session_state["work"]      = work
st.session_state["sales"]     = sales

# ========== الشريط الجانبي ==========
with st.sidebar:
    # شعار المحمصة
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px">
        <h1 style="font-size:42px;margin:0">☕</h1>
        <h2 style="margin:4px 0;font-size:22px;color:white">محمصة هدب</h2>
        <p style="color:#FFD9B8;font-size:13px;margin:0">Hadab Roastery</p>
    </div>
    <hr style="border:1px solid rgba(255,255,255,0.2);margin:10px 0">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#FFD9B8;font-size:13px;padding:10px 0">
        <p>📌 <b>الصفحات المتاحة:</b></p>
        <ul style="margin:0;padding-right:16px">
            <li>🏠 الرئيسية</li>
            <li>📊 النظرة العامة</li>
            <li>👥 الموظفون</li>
            <li>⏰ نظام العمل</li>
            <li>💰 المبيعات</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.2)'>", unsafe_allow_html=True)

    # زر تحديث البيانات
    if st.button("🔄 تحديث البيانات"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("""
    <div style="color:#FFD9B8;font-size:12px;padding-top:10px;text-align:center">
        الإصدار 1.0.0<br>
        © 2025 محمصة هدب
    </div>
    """, unsafe_allow_html=True)

# ========== المحتوى الرئيسي ==========
st.markdown(f"""
<div style="text-align:center;padding:40px 20px 20px">
    <h1 style="color:{HADAB_COLORS['primary']};font-size:48px;margin-bottom:8px">☕ محمصة هدب</h1>
    <h2 style="color:{HADAB_COLORS['secondary']};font-size:24px;font-weight:400;margin-bottom:20px">
        نظام إدارة وتحليل البيانات
    </h2>
    <p style="color:{HADAB_COLORS['muted']};font-size:16px;max-width:600px;margin:0 auto">
        مرحباً بك في لوحة تحكم محمصة هدب. استخدم القائمة الجانبية للتنقل بين الأقسام المختلفة.
    </p>
</div>
""", unsafe_allow_html=True)

# ========== بطاقات الملاحة ==========
col1, col2, col3, col4 = st.columns(4)

nav_cards = [
    ("📊", "النظرة العامة", "ملخص شامل للمؤشرات الرئيسية", HADAB_COLORS["primary"]),
    ("👥", "الموظفون",     "إدارة بيانات وتنبيهات الموظفين", HADAB_COLORS["secondary"]),
    ("⏰", "نظام العمل",  "الحضور والغياب وساعات العمل",    HADAB_COLORS["accent"]),
    ("💰", "المبيعات",    "تحليل مبيعات المنتجات والفروع",   "#78350F"),
]

for col, (icon, title, desc, color) in zip([col1, col2, col3, col4], nav_cards):
    with col:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 28px 20px;
            text-align: center;
            border-top: 5px solid {color};
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            margin: 8px 0;
            cursor: pointer;
        ">
            <div style="font-size:40px;margin-bottom:12px">{icon}</div>
            <h3 style="color:{color};margin:0 0 8px;font-size:18px">{title}</h3>
            <p style="color:{HADAB_COLORS['muted']};font-size:13px;margin:0">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ========== إحصاءات سريعة ==========
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<h2 style="color:{HADAB_COLORS['primary']};text-align:center;margin-bottom:20px">
    📌 إحصاءات سريعة
</h2>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    ("👥 الموظفون", len(employees), ""),
    ("💰 إجمالي المبيعات", f"{sales['إجمالي المبيعات'].sum():,.0f}", "ريال"),
    ("📦 الطلبات", f"{len(sales):,}", ""),
    ("🏪 الفروع", sales['الفرع'].nunique(), ""),
    ("🌍 الجنسيات", employees['الجنسية'].nunique(), ""),
]

for col, (label, value, unit) in zip([c1, c2, c3, c4, c5], metrics):
    with col:
        st.markdown(f"""
        <div style="
            background:white;border-radius:12px;padding:20px;
            text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06);
        ">
            <p style="color:{HADAB_COLORS['muted']};font-size:13px;margin:0">{label}</p>
            <h2 style="color:{HADAB_COLORS['primary']};font-size:26px;margin:6px 0">{value}</h2>
            <p style="color:{HADAB_COLORS['muted']};font-size:12px;margin:0">{unit}</p>
        </div>
        """, unsafe_allow_html=True)

# ========== معلومات ربط البيانات الحقيقية ==========
with st.expander("⚙️ كيفية ربط البيانات الحقيقية"):
    st.markdown("""
    ### 🔗 ربط بيانات Excel
    
    افتح الملف `data/sample_data.py` وعدّل دالة `load_data()` في `app.py`:
    
    ```python
    import pandas as pd
    
    def load_data():
        employees = pd.read_excel("data/employees.xlsx")
        work      = pd.read_excel("data/work_system.xlsx")
        sales     = pd.read_excel("data/sales.xlsx")
        return employees, work, sales
    ```
    
    ### 🗄️ ربط قاعدة بيانات MySQL/PostgreSQL
    
    ```python
    import sqlalchemy
    
    engine = sqlalchemy.create_engine("mysql://user:pass@host/db")
    employees = pd.read_sql("SELECT * FROM employees", engine)
    sales     = pd.read_sql("SELECT * FROM sales", engine)
    ```
    
    ### 📋 أعمدة Excel المطلوبة
    | الجدول | الأعمدة المطلوبة |
    |--------|-----------------|
    | الموظفون | EmployeeID, الاسم, الجنسية, العمر, المسمى الوظيفي, نوع العقد, تاريخ انتهاء الإقامة, تاريخ انتهاء التأمين |
    | نظام العمل | EmployeeID, أيام الحضور, أيام الغياب, عدد ساعات العمل, الأسبوع |
    | المبيعات | التاريخ, الفرع, نوع المنتج, الكمية, سعر البيع, إجمالي المبيعات |
    """)
