import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from json import dumps
# اگر این کتابخانه را ندارید، ابتدا در ترمینال بنویسید: pip install xgboost
from xgboost import XGBClassifier 
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib

def train_advanced_model():
    print("🔄 در حال آموزش مدل پیشرفته برای حل مشکل سخت‌گیری مدل...")
    
    # ۱. بارگذاری دیتای تمیز شده
    try:
        df = pd.read_csv('cleaned_water_data.csv')
    except FileNotFoundError:
        print("❌ خطا: فایل 'cleaned_water_data.csv' یافت نشد.")
        return

    X = df.drop('Potability', axis=1)
    y = df['Potability']
    
    # ۲. تقسیم متعادل داده‌ها
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # ۳. نرمال‌سازی
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # ۴. محاسبه نسبت کلاس صفر به یک برای متعادل‌سازی وزن‌ها
    ratio = float(y_train.value_counts()[0] / y_train.value_counts()[1])
    
    # ۵. تعریف مدل هوشمندتر (XGBoost) با کنترل سخت‌گیری
    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,            # کاهش عمق برای جلوگیری از حفظ کردن داده‌ها
        scale_pos_weight=ratio, # حل مشکل تمایل به کلاس صفر
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    print("مدل جدید با موفقیت جایگزین شد! 🤖")
    
    # ۶. ارزیابی مدل جدید
    y_pred = model.predict(X_test_scaled)
    
    print("\n" + "="*40)
    print(f"🔹 Accuracy (دقت کل):       {accuracy_score(y_test, y_pred)*100:.2f}%")
    print(f"🔹 F1-Score (توازن):        {f1_score(y_test, y_pred)*100:.2f}%")
    print(f"🔹 Recall (حساسیت):          {recall_score(y_test, y_pred)*100:.2f}%")
    print("="*40)
    
    # ۷. ذخیره مدل جدید روی همان فایل‌های قبلی (تا فلسک بدون تغییر آپدیت شود)
    joblib.dump(model, 'final_water_model.pkl')
    joblib.dump(scaler, 'final_scaler.pkl')
    print("💾 فایل‌های مدل پایش آنلاین بروزرسانی شدند.")

if __name__ == "__main__":
    train_advanced_model()