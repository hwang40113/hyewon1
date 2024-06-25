#app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import os

# 데이터 불러오기
file_path = 'cafe.xlsx'

# Check if the file exists before loading
if os.path.exists(file_path):
    cafe_data = pd.read_excel(file_path)
else:
    st.error('File not found. Please check the file path.')
    st.stop()

# order_date를 datetime 형식으로 변환
cafe_data['order_date'] = pd.to_datetime(cafe_data['order_date'])

# 연도와 월 컬럼 추가
cafe_data['year'] = cafe_data['order_date'].dt.year
cafe_data['month'] = cafe_data['order_date'].dt.month

# Streamlit 대시보드 설정
st.title('카페 매출 대시보드')

# 사이드바에서 연도와 제품 선택
selected_year = st.sidebar.selectbox(
    '연도 선택', sorted(cafe_data['year'].unique()))
selected_product = st.sidebar.selectbox(
    '제품 선택', sorted(cafe_data['item'].unique()))

# 선택된 연도와 제품에 따라 데이터 필터링
filtered_data = cafe_data[(cafe_data['year'] == selected_year) &
                          (cafe_data['item'] == selected_product)]

# Check if filtered data is empty
if filtered_data.empty:
    st.warning(f'No data available for {selected_year}년 and {selected_product}.')
else:
    # 월별 매출 데이터 계산
    monthly_sales = filtered_data.groupby('month')['price'].sum().reset_index()

    # 매출 표 출력
    st.subheader(f'{selected_year}년 {selected_product} 매출 데이터')
    st.dataframe(filtered_data)

    # 막대 그래프 그리기
    st.subheader(f'{selected_year}년 {selected_product} 월별 매출')
    st.bar_chart(monthly_sales.set_index('month'))

    # 월별 매출 세부 정보 테이블 추가
    st.subheader(f'{selected_year}년 {selected_product} 월별 매출 세부 정보')
    st.table(monthly_sales)

    # 총 매출 합계 출력
    total_sales = monthly_sales['price'].sum()
    st.metric(label=f"{selected_year}년 {selected_product} 총 매출", value=f"{total_sales:,.0f} 원")

# 전체 데이터에서 잘 팔린 메뉴 분석
st.subheader('전체 메뉴 매출 분석')

# 메뉴별 매출 데이터 계산
menu_sales = cafe_data.groupby('item')['price'].sum().reset_index().sort_values(by='price', ascending=False)

# 전체 매출에서 잘 팔린 상위 10개 메뉴 출력
st.write('가장 잘 팔린 메뉴 Top 10')
st.table(menu_sales.head(10))

# 잘 팔린 메뉴에 대한 막대 그래프 그리기
st.bar_chart(menu_sales.set_index('item').head(10))
