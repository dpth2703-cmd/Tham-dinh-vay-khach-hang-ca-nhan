import streamlit as st
import pandas as pd

st.set_page_config(page_title="Loan Scoring", page_icon="🏦")

st.title("🏦 MINI APP THẨM ĐỊNH CHO VAY KHÁCH HÀNG CÁ NHÂN")

st.header("Thông tin khách hàng")

col1, col2 = st.columns(2)

with col1:
    loan = st.number_input(
        "Số tiền vay (VNĐ)",
        min_value=1000000,
        step=1000000,
        value=500000000
    )

    year = st.number_input(
        "Thời gian vay (năm)",
        min_value=1,
        max_value=35,
        value=20
    )

    interest = st.number_input(
        "Lãi suất (%/năm)",
        min_value=1.0,
        max_value=30.0,
        value=10.0
    )

    income = st.number_input(
        "Thu nhập hàng tháng (VNĐ)",
        min_value=1000000,
        value=30000000
    )

with col2:
    dependent = st.number_input(
        "Số người phụ thuộc",
        min_value=0,
        max_value=10,
        value=0
    )

    old_debt = st.number_input(
        "Dư nợ khoản vay cũ (VNĐ)",
        min_value=0,
        value=0
    )

    collateral = st.number_input(
        "Giá trị tài sản bảo đảm (VNĐ)",
        min_value=1000000,
        value=800000000
    )

    cic = st.selectbox(
        "Xếp hạng CIC",
        [
            "Tốt",
            "Trung bình",
            "Xấu"
        ]
    )

st.divider()

if st.button("Thẩm định khoản vay"):

    # Tính tiền trả hàng tháng (ước tính)
    monthly_interest = interest / 100 / 12
    month = year * 12

    monthly_payment = (
        loan * monthly_interest /
        (1 - (1 + monthly_interest) ** (-month))
    )

    total_debt = monthly_payment + old_debt

    dti = total_debt / income

    ltv = loan / collateral

    score = 100

    # Chấm điểm DTI
    if dti > 0.5:
        score -= 40
    elif dti > 0.4:
        score -= 25
    elif dti > 0.3:
        score -= 10

    # LTV
    if ltv > 0.8:
        score -= 30
    elif ltv > 0.7:
        score -= 15

    # Người phụ thuộc
    if dependent >= 3:
        score -= 10

    # CIC
    if cic == "Trung bình":
        score -= 20
    elif cic == "Xấu":
        score -= 50

    if score >= 80:
        result = "✅ PHÊ DUYỆT"
        color = "green"
    elif score >= 60:
        result = "⚠️ XEM XÉT THÊM"
        color = "orange"
    else:
        result = "❌ TỪ CHỐI"

        color = "red"

    st.header("Kết quả")

    st.metric(
        "Tiền trả mỗi tháng",
        f"{monthly_payment:,.0f} VNĐ"
    )

    st.metric(
        "DTI",
        f"{dti:.2%}"
    )

    st.metric(
        "LTV",
        f"{ltv:.2%}"
    )

    st.metric(
        "Điểm tín dụng",
        score
    )

    st.markdown(
        f"<h2 style='color:{color}'>{result}</h2>",
        unsafe_allow_html=True
    )

    df = pd.DataFrame({
        "Chỉ tiêu": [
            "Khoản vay",
            "Thu nhập",
            "Khoản trả hàng tháng",
            "DTI",
            "LTV",
            "Điểm"
        ],
        "Giá trị": [
            f"{loan:,.0f}",
            f"{income:,.0f}",
            f"{monthly_payment:,.0f}",
            f"{dti:.2%}",
            f"{ltv:.2%}",
            score
        ]
    })

    st.dataframe(df, use_container_width=True)
