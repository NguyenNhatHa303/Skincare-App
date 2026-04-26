import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="GlowCheck - Skincare Optimizer", page_icon="✨", layout="wide")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>✨ Skincare Routine Optimizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Hệ thống tra cứu thành phần và cảnh báo xung đột mỹ phẩm tự động.</p>", unsafe_allow_html=True)
st.divider()

# ĐƯỜNG DẪN MỚI: Chỉ cần gọi tên file vì nó sẽ nằm cùng thư mục trên mạng
path = "sephora_website_dataset.csv"

try:
    df = pd.read_csv(path)
    df = df[df['ingredients'] != 'unknown']
    
    conflicts = [
        {'A': ['retinol'], 'B': ['salicylic acid', 'glycolic acid'], 'level': '❌ Xung đột', 'msg': 'Dễ gây cháy acid, rát da.', 'avoid': 'Da nhạy cảm'},
        {'A': ['vitamin c'], 'B': ['salicylic acid'], 'level': '⚠️ Cẩn trọng', 'msg': 'Nên dùng khác buổi để đạt hiệu quả tối đa.', 'avoid': 'Da khô'}
    ]

    with st.sidebar:
        st.header("⚙️ Thiết lập cá nhân")
        user_skin = st.selectbox("Loại da của bạn:", ["Da thường", "Da khô", "Da dầu", "Da mụn", "Da nhạy cảm"])
        st.info(f"Hệ thống bảo vệ cho: **{user_skin}**")

    st.subheader("🛒 Chọn Sản Phẩm")
    product_list = sorted(df['name'].unique())
    
    col1, col2 = st.columns(2)
    with col1:
        prod_1 = st.selectbox("🧴 Sản phẩm thứ nhất:", product_list)
    with col2:
        prod_2 = st.selectbox("🧴 Sản phẩm thứ hai:", product_list)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Phân Tích Chu Trình", use_container_width=True):
        with st.spinner('Đang "soi" bảng thành phần...'): 
            ing_1 = df[df['name'] == prod_1]['ingredients'].iloc[0].lower()
            ing_2 = df[df['name'] == prod_2]['ingredients'].iloc[0].lower()
            combined = ing_1 + " " + ing_2
            
            found = False
            for rule in conflicts:
                match_a = any(a in combined for a in rule['A'])
                match_b = any(b in combined for b in rule['B'])
                
                if match_a and match_b:
                    st.error(f"**{rule['level']}**: Phát hiện cặp thành phần kỵ nhau!")
                    st.warning(f"💡 Lời khuyên: {rule['msg']}")
                    if user_skin == rule['avoid']:
                        st.error(f"🚨 **BÁO ĐỘNG ĐỎ**: Combo này cực kỳ nguy hiểm với {user_skin}!")
                    found = True
            
            if not found:
                st.success(f"✅ Tuyệt vời! 2 sản phẩm này rất hòa hợp. An toàn cho {user_skin}!")
                st.balloons()

except Exception as e:
    st.error(f"Lỗi hệ thống: {e}")
