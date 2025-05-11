import streamlit as st
import numpy as np
import colour
# Tên và icon của page
st.set_page_config(page_title="Chuyển đổi không gian màu", layout="wide", page_icon="😹")
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
# Tiêu đề
st.markdown(
    """
    <div style='text-align: center; padding-top: 0px;'>
        <h2>Chuyển đổi không gian màu</h2>
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
# Chuyển đổi
chon_khong_gian_mau = st.sidebar.radio('Chuyển đổi không gian màu', ('sRGB to XYZ', 'XYZ to sRGB','XYZ to Lab'))
col1, col2 = st.columns(2)
if chon_khong_gian_mau == 'sRGB to XYZ':
    with col1:
        st.write('### sRGB to XYZ')
        R = st.number_input('Nhập R: ', min_value=0, max_value=255)
        G = st.number_input('Nhập G: ', min_value=0, max_value=255)
        B = st.number_input('Nhập B: ', min_value=0, max_value=255)
        if st.button('Chuyển sang XYZ'):
            R = R/255.0
            G = G/255.0
            B = B/255.0
            RGB = np.array([R, G, B])
            XYZ = colour.sRGB_to_XYZ(RGB)
            X = XYZ[0]*100
            Y = XYZ[1]*100
            Z = XYZ[2]*100
            s = '### X = %.2f, Y = %.2f, Z = %.2f' % (X, Y, Z)
            st.write(s)
elif chon_khong_gian_mau == 'XYZ to sRGB':
    with col1:
        st.write('### XYZ to sRGB')
        X = st.number_input('Nhập X: ')
        Y = st.number_input('Nhập Y: ')
        Z = st.number_input('Nhập Z: ')
        if st.button('Chuyển sang sRGB'):
            X = X/100.0
            Y = Y/100.0
            Z = Z/100.0
            XYZ = np.array([X, Y, Z])
            RGB = colour.XYZ_to_sRGB(XYZ)
            R = RGB[0]*255
            G = RGB[1]*255
            B = RGB[2]*255
            s = '### R = %.0f, G = %.0f, B = %.0f' % (R, G, B) # .0f: Số 0 là số lượng số thập phân
            st.write(s)
elif chon_khong_gian_mau == 'XYZ to Lab':
    with col1:
        st.write('### XYZ to Lab')
        X = st.number_input('Nhập X: ')
        Y = st.number_input('Nhập Y: ')
        Z = st.number_input('Nhập Z: ')
        if st.button('Chuyển sang Lab'):
            X = X/100.0
            Y = Y/100.0
            Z = Z/100.0
            XYZ = np.array([X, Y, Z])
            Lab = colour.XYZ_to_Lab(XYZ)
            L = Lab[0]
            a = Lab[1]
            b = Lab[2]
            s = '### L = %.2f, a = %.2f, b = %.2f' % (L, a, b) # .0f: Số 0 là số lượng số thập phân
            st.write(s)
