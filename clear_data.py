import pandas as pd
import numpy as np

def clean_data(file_path):
    print("🔄 در حال بارگذاری و تمیزکاری داده‌ها...")
    
    # ۱. بارگذاری فایل داده‌ها
    df = pd.read_csv(file_path)
    
    # ۲. پاک‌سازی داده‌های متنی مزاحم (مثل عبارت "دیتا برا" در ستون Organic_carbon)
    # این دستور متن‌ها را به NaN (مقدار خالی) تبدیل می‌کند تا بعداً به صورت عددی پردازش شوند
    for col in df.columns:
        if col != 'Potability':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # ۳. پر کردن داده‌های گم‌شده (Missing Values) با استفاده از میانه (Median) هر ستون
    # میانه نسبت به میانگین در برابر داده‌های پرت مقاوم‌تر است
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            median_value = df[col].median()
            df[col].fillna(median_value, inplace=True)
            print(col, f"برطرف شد. مقادیر خالی با میانه ({median_value:.2f}) پر شدند. ✅")
            
    # ۴. ذخیره داده‌های تمیز شده در یک فایل جدید
    output_filename = 'cleaned_water_data.csv'
    df.to_csv(output_filename, index=False)
    print(f"Dataset cleaned successfully! Saved as: '{output_filename}' ✨")

if __name__ == "__main__":
    # نام فایل دیتای خود را اینجا بنویسید (مثلاً data.csv)
    # اگر فایل در پوشه دیگری است، آدرس کامل آن را بدهید
    clean_data('water_potability.csv')
