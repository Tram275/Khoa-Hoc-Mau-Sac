import streamlit as st
# Tên và icon của page 
st.set_page_config(
    page_title="Khoa học về màu sắc", layout="wide", page_icon="😸")
# Logo và tên của trường
st.markdown(
    """
    <div style="display: flex; height: 80px; border-radius: 5px; overflow: hidden;">
        <div style="background-color: white; width: 105px; display: flex; align-items: center; justify-content: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b9/Logo_Tr%C6%B0%E1%BB%9Dng_%C4%90%E1%BA%A1i_H%E1%BB%8Dc_S%C6%B0_Ph%E1%BA%A1m_K%E1%BB%B9_Thu%E1%BA%ADt_TP_H%E1%BB%93_Ch%C3%AD_Minh.png" alt="Logo" style="height: 65px;">
        </div>
        <div style="background-color: #003366; flex-grow: 1; display: flex; align-items: center; justify-content: center;">
            <h2.75 style="color: white; margin: 0;">Trường Đại học Sư phạm Kỹ thuật TP. HCM</h2.75>
        </div>
    </div>
    """,
    unsafe_allow_html=True)
# Logo và tên của khoa
st.markdown(
    """
    <div style="display: flex; height: 70px; border-radius: 5px; overflow: hidden;">
        <div style="background-color: white; width: 105px; display: flex; align-items: center; justify-content: center;">
            <img src="https://fgam.hcmute.edu.vn/Resources/Images/SubDomain/fgam/Logo%20khoa/Logo_FGAM.png" alt="Logo Khoa" style="height: 60px;">
        </div>
        <div style="background-color:#A7A8AA; flex-grow: 1; display: flex; align-items: center; justify-content: center;">
            <h3 style="color: white; margin: 0;">Khoa In và Truyền thông</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True)
# Nền màu gradient xanh dương và tím
st.markdown(
    """
    <style>
        .stApp {background: linear-gradient(to bottom, #87CEFA, #D8BFD8);}
    </style>
    """,
    unsafe_allow_html=True)
# Tiêu đề và nội dung
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px;'>
        <h3>👋 Chào mừng bạn đến với project</h3>
        <h3>🎨 Khoa Học Về Màu Sắc của mình nha</h3>
        <h3>👩‍🎓 Mình tên là Ngô Ngọc Trâm, MSSV 22158098</h3>
    </div>
    <div style='text-align: left; padding-left: 150px; padding-right: 100px;'>
        <h3>Trong project này sẽ gồm: Chuyển đổi không gian màu, Tính giá trị 3 thành phần, 
        Vẽ biểu CIE, Vẽ gamut của thiết bị RGB</h3>
    </div>
    """,
    unsafe_allow_html=True)