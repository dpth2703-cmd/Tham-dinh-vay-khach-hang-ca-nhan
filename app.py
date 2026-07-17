import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Cấu hình trang trang trí giao diện chuyên nghiệp
st.set_page_config(
    page_title="Hệ thống Thẩm định Tín dụng Cá nhân",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm CSS tùy chỉnh để làm đẹp giao diện
st.markdown("""
    <style>
    .main-title {
        font-size:32px !important;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-title {
        font-size:20px !important;
        font-weight: bold;
        color: #0D9488;
        border-bottom: 2px solid #0D9488;
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .metric-box {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_base_color=True)

st.markdown('<div class="main-title">🏦 HỆ THỐNG THẨM ĐỊNH CHO VAY KHÁCH HÀNG CÁ NHÂN</div>', unsafe_allow_html=True)
st.write("---")

# ================= SIDEBAR: NHẬP THÔNG TIN KHÁCH HÀNG =================
st.sidebar.header("📁 THÔNG TIN KHOẢN VAY & KHÁCH HÀNG")

with st.sidebar.expander("1. Thông tin Khoản vay", expanded=True):
    loan_amount = st.number_input("Số tiền đề nghị vay (VND)", min_value=0.0, value=500000000.0, step=10000000.0, format="%.2f")
    loan_term = st.number_input("Thời gian vay (tháng)", min_value=1, value=60, step=1)
    interest_rate = st.number_input("Lãi suất cho vay (%/năm)", min_value=0.0, value=8.5, step=0.1, format="%.2f")

with st.sidebar.expander("2. Năng lực Tài chính", expanded=True):
    monthly_income = st.number_input("Thu nhập hàng tháng (VND)", min_value=0.0, value=30000000.0, step=10000000.0, format="%.2f")
    dependents = st.number_input("Số người phụ thuộc", min_value=0, value=1, step=1)
    existing_debt = st.number_input("Dư nợ khoản vay cũ (nếu có) (VND)", min_value=0.0, value=50000000.0, step=5000000.0, format="%.2f")
    old_monthly_payment = st.number_input("Gốc + lãi trả cũ hàng tháng (VND)", min_value=0.0, value=3000000.0, step=500000.0, format="%.2f")

with st.sidebar.expander("3. Tài sản Bảo đảm (TSĐB) & CIC", expanded=True):
    collateral_value = st.number_input("Giá trị Tài sản Đảm bảo (VND)", min_value=1.0, value=800000000.0, step=10000000.0, format="%.2f")
    cic_group = st.selectbox("Nhóm nợ CIC hiện tại", options=["Nhóm 1 (Nợ đủ tiêu chuẩn)", "Nhóm 2 (Nợ cần chú ý)", "Nhóm 3 (Nợ dưới tiêu chuẩn)", "Nhóm 4 (Nợ nghi ngờ)", "Nhóm 5 (Nợ có khả năng mất vốn)"])

# ================= XỬ LÝ LOGIC VÀ TÍNH TOÁN =================

# 1. Tính toán Nghĩa vụ trả nợ gốc + lãi hàng tháng (EMI) của khoản vay mới
r_monthly = (interest_rate / 100) / 12
if r_monthly > 0:
    new_monthly_payment = loan_amount * r_monthly * ((1 + r_monthly) ** loan_term) / (((1 + r_monthly) ** loan_term) - 1)
else:
    new_monthly_payment = loan_amount / loan_term

total_monthly_debt_service = new_monthly_payment + old_monthly_payment

# 2. Tính chỉ số DTI (Debt-to-Income)
dti = (total_monthly_debt_service / monthly_income) * 100 if monthly_income > 0 else 100.0

# 3. Tính chỉ số LTV / LAV (Loan-to-Value)
ltv = (loan_amount / collateral_value) * 100

# 4. Chi phí sinh hoạt ước tính dựa trên số người phụ thuộc (giả định 3,000,000 VND / người)
living_cost_per_person = 3000000.0
total_living_cost = dependents * living_cost_per_person
disposable_income = monthly_income - total_living_cost - total_monthly_debt_service

# ================= GIAO DIỆN CHÍNH: HIỂN THỊ KẾT QUẢ =================

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-title">📊 Chỉ số Tài chính Cơ bản</div>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><b>Số tiền trả mới / tháng</b><br><span style="font-size:20px; color:#1E3A8A; font-weight:bold;">{new_monthly_payment:,.2f} VND</span></div>', unsafe_allow_html=True)
    with m2:
        # Màu sắc động cho DTI
        dti_color = "#10B981" if dti <= 55 else "#EF4444"
        st.markdown(f'<div class="metric-box"><b>Tỷ lệ DTI</b><br><span style="font-size:20px; color:{dti_color}; font-weight:bold;">{dti:.2f}%</span></div>', unsafe_allow_html=True)
    with m3:
        # Màu sắc động cho LTV
        ltv_color = "#10B981" if ltv <= 70 else "#EF4444"
        st.markdown(f'<div class="metric-box"><b>Tỷ lệ LTV (LAV)</b><br><span style="font-size:20px; color:{ltv_color}; font-weight:bold;">{ltv:.2f}%</span></div>', unsafe_allow_html=True)

    # Biểu đồ dòng tiền thu nhập phân bổ
    st.markdown('<div class="section-title">🍰 Phân bổ Thu nhập Hàng tháng</div>', unsafe_allow_html=True)
    
    labels = ['Trả nợ cũ', 'Trả nợ vay mới', 'Chi phí phụ thuộc', 'Thu nhập còn lại']
    values = [old_monthly_payment, new_monthly_payment, total_living_cost, max(0.0, disposable_income)]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=['#FFA07A', '#5C6BC0', '#FFD700', '#66BB6A']))])
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">📝 Kết luận Thẩm định</div>', unsafe_allow_html=True)
    
    # Tiêu chuẩn thẩm định (Policy thresholds)
    dti_threshold = 55.0  # Tối đa 55% thu nhập
    ltv_threshold = 70.0  # Tối đa 70% giá trị TSĐB
    
    reasons = []
    approved = True
    
    if dti > dti_threshold:
        approved = False
        reasons.append(f"Tỷ lệ DTI ({dti:.2f}%) vượt mức quy định ({dti_threshold:.2f}%)")
        
    if ltv > ltv_threshold:
        approved = False
        reasons.append(f"Tỷ lệ LTV ({ltv:.2f}%) vượt mức quy định ({ltv_threshold:.2f}%)")
        
    if cic_group != "Nhóm 1 (Nợ đủ tiêu chuẩn)":
        if cic_group == "Nhóm 2 (Nợ cần chú ý)":
            reasons.append("CIC Nhóm 2: Cần giải trình và bổ sung hồ sơ chứng minh lý do chậm thanh toán.")
        else:
            approved = False
            reasons.append(f"CIC thuộc {cic_group}: Từ chối cho vay do có nợ xấu.")
            
    if disposable_income < 0:
        approved = False
        reasons.append("Thu nhập tích lũy còn lại sau khi trừ chi phí và nợ vay bị âm.")

    # Hiển thị kết quả Approve / Reject trực quan
    if approved:
        if cic_group == "Nhóm 2 (Nợ cần chú ý)":
            st.warning("⚠️ ĐỀ XUẤT: PHÊ DUYỆT CÓ ĐIỀU KIỆN")
        else:
            st.success("✅ ĐỀ XUẤT: PHÊ DUYỆT KHOẢN VAY")
        st.write("Khách hàng đạt đủ điều kiện cơ bản về năng lực tài chính, CIC và tài sản bảo đảm.")
    else:
        st.error("❌ ĐỀ XUẤT: TỪ CHỐI KHOẢN VAY")
        st.write("**Lý do từ chối:**")
        for r in reasons:
            st.write(f"- {r}")

# ================= CHI TIẾT LỊCH TRẢ NỢ PHÂN BỔ =================
st.markdown('<div class="section-title">📅 Lịch trình Trả nợ Ước tính (10 kỳ đầu tiên)</div>', unsafe_allow_html=True)

amortization_schedule = []
remaining_balance = loan_amount

for month in range(1, int(loan_term) + 1):
    interest_payment = remaining_balance * r_monthly
    principal_payment = new_monthly_payment - interest_payment
    remaining_balance -= principal_payment
    
    amortization_schedule.append({
        "Kỳ thứ": month,
        "Dư nợ đầu kỳ (VND)": round(remaining_balance + principal_payment, 2),
        "Gốc phải trả (VND)": round(principal_payment, 2),
        "Lãi phải trả (VND)": round(interest_payment, 2),
        "Tổng số tiền trả (VND)": round(new_monthly_payment, 2),
        "Dư nợ cuối kỳ (VND)": round(max(0.0, remaining_balance), 2)
    })

df_schedule = pd.DataFrame(amortization_schedule)
st.dataframe(df_schedule.head(10).style.format({
    "Dư nợ đầu kỳ (VND)": "{:,.2f}",
    "Gốc phải trả (VND)": "{:,.2f}",
    "Lãi phải trả (VND)": "{:,.2f}",
    "Tổng số tiền trả (VND)": "{:,.2f}",
    "Dư nợ cuối kỳ (VND)": "{:,.2f}"
}), use_container_width=True)
