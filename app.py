import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px

# โหลดข้อมูล (สมมติว่าเรามีฟังก์ชัน load_data() ที่โหลดข้อมูลเรียบร้อยแล้ว)
@st.cache_data
def load_data():
    df = pd.read_csv("accident2021.csv")
    df['วันที่เกิดเหตุ'] = pd.to_datetime(df['วันที่เกิดเหตุ'], format='%d/%m/%Y', errors='coerce')
    df['เวลา'] = pd.to_datetime(df['เวลา'], format='%H:%M', errors='coerce')
    df = df.dropna(subset=['วันที่เกิดเหตุ', 'เวลา'])
    return df

df = load_data()

st.header("7. การสร้างแบบจำลองทำนาย")

# 1. การวิเคราะห์การถดถอย (Regression Analysis)
st.subheader("1. การวิเคราะห์การถดถอย (Regression Analysis)")

# เตรียมข้อมูล
df['hour'] = df['เวลา'].dt.hour
df['day_of_week'] = df['วันที่เกิดเหตุ'].dt.dayofweek
weather_dummies = pd.get_dummies(df['สภาพอากาศ'], prefix='weather')
road_dummies = pd.get_dummies(df['บริเวณที่เกิดเหตุ'], prefix='road')

X = pd.concat([df[['hour', 'day_of_week']], weather_dummies, road_dummies], axis=1)
y = df['ผู้บาดเจ็บสาหัส'] + df['ผู้บาดเจ็บเล็กน้อย']

# แบ่งข้อมูลสำหรับการเทรนและทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# สร้างและเทรนโมเดล
model = LinearRegression()
model.fit(X_train, y_train)

# ทำนายและประเมินผล
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
st.write(f"Mean Squared Error: {mse:.2f}")

# แสดงผลลัพธ์
fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Actual', 'y': 'Predicted'}, 
                 title='Actual vs Predicted Injuries')
st.plotly_chart(fig)

# 2. การจำแนกประเภท (Classification)
st.subheader("2. การจำแนกประเภท (Classification)")

# เตรียมข้อมูล
df['accident_severity'] = np.where(df['ผู้เสียชีวิต'] > 0, 1, 0)
vehicle_columns = ['รถจักรยานยนต์', 'รถยนต์นั่งส่วนบุคคล', 'รถปิคอัพบรรทุก4ล้อ', 'รถบรรทุก6ล้อ', 'รถอื่นๆ']

X = pd.concat([df[['hour', 'day_of_week'] + vehicle_columns], weather_dummies], axis=1)
y = df['accident_severity']

# แบ่งข้อมูลสำหรับการเทรนและทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# สร้างและเทรนโมเดล
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# ทำนายและประเมินผล
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
st.write(f"Accuracy: {accuracy:.2f}")

# แสดงความสำคัญของฟีเจอร์
feature_importance = pd.DataFrame({'feature': X.columns, 'importance': model.feature_importances_})
feature_importance = feature_importance.sort_values('importance', ascending=False).head(10)
fig = px.bar(feature_importance, x='importance', y='feature', orientation='h', 
             title='Top 10 Most Important Features')
st.plotly_chart(fig)

# 3. การวิเคราะห์อนุกรมเวลา (Time Series Analysis)
st.subheader("3. การวิเคราะห์อนุกรมเวลา (Time Series Analysis)")

# เตรียมข้อมูล
daily_accidents = df.groupby('วันที่เกิดเหตุ').size().reset_index(name='count')
daily_accidents = daily_accidents.set_index('วันที่เกิดเหตุ')

# สร้างและเทรนโมเดล ARIMA
model = ARIMA(daily_accidents['count'], order=(1, 1, 1))
results = model.fit()

# ทำนาย 30 วันถัดไป
forecast = results.forecast(steps=30)

# แสดงผลลัพธ์
fig = px.line(daily_accidents, x=daily_accidents.index, y='count', title='Daily Accidents and Forecast')
fig.add_scatter(x=forecast.index, y=forecast, mode='lines', name='Forecast')
st.plotly_chart(fig)

st.write("""
หมายเหตุ: แบบจำลองเหล่านี้เป็นเพียงตัวอย่างเบื้องต้น ในการใช้งานจริง ควรมีการปรับแต่งพารามิเตอร์, 
ทำ feature engineering เพิ่มเติม, และใช้เทคนิคการประเมินผลที่ซับซ้อนมากขึ้น เพื่อให้ได้ผลลัพธ์ที่แม่นยำและน่าเชื่อถือมากขึ้น
""")