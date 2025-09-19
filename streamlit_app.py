# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import io

# ================================
# 공통 설정
# ================================
plotly_font_config = {
    'font': {'family': 'Pretendard-Bold, sans-serif'}
}

st.set_page_config(layout="wide")
st.title("기후변화와 일자리 : 녹색 전환의 기회와 위험 🌍💼")

# ================================
# 유틸 함수
# ================================
def remove_future_data(df, date_col):
    today = datetime.datetime.now().date()
    df[date_col] = pd.to_datetime(df[date_col]).dt.date
    return df[df[date_col] <= today]

@st.cache_data
def get_data_from_url(url):
    """URL에서 데이터 불러오기 (CSV 또는 Excel 지원)."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.content

        if url.lower().endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif url.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
        else:
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")

        return df
    except Exception as e:
        st.error(f"데이터 불러오기에 실패했습니다: {e}")
        return None

# ================================
# 페이지 1. 기후변화 지표
# ================================
def run_public_data_dashboard():
    st.subheader("1. 공개 데이터로 보는 기후변화와 일자리")

    df_climate = pd.DataFrame({
        'year': [1990, 2000, 2010, 2020, 2023],
        '온실가스농도': [354, 370, 390, 412, 419],
        '해수면상승(mm)': [0, 2, 6, 12, 15],
        '해수온도(°C)': [14.0, 14.3, 14.7, 15.0, 15.1],
        '해양산성도(pH)': [8.2, 8.15, 8.1, 8.05, 8.03]
    })

    year_range = st.slider(
        "기후 지표 연도 범위 선택",
        min_value=int(df_climate['year'].min()),
        max_value=int(df_climate['year'].max()),
        value=(1990, 2023)
    )
    df_filtered = df_climate[(df_climate['year'] >= year_range[0]) & (df_climate['year'] <= year_range[1])]

    df_melt = df_filtered.melt(id_vars=['year'], var_name='지표', value_name='값')
    fig = px.line(
        df_melt,
        x='year', y='값', color='지표',
        title='기후변화 4대지표 변화 추이',
        markers=True,
        labels={'year': '연도', '값': '지표 값'}
    )
    fig.update_layout(plotly_font_config)
    st.plotly_chart(fig, use_container_width=True)

# ================================
# 페이지 2. 교육 및 취업 지표
# ================================
def run_education_employment_dashboard():
    st.subheader("2. 교육 및 취업 관련 지표")

    df_college = pd.DataFrame({
        'year': [2018, 2019, 2020, 2021, 2022, 2023],
        '대학진학률': [70.1, 71.3, 72.5, 73.0, 73.8, 74.6],
        '졸업 후 취업률': [65.0, 66.2, 65.8, 67.1, 68.0, 70.3]
    })

    year_range = st.slider(
        "진학/취업 지표 연도 범위 선택",
        min_value=int(df_college['year'].min()),
        max_value=int(df_college['year'].max()),
        value=(2018, 2023)
    )
    df_filtered = df_college[(df_college['year'] >= year_range[0]) & (df_college['year'] <= year_range[1])]

    fig = px.line(
        df_filtered,
        x='year',
        y=['대학진학률', '졸업 후 취업률'],
        markers=True,
        title='대학 진학률 vs 졸업 후 취업률',
        labels={'value': '비율 (%)', 'year': '연도', 'variable': '지표'}
    )
    fig.update_layout(plotly_font_config)
    st.plotly_chart(fig, use_container_width=True)

# ================================
# 페이지 3. 직무 기회 vs 위험
# ================================
def run_risk_opportunity_dashboard():
    st.subheader("3. 녹색 전환: 기회와 위험 직무 비교")

    df_op = pd.DataFrame({
        '직무': ['기후 데이터 분석가', '탄소배출권 전문가', '신재생 에너지 개발자', 'ESG 경영 컨설턴트'],
        '성장 가능성 (점수)': [95, 90, 88, 85]
    })
    df_r = pd.DataFrame({
        '직무': ['화력 발전소 기술자', '자동차 내연기관 엔지니어', '석유화학 공장 운영원'],
        '위험도 (점수)': [90, 85, 80]
    })

    col1, col2 = st.columns(2)
    with col1:
        fig_op = px.bar(df_op, x='직무', y='성장 가능성 (점수)', color='성장 가능성 (점수)',
                        color_continuous_scale=px.colors.sequential.Greens,
                        title='새롭게 떠오르는 녹색 직무')
        fig_op.update_layout(plotly_font_config)
        st.plotly_chart(fig_op, use_container_width=True)

    with col2:
        fig_r = px.bar(df_r, x='직무', y='위험도 (점수)', color='위험도 (점수)',
                       color_continuous_scale=px.colors.sequential.Reds,
                       title='녹색 전환으로 위협받는 직무')
        fig_r.update_layout(plotly_font_config)
        st.plotly_chart(fig_r, use_container_width=True)

# ================================
# 페이지 4. 설문
# ================================
def run_survey_page():
    st.subheader("4.설문 ✍️")

    st.markdown("아래 **15문항** 설문에 답해주세요!")

    q1 = st.radio("1️⃣ 기후변화가 내 직업에 영향을 줄 것 같나요?", ["전혀 아니다", "조금 그렇다", "매우 그렇다"])
    q2 = st.selectbox("2️⃣ 가장 관심 있는 녹색 일자리 분야는?", ["신재생에너지", "ESG 컨설팅", "탄소 배출권", "기후 데이터 분석"])
    q3 = st.slider("3️⃣ 기후변화 대응 역량을 키우고 싶은 정도 (0~10)", 0, 10, 5)
    q4 = st.radio("4️⃣ 기후위기를 얼마나 심각하게 느끼시나요?", ["전혀 심각하지 않다", "보통이다", "매우 심각하다"])
    q5 = st.checkbox("5️⃣ 기후변화 대응 관련 교육을 받은 적이 있다")
    q6 = st.multiselect("6️⃣ 평소 실천하는 친환경 생활 습관을 선택해주세요", ["재활용", "대중교통 이용", "에너지 절약", "친환경 제품 구매", "채식 실천"])
    q7 = st.radio("7️⃣ 기후변화 대응에서 더 중요한 역할을 해야 할 주체는 누구라고 생각하시나요?", ["정부", "기업", "개인", "모두"])
    q8 = st.select_slider("8️⃣ 녹색 전환 과정에서 내 직업 안정성에 대한 우려 정도", options=["없음", "낮음", "보통", "높음", "매우 높음"])
    q9 = st.text_area("9️⃣ 녹색 일자리 확대를 위해 필요한 정책이나 제안이 있다면 적어주세요.")
    q10 = st.radio("🔟 기후변화 대응을 위한 세금(탄소세 등) 부과에 동의하시나요?", ["찬성", "반대", "잘 모르겠다"])
    q11 = st.slider("1️⃣1️⃣ 기업의 친환경 경영이 중요하다고 생각하는 정도 (0~10)", 0, 10, 7)
    q12 = st.radio("1️⃣2️⃣ 기후변화로 인한 직무 재교육이 필요하다고 생각하시나요?", ["필요 없다", "어느 정도 필요하다", "매우 필요하다"])
    q13 = st.multiselect("1️⃣3️⃣ 녹색 일자리 전환 시 가장 필요한 지원은?", ["재교육", "재정지원", "멘토링/상담", "일자리 매칭"])
    q14 = st.radio("1️⃣4️⃣ 해외보다 국내 기후정책이 더 중요하다고 생각하시나요?", ["국내 정책이 우선", "해외 협력이 더 중요", "둘 다 중요"])
    q15 = st.text_area("1️⃣5️⃣ 자유롭게 기후변화와 미래 일자리에 대한 의견을 남겨주세요.")

    if st.button("설문 제출"):
        st.success("✅ 설문이 제출되었습니다. 감사합니다!")

# ================================
# 메인 실행
# ================================
def main():
    tabs = st.tabs(["🌍 기후변화 지표", "📚 교육 및 취업 지표", "⚖️ 직무 기회 vs 위험", "📝 설문"])

    with tabs[0]:
        run_public_data_dashboard()
    with tabs[1]:
        run_education_employment_dashboard()
    with tabs[2]:
        run_risk_opportunity_dashboard()
    with tabs[3]:
        run_survey_page()

if __name__ == "__main__":
    main()
