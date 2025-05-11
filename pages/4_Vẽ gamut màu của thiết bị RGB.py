import streamlit as st
import matplotlib.pyplot as plt
import colour
import numpy as np
# Tên và icon của page
st.set_page_config(page_title="Vẽ gamut màu của thiết bị RGB", layout="wide", page_icon="🙀")
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

colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
R = np.array([1.0, 0.0, 0.0])
G = np.array([0.0, 1.0, 0.0])
B = np.array([0.0, 0.0, 1.0])

XYZ_R = colour.sRGB_to_XYZ(R)
xyR = colour.XYZ_to_xy(XYZ_R)
xR = xyR[0]
yR = xyR[1]

XYZ_G = colour.sRGB_to_XYZ(G)
xyG = colour.XYZ_to_xy(XYZ_G)
xG = xyG[0]
yG = xyG[1]

XYZ_B = colour.sRGB_to_XYZ(B)
xyB = colour.XYZ_to_xy(XYZ_B)
xB = xyB[0]
yB = xyB[1]

tam_giac_x = [xR, xG, xB, xR]
tam_giac_y = [yR, yG, yB, yR]

plt.plot(tam_giac_x,tam_giac_y, 'k')
figure, axes = colour.plotting.render(
    show=True,
    limits=(-0.1, 0.9, -0.1, 0.9),
    x_tighten=True,
    y_tighten=True)
st.pyplot(figure, clear_figure=True)
