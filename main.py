# import streamlit as st
# import pandas as pd

# # Set page title
# st.set_page_config(page_title="Accident Data Viewer 2021")

# # Add a title to the app
# st.title("Accident Data Viewer 2021")

# # Load the CSV file
# @st.cache_data
# def load_data():
#     return pd.read_csv("accident2021.csv")

# df = load_data()

# # Display the dataframe
# st.dataframe(df)

# # Add some basic statistics
# st.subheader("Basic Statistics")
# st.write(f"Total number of accidents: {len(df)}")
# st.write(f"Number of columns: {len(df.columns)}")

# # Add a section for user to select columns to view
# st.subheader("Select columns to view")
# selected_columns = st.multiselect("Choose columns", df.columns.tolist(), default=df.columns.tolist()[:5])

# # Display selected columns
# if selected_columns:
#     st.dataframe(df[selected_columns])
# else:
#     st.warning("Please select at least one column.")
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="การวิเคราะห์ข้อมูลอุบัติเหตุปี 2021", layout="wide")

# Load data function
@st.cache_data
def load_data():
    df = pd.read_csv("accident2021.csv")
    df['วันที่เกิดเหตุ'] = pd.to_datetime(df['วันที่เกิดเหตุ'], format='%d/%m/%Y', errors='coerce')
    df['เวลา'] = pd.to_datetime(df['เวลา'], format='%H:%M', errors='coerce')
    df = df.dropna(subset=['วันที่เกิดเหตุ', 'เวลา'])
    return df

df = load_data()

st.title("การวิเคราะห์ข้อมูลอุบัติเหตุปี 2021")

# 1. Analysis of accident trends
st.header("1. การวิเคราะห์แนวโน้มอุบัติเหตุ")

# Daily trend
daily_accidents = df['วันที่เกิดเหตุ'].dt.date.value_counts().sort_index()
fig = px.line(x=daily_accidents.index, y=daily_accidents.values, 
              title="ความถี่ของอุบัติเหตุรายวัน",
              labels={"x": "วันที่", "y": "จำนวนอุบัติเหตุ"})
st.plotly_chart(fig)

# Hourly trend
hourly_accidents = df['เวลา'].dt.hour.value_counts().sort_index()
fig = px.bar(x=hourly_accidents.index, y=hourly_accidents.values, 
             title="ความถี่ของอุบัติเหตุรายชั่วโมง",
             labels={"x": "ชั่วโมง", "y": "จำนวนอุบัติเหตุ"})
st.plotly_chart(fig)

# 2. Identification of high-risk areas
st.header("2. การระบุพื้นที่เสี่ยง")

# Map of accident locations
st.subheader("แผนที่แสดงตำแหน่งที่เกิดอุบัติเหตุ")
fig = px.scatter_mapbox(df, lat="LATITUDE", lon="LONGITUDE", zoom=3, 
                        mapbox_style="open-street-map")
fig.update_layout(height=600)
st.plotly_chart(fig)

# Road characteristics
road_char = df['บริเวณที่เกิดเหตุ'].value_counts()
fig = px.pie(values=road_char.values, names=road_char.index, 
             title="ความถี่ของอุบัติเหตุตามลักษณะถนน")
st.plotly_chart(fig)

# 3. Analysis of accident causes
st.header("3. การวิเคราะห์สาเหตุของอุบัติเหตุ")

# Suspected causes
causes = df['มูลเหตุสันนิษฐาน'].value_counts().reset_index()
causes.columns = ['สาเหตุ', 'จำนวน']
fig = px.bar(causes, x='จำนวน', y='สาเหตุ', orientation='h',
             title='ความถี่ของสาเหตุที่สันนิษฐาน',
             labels={'จำนวน': 'จำนวนอุบัติเหตุ', 'สาเหตุ': 'สาเหตุ'})
fig.update_layout(height=800)
st.plotly_chart(fig)

# Weather conditions
weather = df['สภาพอากาศ'].value_counts().reset_index()
weather.columns = ['สภาพอากาศ', 'จำนวน']
fig = px.pie(weather, values='จำนวน', names='สภาพอากาศ', 
             title='อุบัติเหตุตามสภาพอากาศ')
st.plotly_chart(fig)

# 4. Analysis of vehicle types
st.header("4. การวิเคราะห์ประเภทยานพาหนะ")

vehicle_columns = ['รถจักรยานยนต์', 'รถยนต์นั่งส่วนบุคคล', 'รถปิคอัพบรรทุก4ล้อ', 'รถบรรทุก6ล้อ', 'รถอื่นๆ']
vehicle_counts = df[vehicle_columns].sum().sort_values(ascending=False)
fig = px.bar(x=vehicle_counts.index, y=vehicle_counts.values,
             title="ความถี่ของประเภทยานพาหนะในอุบัติเหตุ",
             labels={"x": "ประเภทยานพาหนะ", "y": "จำนวนอุบัติเหตุ"})
st.plotly_chart(fig)

# 5. Analysis of accident severity
st.header("5. การวิเคราะห์ความรุนแรงของอุบัติเหตุ")

severity_columns = ['ผู้เสียชีวิต', 'ผู้บาดเจ็บสาหัส', 'ผู้บาดเจ็บเล็กน้อย']
severity_data = df[severity_columns].sum()
fig = px.bar(x=severity_data.index, y=severity_data.values,
             title="ความรุนแรงของอุบัติเหตุ",
             labels={"x": "ประเภทความรุนแรง", "y": "จำนวนคน"})
st.plotly_chart(fig)

# Correlation between vehicle types and severity
correlation = df[vehicle_columns + severity_columns].corr()
fig = px.imshow(correlation, 
                title="ความสัมพันธ์ระหว่างประเภทยานพาหนะและความรุนแรงของอุบัติเหตุ")
st.plotly_chart(fig)

# 6. Accident prevention and reduction planning
st.header("6. การวางแผนป้องกันและลดอุบัติเหตุ")
st.write("""
ข้อมูลนี้สามารถนำไปใช้ในการวางแผนป้องกันและลดอุบัติเหตุ โดยมุ่งเน้นที่:
- พื้นที่ที่มีอุบัติเหตุบ่อย
- ช่วงเวลาที่เกิดอุบัติเหตุมาก
- สาเหตุหลักของอุบัติเหตุ
- ประเภทยานพาหนะที่มีความเสี่ยงสูง
""")

# 7. Predictive modeling
st.header("7. การสร้างแบบจำลองทำนาย")
st.write("""
การสร้างแบบจำลองทำนายโอกาสการเกิดอุบัติเหตุสามารถทำได้โดยใช้ข้อมูลนี้ 
ซึ่งอาจรวมถึงการใช้เทคนิค Machine Learning เช่น:
- การวิเคราะห์การถดถอย (Regression Analysis)
- การจำแนกประเภท (Classification)
- การวิเคราะห์อนุกรมเวลา (Time Series Analysis)
""")

# 8. Detailed reporting and data presentation
st.header("8. การจัดทำรายงานและการนำเสนอข้อมูลโดยละเอียด")
st.write("""
การนำเสนอข้อมูลเชิงลึกเพิ่มเติมสามารถทำได้โดย:
- สร้างแดชบอร์ดแบบโต้ตอบ (Interactive Dashboard)
- จัดทำรายงานประจำเดือนหรือประจำปี
- วิเคราะห์แนวโน้มระยะยาวของอุบัติเหตุ
- เปรียบเทียบข้อมูลระหว่างภูมิภาคหรือช่วงเวลาต่างๆ
""")