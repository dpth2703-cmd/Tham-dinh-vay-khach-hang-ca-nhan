import streamlit as st
import pandas as pd

# Cấu hình giao diện chuyên nghiệp
st.set_page_config(
    page_title="Hệ thống Thẩm định Tín dụng Cá nhân",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo CSS tùy chỉnh để trang trí giao diện và thanh chỉ số màu sắc
st.markdown("""
    <style>
    .main-title {
        font-size:32px !important;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #4B5563;
        font-size: 16px;
        margin-bottom: 25px;
    }
    .section-title {
        font-size:20px !important;
        font-weight: bold;
        color: #0D9488;
        border-bottom: 2px solid #0D9488;
        padding-bottom: 5px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .metric-box {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .progress-bg {
        background-color: #E5E7EB;
        border-radius: 10px;
        width: 100%;
        height: 20px;
        margin-top: 8px;
        margin-bottom: 15px;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        text-align: right;
        padding-right: 10px;
        color: white;
        font-size: 12px;
        font-weight: bold;
        line-height: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏦 HỆ THỐNG THẨM ĐỊNH CHO VAY KHÁCH HÀNG CÁ NHÂN</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Công cụ hỗ trợ phân tích năng lực tài chính, đánh giá khả năng trả nợ và phê duyệt khoản vay tự động</div>', unsafe_allow_html=True)
st.write("---")

# ================= SIDEBAR: NHẬP THÔNG TIN KHÁCH HÀNG =================
st.sidebar.header("📁 THÔNG TIN ĐẦU VÀO")

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
    cic_group = st.selectbox(
        "Nhóm nợ CIC hiện tại", 
        options=[
            "Nhóm 1 (Nợ đủ tiêu chuẩn)", 
            "Nhóm 2 (Nợ cần chú ý)", 
            "Nhóm 3 (Nợ dưới tiêu chuẩn)", 
            "Nhóm 4 (Nợ nghi ngờ)", 
            "Nhóm 5 (Nợ có khả năng mất vốn)"
        ]
    )

# ================= XỬ LÝ LOGIC VÀ TÍNH TOÁN =================

# 1. Tính toán khoản thanh toán hàng tháng (EMI) cho khoản vay mới (Công thức gốc và lãi chia đều)
r_monthly = (interest_rate / 100) / 12
if r_monthly > 0:
    new_monthly_payment = loan_amount * r_monthly * ((1 + r_monthly) ** loan_term) / (((1 + r_monthly) ** loan_term) - 1)
else:
    new_monthly_payment = loan_amount / loan_term

# Làm tròn 2 chữ số sau dấu phẩy
new_monthly_payment = round(new_monthly_payment, 2)
total_monthly_debt_service = round(new_monthly_payment + old_monthly_payment, 2)

# 2. Tính chỉ số DTI (Debt-to-Income)
dti = round((total_monthly_debt_service / monthly_income) * 100, 2) if monthly_income > 0 else 100.0

# 3. Tính chỉ số LTV / LAV (Loan-to-Value)
ltv = round((loan_amount / collateral_value) * 100, 2)

# 4. Tính toán chi phí sinh hoạt của người phụ thuộc (ước tính 3.000.000 VND/người)
living_cost_per_person = 3000000.0
total_living_cost = round(dependents * living_cost_per_person, 2)
disposable_income = round(monthly_income - total_living_cost - total_monthly_debt_service, 2)

# ================= GIAO DIỆN CHÍNH: HIỂN THỊ KẾT QUẢ =================

col1, col2 = st.columns([1.8, 1.2])

with col1:
    st.markdown('<div class="section-title">📊 Các Chỉ số Thẩm định Tài chính</div>', unsafe_allow_html=True)
    
    # Hiển thị các khối Metric đẹp mắt
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><b>Nghĩa vụ mới / tháng</b><br><span style="font-size:18px; color:#1E3A8A; font-weight:bold;">{new_monthly_payment:,.2f} VND</span></div>', unsafe_allow_html=True)
    with m2:
        dti_color = "#10B981" if dti <= 55 else "#EF4444"
        st.markdown(f'<div class="metric-box"><b>Tỷ lệ DTI</b><br><span style="font-size:18px; color:{dti_color}; font-weight:bold;">{dti:.2f}%</span></div>', unsafe_allow_html=True)
    with m3:
        ltv_color = "#10B981" if ltv <= 70 else "#EF4444"
        st.markdown(f'<div class="metric-box"><b>Tỷ lệ LTV (LAV)</b><br><span style="font-size:18px; color:{ltv_color}; font-weight:bold;">{ltv:.2f}%</span></div>', unsafe_allow_html=True)

    # Biểu diễn trực quan tỷ lệ bằng Thanh tiến độ (Progress Bar) động tự viết bằng CSS
    st.markdown("🔍 **Độ an toàn của các chỉ số tài chính:**")
    
    # DTI Progress Bar (Mức trần thông thường: 55%)
    dti_percentage = min(100.0, dti)
    dti_fill_color = "#10B981" if dti <= 55 else "#EF4444"
    st.write(f"Tỷ lệ Nợ trên Thu nhập (DTI) - Hạn mức tối đa: 55%")
    st.markdown(f"""
        <div class="progress-bg">
            <div class="progress-fill" style="width: {dti_percentage:.2f}%; background-color: {dti_fill_color};">
                {dti:.2f}%
            </div>
        </div>
    """, unsafe_allow_html=True)

    # LTV Progress Bar (Mức trần thông thường: 70%)
    ltv_percentage = min(100.0, ltv)
    ltv_fill_color = "#10B981" if ltv <= 70 else "#EF4444"
    st.write(f"Tỷ lệ Khoản vay trên Tài sản bảo đảm (LTV) - Hạn mức tối đa: 70%")
    st.markdown(f"""
        <div class="progress-bg">
            <div class="progress-fill" style="width: {ltv_percentage:.2f}%; background-color: {ltv_fill_color};">
                {ltv:.2f}%
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Phân tích Thu nhập tích lũy
    st.write("📈 **Cân đối dòng tiền hàng tháng của khách hàng:**")
    balance_data = {
        "Hạng mục chi phí": ["Tổng thu nhập hàng tháng", "Trả nợ cũ hàng tháng", "Nghĩa vụ trả nợ mới", "Ước tính chi tiêu sinh hoạt", "Thu nhập khả dụng còn dư"],
        "Số tiền (VND)": [monthly_income, old_monthly_payment, new_monthly_payment, total_living_cost, disposable_income]
    }
    df_balance = pd.DataFrame(balance_data)
    st.dataframe(df_balance.style.format({"Số tiền (VND)": "{:,.2f}"}), use_container_width=True, hide_index=True)

with col2:
    st.markdown('<div class="section-title">📝 Quyết định Thẩm định Tự động</div>', unsafe_allow_html=True)
    
    # Tiêu chuẩn thẩm định tự động (Policy Rules)
    dti_threshold = 55.0
    ltv_threshold = 70.0
    
    reasons = []
    approved = True
    
    # Đánh giá DTI
    if dti > dti_threshold:
        approved = False
        reasons.append(f"Tỷ lệ Nợ/Thu nhập (DTI) {dti:.2f}% vượt quá giới hạn an toàn {dti_threshold:.2f}%.")
        
    # Đánh giá LTV
    if ltv > ltv_threshold:
        approved = False
        reasons.append(f"Tỷ lệ LTV {ltv:.2f}% vượt ngưỡng quy định {ltv_threshold:.2f}% đối với tài sản đảm bảo.")
        
    # Đánh giá CIC
    if cic_group != "Nhóm 1 (Nợ đủ tiêu chuẩn)":
        if cic_group == "Nhóm 2 (Nợ cần chú ý)":
            reasons.append("⚠️ Lưu ý: Khách hàng thuộc CIC Nhóm 2. Cần trình giải trình chi tiết về lịch sử trễ hạn.")
        else:
            approved = False
            reasons.append(f"Từ chối thẳng: Khách hàng thuộc {cic_group} (nợ xấu cấp độ cao).")
            
    # Đánh giá Thu nhập tích lũy còn dư
    if disposable_income < 0:
        approved = False
        reasons.append("Thu nhập khả dụng sau khi trừ các chi phí thiết yếu và gốc lãi bị âm.")

    # Hiển thị kết quả quyết định trực quan
    if approved:
        if cic_group == "Nhóm 2 (Nợ cần chú ý)":
            st.warning("⚠️ ĐỀ XUẤT: PHÊ DUYỆT CÓ ĐIỀU KIỆN (CIC nhóm 2)")
        else:
            st.success("✅ ĐỀ XUẤT: PHÊ DUYỆT KHOẢN VAY")
        st.info("💡 **Ghi chú:** Khách hàng đạt đủ toàn bộ các điều kiện và chỉ số an toàn tài chính theo quy định hiện hành.")
    else:
        st.error("❌ ĐỀ XUẤT: TỪ CHỐI DUYỆT HỒ SƠ")
        st.write("**Lý do không đạt tiêu chí phê duyệt:**")
        for r in reasons:
            st.write(f"- {r}")

# ================= BẢNG LỊCH TRÌNH TRẢ NỢ (AMORTIZATION SCHEDULE) =================
st.markdown('<div class="section-title">📅 Chi tiết Lịch trình Trả nợ Ước tính (10 kỳ đầu)</div>', unsafe_allow_html=True)

amortization_schedule = []
remaining_balance = loan_amount

for month in range(1, int(loan_term) + 1):
    interest_payment = round(remaining_balance * r_monthly, 2)
    principal_payment = round(new_monthly_payment - interest_payment, 2)
    remaining_balance = round(remaining_balance - principal_payment, 2)
    
    # Đảm bảo kỳ cuối cùng không bị lệch lẻ do làm tròn
    if month == int(loan_term) or remaining_balance < 0:
        principal_payment = round(remaining_balance + principal_payment, 2)
        remaining_balance = 0.00
    
    amortization_schedule.append({
        "Kỳ thứ": month,
        "Dư nợ đầu kỳ (VND)": round(remaining_balance + principal_payment, 2),
        "Gốc phải trả (VND)": round(principal_payment, 2),
        "Lãi phải trả (VND)": round(interest_payment, 2),
        "Tổng số tiền trả (VND)": round(new_monthly_payment, 2),
        "Dư nợ cuối kỳ (VND)": round(remaining_balance, 2)
    })

df_schedule = pd.DataFrame(amortization_schedule)
st.dataframe(
    df_schedule.head(10).style.format({
        "Dư nợ đầu kỳ (VND)": "{:,.2f}",
        "Gốc phải trả (VND)": "{:,.2f}",
        "Lãi phải trả (VND)": "{:,.2f}",
        "Tổng số tiền trả (VND)": "{:,.2f}",
        "Dư nợ cuối kỳ (VND)": "{:,.2f}"
    }), 
    use_container_width=True, 
    hide_index=True
)
