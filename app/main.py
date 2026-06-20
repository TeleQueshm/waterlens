from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# ⚙️ تنظیم آستانه تصمیم‌گیری سفارشی (تغییر از 0.50 به 0.35 برای کاهش سخت‌گیری مدل)
# هرچه این عدد را پایین‌تر بیاورید، مدل راحت‌تر رای به "قابل شرب" می‌دهد.
CUSTOM_THRESHOLD = 0.35

# بارگذاری مدل و اسکالر آموزش‌دیده
try:
    model = joblib.load('final_water_model.pkl')
    scaler = joblib.load('final_scaler.pkl')
    print(f"✅ مدل و اسکالر بارگذاری شدند. آستانه تصمیم‌گیری روی {CUSTOM_THRESHOLD*100}% تنظیم شد.")
except FileNotFoundError:
    print("❌ خطا: فایل‌های مدل (.pkl) پیدا نشدند! ابتدا مدل را آموزش دهید.")

# ۱. صفحه اصلی (فرم ورود داده برای اپراتور)
@app.route('/')
def home():
    return render_template('index.html')

# ۲. پردازش داده‌های فرم وب (Web Predict)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # دریافت داده‌ها از فرم HTML
        features = [float(x) for x in request.form.values()]
        final_features = np.array([features])
        
        # نرمال‌سازی داده‌ها با اسکالر قبلی
        scaled_features = scaler.transform(final_features)
        
        # دریافت میزان احتمال (Probability) برای کلاس ۱ (قابل شرب)
        probability = model.predict_proba(scaled_features)[0][1]
        
        # اعمال آستانه تصمیم‌گیری جدید به جای model.predict پیش‌فرض
        if probability >= CUSTOM_THRESHOLD:
            # نمایش درصد اطمینان واقعی به کاربر
            result = f"قابل شرب (سطح اطمینان: {probability*100:.1f}%)"
            status_class = "safe"
        else:
            result = f"غیرقابل شرب ⚠️ (احتمال آلودگی: {(1-probability)*100:.1f}%)"
            status_class = "danger"
            
        return render_template('index.html', prediction_text=f'وضعیت آب: {result}', status_class=status_class)
    
    except Exception as e:
        return render_template('index.html', prediction_text=f'خطا در پردازش داده‌ها: {str(e)}')

# ۳. سرویس API برای سنسورهای هوشمند و IoT (JSON Predict)
@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()
        
        # ترتیب ستون‌ها باید دقیقاً مطابق دیتای اولیه باشد
        feature_order = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 
                         'Conductivity', 'Organic_carbon', 'Trihalومتان‌ها', 'Turbidity']
        
        # اصلاح کوچک برای تطبیق نام انگلیسی در صورت وجود در کلیدهای جیسون شما
        feature_order = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 
                         'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
        
        features = [float(data[field]) for field in feature_order]
        final_features = np.array([features])
        
        # محاسبات احتمال با آستانه جدید
        scaled_features = scaler.transform(final_features)
        probability = float(model.predict_proba(scaled_features)[0][1])
        
        # تعیین خروجی 0 یا 1 بر اساس آستانه سفارشی
        custom_prediction = 1 if probability >= CUSTOM_THRESHOLD else 0
        
        return jsonify({
            'status': 'success',
            'potability': custom_prediction,
            'potability_probability': probability,
            'applied_threshold': CUSTOM_THRESHOLD,
            'message': 'Water is potable' if custom_prediction == 1 else 'Water is NOT potable'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == "__main__":
    # برنامه روی پورت 5005 اجرا می‌شود
    app.run(debug=True, host='0.0.0.0', port=5005)