# ☕ داشبورد محمصة هدب — Hadab Roastery Dashboard

![Hadab Roastery](https://img.shields.io/badge/محمصة-هدب-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=for-the-badge&logo=streamlit)

نظام داشبورد متكامل لإدارة وتحليل بيانات محمصة هدب، يشمل إدارة الموظفين، نظام العمل، والمبيعات.

---

## 📂 هيكل المشروع

```
hadab_dashboard/
├── app.py                  # الصفحة الرئيسية ونقطة التشغيل
├── requirements.txt        # المكتبات المطلوبة
├── pages/
│   ├── 1_Overview.py       # لوحة النظرة العامة
│   ├── 2_Employees.py      # لوحة الموظفين
│   ├── 3_WorkSystem.py     # لوحة نظام العمل
│   └── 4_Sales.py          # لوحة المبيعات
├── data/
│   └── sample_data.py      # بيانات تجريبية (استبدلها ببياناتك)
└── utils/
    └── helpers.py          # دوال مساعدة مشتركة
```

---

## 🚀 طريقة التشغيل

### 1. المتطلبات الأساسية
- Python 3.9 أو أحدث
- pip

### 2. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 3. تشغيل الداشبورد
```bash
streamlit run app.py
```

سيفتح المتصفح تلقائياً على العنوان: `http://localhost:8501`

---

## 🔗 ربط بياناتك الحقيقية

### ربط Excel
افتح `app.py` وعدّل دالة `load_data`:
```python
def load_data():
    employees = pd.read_excel("data/employees.xlsx")
    work      = pd.read_excel("data/work_system.xlsx")
    sales     = pd.read_excel("data/sales.xlsx")
    return employees, work, sales
```

### ربط قاعدة بيانات
```python
import sqlalchemy
engine = sqlalchemy.create_engine("mysql://user:pass@host/db_name")
employees = pd.read_sql("SELECT * FROM employees", engine)
```

---

## 📊 مكونات الداشبورد

| الصفحة | المحتوى |
|--------|---------|
| 🏠 الرئيسية | نقطة البداية وملخص سريع |
| 📊 النظرة العامة | إحصاءات كلية، رسوم بيانية للمبيعات والموظفين |
| 👥 الموظفون | جدول تفاعلي، تنبيهات الإقامة والتأمين، رسوم |
| ⏰ نظام العمل | الحضور والغياب، ساعات العمل، اتجاهات أسبوعية |
| 💰 المبيعات | تحليل المنتجات والفروع، خريطة حرارية، تحميل CSV |

---

## 📤 النشر على Streamlit Cloud (مجاني)

1. ارفع المشروع على GitHub
2. اذهب إلى [share.streamlit.io](https://share.streamlit.io)
3. اختر المستودع والملف `app.py`
4. اضغط Deploy!

---

## 🎨 الألوان المستخدمة (هوية هدب)
- البرتقالي الرئيسي: `#C2570A`
- البرتقالي الثانوي: `#E07820`
- البني الداكن: `#8B3A00`
