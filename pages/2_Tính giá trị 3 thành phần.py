import streamlit as st
import colour
import pandas as pd
# Tên và icon của page
st.set_page_config(page_title="Tính giá trị 3 thành phần", layout="wide", page_icon="😻")
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
# Nền màu gradient xanh dương và tím
st.markdown(
    """
    <style>
        .stApp {background: linear-gradient(to bottom, #87CEFA, #D8BFD8);}
    </style>
    """,
    unsafe_allow_html=True)
# Tiêu đề
st.markdown(
    """
    <div style='text-align: center; padding-top: 0px;'>
        <h2>Tính giá trị 3 thành phần</h2>
    </div>
    """,
    unsafe_allow_html=True)
# Nhập dữ liệu
csv_file = st.sidebar.file_uploader('Upload a csv file', type=['csv'])
if csv_file is not None: 
    df = pd.read_csv(csv_file)
    s = ''
    n = len(df)
    for i in range(0, 5): # Hiện 5 số đầu tiên
        key = int(df.values[i,0])
        value = df.values[i,1]
        s = s + '%3d %8.4f\n' % (key, value) 
        # %3d có độ rộng là 3 %8.4f là có độ rộng là 8 và có 4 số thập phân

    s = s + '...\n' #\n là xuống hàng

    for i in range(n-5, n): # Hiện 5 số cuối cùng
        key = int(df.values[i,0])
        value = df.values[i,1]
        s = s + '%3d %8.4f\n' % (key, value) 
        # %3d có độ rộng là 3 %8.4f là có độ rộng là 8 và có 4 số thập phân

# Tính XYZ
    st.text(s)
    if st.button('Tính XYZ'):
        n = len(df)
        dict_data = {}
        for i in range(0, n):
            key = int(df.values[i,0])
            value = df.values[i,1]
            dict_data[key] = value
        sd = colour.SpectralDistribution(dict_data)
        cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
        illuminant = colour.SDS_ILLUMINANTS['D65']
        # Tính bước sóng qua XYZ theo chuẩn
        XYZ = colour.sd_to_XYZ(sd, cmfs, illuminant)
        X = XYZ[0]
        Y = XYZ[1]
        Z = XYZ[2]
        s = 'X = %.2f, Y = %.2f, Z = %.2f' % (X, Y, Z)
        st.markdown(
                f"""
                <div style="text-align: center;">
                    <h4>{s}</h4>
                </div>
                """,
                unsafe_allow_html=True)