import streamlit as st
import matplotlib.pyplot as plt
import colour
import numpy as np
import pandas as pd

# Tên và icon của page
st.set_page_config(page_title="Vẽ gamut màu của thiết bị in", layout="wide", page_icon="😹")

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
        <h2>Vẽ gamut màu của thiết bị in</h2>
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

def process_file():
    if st.session_state["dem"] == 1:
        st.session_state["dem"] = 0

col1, col2 = st.columns(2)

if "data_point" not in st.session_state:
    st.session_state["data_point"] = None 
    st.session_state["dem"] = 0
else:
    print('Đã load file csv')

if st.session_state["dem"] == 0:
    figure, axes = colour.plotting.plot_chromaticity_diagram_CIE1931()
    axes.set_xlim([-0.1, 0.85])
    axes.set_ylim([-0.1, 0.90])
    axes.set_title('CIE 1931 Chromaticity Diagram\n2 Degree Standard Observer')
    col1.empty()
    col1.pyplot(figure)
else:
    df = st.session_state["data_point"]
    px = np.zeros(7, np.float64)
    py = np.zeros(7, np.float64)

    Lab = df['R'].to_numpy()
    XYZ = colour.Lab_to_XYZ(Lab)
    xy = colour.XYZ_to_xy(XYZ)
    px[0] = xy[0]
    py[0] = xy[1]

    Lab = df['Y'].to_numpy()
    XYZ = colour.Lab_to_XYZ(Lab)
    xy = colour.XYZ_to_xy(XYZ)
    px[1] = xy[0]
    py[1] = xy[1]

    Lab = df['G'].to_numpy()
    XYZ = colour.Lab_to_XYZ(Lab)
    xy = colour.XYZ_to_xy(XYZ)
    px[2] = xy[0]
    py[2] = xy[1]

    Lab = df['C'].to_numpy()
    XYZ = colour.Lab_to_XYZ(Lab)
    xy = colour.XYZ_to_xy(XYZ)
    px[3] = xy[0]
    py[3] = xy[1]

    Lab = df['B'].to_numpy()
    XYZ = colour.Lab_to_XYZ(Lab)
    xy = colour.XYZ_to_xy(XYZ)
    px[4] = xy[0]
    py[4] = xy[1]

    Lab = df['M'].to_numpy()
    XYZ = colour.Lab_to_XYZ(Lab)
    xy = colour.XYZ_to_xy(XYZ)
    px[5] = xy[0]
    py[5] = xy[1]

    px[6] = px[0]
    py[6] = py[0]

    figure, axes = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
    axes.set_xlim([-0.1, 0.85])
    axes.set_ylim([-0.1, 0.90])
    axes.set_title('CIE 1931 Chromaticity Diagram\n2 Degree Standard Observer')
    plt.plot(px, py, 'k')
    figure, axes = colour.plotting.render(
        show=True,
        x_tighten=True,
        y_tighten=True)
    col1.empty()
    col1.pyplot(figure, clear_figure=True)

csv_file = st.sidebar.file_uploader("Upload a csv color gamut file", type=["csv"], on_change=process_file)
if csv_file is not None:
    df = pd.read_csv(csv_file)
    df = df.set_index('ColorSpace')
    col2.empty()
    col2.write(df)
    if col2.button('Plot'):
        st.session_state["data_point"] = df
        st.session_state["dem"] = 1
        st.rerun()
