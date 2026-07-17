import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================
# CONFIG
# ==========================

st.set_page_config(
    page_title="Loan Scoring System",
    page_icon="🏦",
    layout="wide"
)

# ==========================
# CSS
# ==========================

st.markdown("""
<style>

.stApp{
    background:linear-gradient(135deg,#edf4ff,#ffffff);
}

/* Title */

.title{
text-align:center;
font-size:42px;
font-weight:bold;
color:#003366;
}

/* Card */

.card{
background:white;
padding:25px;
border-radius:18px;
box-shadow:0px 8px 18px rgba(0,0,0,.15);
margin-bottom:20px;
}

/* Button */

.stButton>button{
width:100%;
height:55px;
background:#0052cc;
color:white;
font-size:20px;
border-radius:12px;
border:none;
font-weight:bold;
}

.stButton>button:hover{
background:#003399;
}

/* Metric */

[data-testid="metric-container"]{
background:white;
padding:15px;
border-radius:15px;
box-shadow:0 3px 10px rgba(0,0,0,.12);
}

/* Sidebar */

section[data-testid="stSidebar"]{
background:#003366;
}

section[data-testid="stSidebar"] *{
color:white;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.image(
        "https://img.icons8.com/color/480/bank-building.png",
        width=120
    )

    st.title("Loan Scoring")

    st.markdown("---")

    st.write("### Tiêu chí")

    st.write("✔ DTI < 40%")

    st.write("✔ LTV < 80%")

    st.write("✔ CIC tốt")

    st.write("✔ Thu nhập ổn định")

    st.markdown("---")

    st.success("UFM Finance Project")

# ==========================
# TITLE
# ==========================

st.markdown("""
<div class="title">
🏦 MINI LOAN SCORING SYSTEM
</div>
""", unsafe_allow_html=True)

st.caption("Ứng dụng hỗ trợ thẩm định cho vay khách hàng cá nhân")

st.markdown("---")

# ==========================
# INPUT
# ==========================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📋 Thông tin khách hàng")

col1,col2=st.columns(2)

with col1:

    loan=st.number_input(
        "💰 Số tiền vay (VNĐ)",
        value=500000000,
        step=1000000
    )

    year=st.slider(
        "📅 Thời gian vay (năm)",
        1,
        35,
        20
    )

    interest=st.slider(
        "📈 Lãi suất (%/năm)",
        1.0,
        20.0,
        9.5
    )

    income=st.number_input(
        "💵 Thu nhập hàng tháng",
        value=30000000
    )

with col2:

    dependent=st.slider(
        "👨‍👩‍👧 Người phụ thuộc",
        0,
        10,
        1
    )

    old_debt=st.number_input(
        "💳 Dư nợ khoản vay cũ",
        value=0
    )

    collateral=st.number_input(
        "🏠 Giá trị tài sản đảm bảo",
        value=800000000
    )

    cic=st.selectbox(
        "📄 Xếp hạng CIC",
        [
            "Tốt",
            "Trung bình",
            "Xấu"
        ]
    )

st.markdown("</div>",unsafe_allow_html=True)

# ==========================
# BUTTON
# ==========================

if st.button("🔍 THẨM ĐỊNH KHOẢN VAY"):

    month=year*12

    monthly_rate=interest/100/12

    payment=loan*monthly_rate/(1-(1+monthly_rate)**(-month))

    total_debt=payment+old_debt

    dti=total_debt/income

    ltv=loan/collateral

    score=100

    # DTI

    if dti>0.5:
        score-=40
    elif dti>0.4:
        score-=25
    elif dti>0.3:
        score-=10

    # LTV

    if ltv>0.8:
        score-=30
    elif ltv>0.7:
        score-=15

    # Dependent

    if dependent>=3:
        score-=10

    # CIC

    if cic=="Trung bình":
        score-=20

    elif cic=="Xấu":
        score-=50

    score=max(score,0)

    st.markdown("---")

    c1,c2,c3,c4=st.columns(4)

    c1.metric(
        "Khoản vay",
        f"{loan:,.0f}"
    )

    c2.metric(
        "DTI",
        f"{dti:.1%}"
    )

    c3.metric(
        "LTV",
        f"{ltv:.1%}"
    )

    c4.metric(
        "Điểm",
        score
    )

    col1,col2=st.columns([1,1])

    with col1:

        fig=go.Figure(go.Indicator(

            mode="gauge+number",

            value=score,

            title={"text":"Loan Score"},

            gauge={

                "axis":{"range":[0,100]},

                "bar":{"color":"darkblue"},

                "steps":[

                    {"range":[0,60],"color":"#ff6666"},

                    {"range":[60,80],"color":"#ffd633"},

                    {"range":[80,100],"color":"#66cc66"}

                ]

            }

        ))

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("📊 Kết quả")

        if score>=80:

            st.success("✅ PHÊ DUYỆT")

        elif score>=60:

            st.warning("🟠 CẦN THẨM ĐỊNH THÊM")

        else:

            st.error("❌ TỪ CHỐI")

        st.progress(score/100)

        st.write(f"### {score}/100 điểm")

        st.metric(
            "Tiền trả mỗi tháng",
            f"{payment:,.0f} VNĐ"
        )

    st.markdown("---")

    df=pd.DataFrame({

        "Chỉ tiêu":[

            "Khoản vay",

            "Thu nhập",

            "Tiền trả/tháng",

            "DTI",

            "LTV",

            "Người phụ thuộc",

            "CIC",

            "Điểm"

        ],

        "Giá trị":[

            f"{loan:,.0f}",

            f"{income:,.0f}",

            f"{payment:,.0f}",

            f"{dti:.2%}",

            f"{ltv:.2%}",

            dependent,

            cic,

            score

        ]

    })

    st.subheader("📑 Báo cáo")

    st.dataframe(
        df,
        use_container_width=True
    )

st.markdown("---")

st.markdown(
"""
<center>

### 🏦 Mini Loan Scoring System

Phát triển bằng Streamlit | Đại học Tài chính - Marketing

</center>
""",
unsafe_allow_html=True
)
