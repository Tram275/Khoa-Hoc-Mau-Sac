import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import json
import math
import streamlit.components.v1 as components
# Tên và icon của page
st.set_page_config(page_title="Tự chọn - Độ sai lệch và sự phối trộn màu sắc", layout="wide", page_icon="😽")
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

st.markdown("<h2 style='text-align: center;'>Độ sai lệch và sự phối trộn màu sắc</h2>", unsafe_allow_html=True)

conversion = st.sidebar.radio(
    "Độ sai lệch và sự phối trộn màu sắc:",
    ["Độ sai lệch của 2 màu trong cùng hình ảnh", "Độ sai lệch của 2 màu ở 2 hình ảnh khác nhau", "Phối trộn màu"], index=0)

if conversion == "Độ sai lệch của 2 màu trong cùng hình ảnh":
    st.info("Bạn đã chọn Độ sai lệch của 2 màu trong cùng hình ảnh")
    with st.sidebar:
        uploaded_file = st.file_uploader("Tải ảnh lên", type=["png", "jpg", "jpeg", "tif"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert("RGB")
        MAX_SIZE = (512, 512)
        img.thumbnail(MAX_SIZE, Image.LANCZOS)
        width, height = img.size

        buf = BytesIO()
        img.save(buf, format="PNG")
        img_b64 = base64.b64encode(buf.getvalue()).decode()

        st.markdown("## Click vào ảnh để chọn 2 điểm:")

        html_code = f"""
        <canvas id="canvas" width="{width}" height="{height}" style="border:1px solid #ccc;"></canvas>
        <p id="status"> Click vào ảnh để chọn màu</p>
        <textarea id="jsonbox" rows="5" cols="60" placeholder="JSON 2 điểm sẽ hiện ở đây sau khi chọn đủ..."></textarea>

        <script>
            const canvas = document.getElementById("canvas");
            const ctx = canvas.getContext("2d");
            const img = new Image();
            img.src = "data:image/png;base64,{img_b64}";

            let points = [];
            let clicks = 0;

            img.onload = function() {{
                ctx.drawImage(img, 0, 0);
            }};

            canvas.addEventListener("click", function(e) {{
                const rect = canvas.getBoundingClientRect();
                const x = Math.round(e.clientX - rect.left);
                const y = Math.round(e.clientY - rect.top);
                const pixel = ctx.getImageData(x, y, 1, 1).data;
                points.push({{ x: x, y: y, r: pixel[0], g: pixel[1], b: pixel[2] }});
                clicks++;

                document.getElementById("status").textContent = "RGB(" + pixel[0] + ", " + pixel[1] + ", " + pixel[2] + ") tại (" + x + ", " + y + ")";

                if (clicks === 2) {{
                    document.getElementById("jsonbox").value = JSON.stringify(points);
                    points = [];
                }}
            }});
        </script>
        """

        components.html(html_code, height=height + 100)
        user_input = st.text_area("Dán JSON 2 điểm để tính ΔE2000:", height=100)

        def rgb_to_lab(r, g, b):
            r, g, b = [x / 255.0 for x in (r, g, b)]

            def correct(c):
                return pow((c + 0.055) / 1.055, 2.4) if c > 0.04045 else c / 12.92

            r, g, b = correct(r), correct(g), correct(b)

            x = r * 0.4124 + g * 0.3576 + b * 0.1805
            y = r * 0.2126 + g * 0.7152 + b * 0.0722
            z = r * 0.0193 + g * 0.1192 + b * 0.9505

            x /= 0.95047
            y /= 1.00000
            z /= 1.08883

            def f(t):
                return pow(t, 1/3) if t > 0.008856 else (7.787 * t) + (16 / 116)

            l = 116 * f(y) - 16
            a = 500 * (f(x) - f(y))
            b = 200 * (f(y) - f(z))
            return (l, a, b)

        def delta_e2000(lab1, lab2):
            return math.sqrt(sum((a - b) ** 2 for a, b in zip(lab1, lab2)))

        if user_input:
            try:
                points = json.loads(user_input)
                if len(points) != 2:
                    st.error("Vui lòng chọn đúng 2 điểm!")
                else:
                    p1, p2 = points
                    lab1 = rgb_to_lab(p1['r'], p1['g'], p1['b'])
                    lab2 = rgb_to_lab(p2['r'], p2['g'], p2['b'])
                    delta_e = delta_e2000(lab1, lab2)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f" Điểm 1: ({p1['x']},{p1['y']}) - RGB({p1['r']},{p1['g']},{p1['b']})")
                        st.color_picker("Màu 1", f"#{p1['r']:02x}{p1['g']:02x}{p1['b']:02x}", label_visibility="collapsed")
                    with col2:
                        st.markdown(f" Điểm 2: ({p2['x']},{p2['y']}) - RGB({p2['r']},{p2['g']},{p2['b']})")
                        st.color_picker("Màu 2", f"#{p2['r']:02x}{p2['g']:02x}{p2['b']:02x}", label_visibility="collapsed")

                    st.success(f"ΔE2000: **{delta_e:.1f}**")
            except Exception as e:
                st.error(f"JSON không hợp lệ: {e}")

if conversion == "Độ sai lệch của 2 màu ở 2 hình ảnh khác nhau":
    st.info("Bạn đã chọn Độ sai lệch của 2 màu ở 2 hình ảnh khác nhau")
    with st.sidebar:
        uploaded_file1 = st.file_uploader("Tải ảnh thứ nhất", type=["png", "jpg", "jpeg", "tif"])
        uploaded_file2 = st.file_uploader("Tải ảnh thứ hai", type=["png", "jpg", "jpeg", "tif"])

    if uploaded_file1 and uploaded_file2:
        img1 = Image.open(uploaded_file1).convert("RGB")
        img2 = Image.open(uploaded_file2).convert("RGB")

        if img1.mode in ("RGBA", "LA"):
            background1 = Image.new("RGB", img1.size, (255, 255, 255))
            background1.paste(img1, mask=img1.split()[-1])
            img1 = background1

        if img2.mode in ("RGBA", "LA"):
            background2 = Image.new("RGB", img2.size, (255, 255, 255))
            background2.paste(img2, mask=img2.split()[-1])
            img2 = background2

        MAX_SIZE = (512, 512)
        img1.thumbnail(MAX_SIZE, Image.LANCZOS)
        img2.thumbnail(MAX_SIZE, Image.LANCZOS)

        width1, height1 = img1.size
        width2, height2 = img2.size

        buf1 = BytesIO()
        img1.save(buf1, format="PNG")
        img_b64_1 = base64.b64encode(buf1.getvalue()).decode()

        buf2 = BytesIO()
        img2.save(buf2, format="PNG")
        img_b64_2 = base64.b64encode(buf2.getvalue()).decode()

        st.markdown("## Click vào ảnh để chọn 1 điểm:")

        html_code1 = f"""
        <canvas id="canvas1" width="{width1}" height="{height1}" style="border:1px solid #ccc;"></canvas>
        <p id="status1"> Click vào ảnh đầu tiên để chọn màu</p>
        <textarea id="jsonbox1" rows="5" cols="60" placeholder="JSON điểm của ảnh 1 sẽ hiện ở đây sau khi chọn đủ..."></textarea>
        <script>
            const canvas1 = document.getElementById("canvas1");
            const ctx1 = canvas1.getContext("2d");
            const img1 = new Image();
            img1.src = "data:image/png;base64,{img_b64_1}";
            let points1 = [];
            let clicks1 = 0;
            img1.onload = function() {{
                ctx1.drawImage(img1, 0, 0);
            }}; 
            canvas1.addEventListener("click", function(e) {{
                const rect = canvas1.getBoundingClientRect();
                const x = Math.round(e.clientX - rect.left);
                const y = Math.round(e.clientY - rect.top);
                const pixel = ctx1.getImageData(x, y, 1, 1).data;
                points1.push({{ x: x, y: y, r: pixel[0], g: pixel[1], b: pixel[2] }});
                clicks1++;
                document.getElementById("status1").textContent = "RGB(" + pixel[0] + ", " + pixel[1] + ", " + pixel[2] + ") tại (" + x + ", " + y + ")";
                if (clicks1 === 1) {{
                    document.getElementById("jsonbox1").value = JSON.stringify(points1);
                    points1 = [];
                }}
            }});
        </script>
        """

        html_code2 = f"""
        <canvas id="canvas2" width="{width2}" height="{height2}" style="border:1px solid #ccc;"></canvas>
        <p id="status2"> Click vào ảnh thứ hai để chọn màu</p>
        <textarea id="jsonbox2" rows="5" cols="60" placeholder="JSON điểm của ảnh 2 sẽ hiện ở đây sau khi chọn đủ..."></textarea>
        <script>
            const canvas2 = document.getElementById("canvas2");
            const ctx2 = canvas2.getContext("2d");
            const img2 = new Image();
            img2.src = "data:image/png;base64,{img_b64_2}";
            let points2 = [];
            let clicks2 = 0;
            img2.onload = function() {{
                ctx2.drawImage(img2, 0, 0);
            }}; 
            canvas2.addEventListener("click", function(e) {{
                const rect = canvas2.getBoundingClientRect();
                const x = Math.round(e.clientX - rect.left);
                const y = Math.round(e.clientY - rect.top);
                const pixel = ctx2.getImageData(x, y, 1, 1).data;
                points2.push({{ x: x, y: y, r: pixel[0], g: pixel[1], b: pixel[2] }});
                clicks2++;
                document.getElementById("status2").textContent = "RGB(" + pixel[0] + ", " + pixel[1] + ", " + pixel[2] + ") tại (" + x + ", " + y + ")";
                if (clicks2 === 1) {{
                    document.getElementById("jsonbox2").value = JSON.stringify(points2);
                    clicks2 = 0;
                    points2 = [];
                }}
            }});
        </script>
        """

        components.html(html_code1, height=height1 + 100)
        components.html(html_code2, height=height2 + 100)

        json_input = st.text_area("Dán JSON điểm màu từ ảnh 1 và 2:", height=100)
        def rgb_to_lab(r, g, b):
            r, g, b = [x / 255.0 for x in (r, g, b)]

            def correct(c):
                return pow((c + 0.055) / 1.055, 2.4) if c > 0.04045 else c / 12.92

            r, g, b = correct(r), correct(g), correct(b)

            x = r * 0.4124 + g * 0.3576 + b * 0.1805
            y = r * 0.2126 + g * 0.7152 + b * 0.0722
            z = r * 0.0193 + g * 0.1192 + b * 0.9505

            x /= 0.95047
            y /= 1.00000
            z /= 1.08883

            def f(t):
                return pow(t, 1/3) if t > 0.008856 else (7.787 * t) + (16 / 116)

            l = 116 * f(y) - 16
            a = 500 * (f(x) - f(y))
            b = 200 * (f(y) - f(z))
            return (l, a, b)

        def delta_e2000(lab1, lab2):
            return math.sqrt(sum((a - b) ** 2 for a, b in zip(lab1, lab2)))

        if json_input:
            try:
                data = json.loads(json_input)
                if not isinstance(data, list) or len(data) != 2:
                    st.error("JSON phải là một mảng gồm đúng 2 đối tượng (mỗi ảnh 1 điểm màu). Ví dụ: "
                     '[{"x": 282, "y": 100, "r": 156, "g": 50, "b": 30}, {"x": 282, "y": 100, "r": 160, "g": 55, "b": 35}]')
                else:
                    p1, p2 = data

                    lab1 = rgb_to_lab(p1['r'], p1['g'], p1['b'])
                    lab2 = rgb_to_lab(p2['r'], p2['g'], p2['b'])
                    delta_e1 = delta_e2000(lab1, lab2)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Điểm 1 (Ảnh 1)**: ({p1['x']},{p1['y']}) - RGB({p1['r']},{p1['g']},{p1['b']})")
                        st.color_picker("Màu 1", f"#{p1['r']:02x}{p1['g']:02x}{p1['b']:02x}", label_visibility="collapsed")
                    with col2:
                        st.markdown(f"**Điểm 2 (Ảnh 2)**: ({p2['x']},{p2['y']}) - RGB({p2['r']},{p2['g']},{p2['b']})")
                        st.color_picker("Màu 2", f"#{p2['r']:02x}{p2['g']:02x}{p2['b']:02x}", label_visibility="collapsed")

                    st.success(f"ΔE2000: **{delta_e1:.2f}**")
            except json.JSONDecodeError as e:
                st.error("JSON không hợp lệ. Kiểm tra cú pháp (không dấu phẩy cuối, dùng dấu ngoặc kép cho key). Ví dụ:\n"
                        '[{"x": 282, "y": 100, "r": 156, "g": 50, "b": 30}, {"x": 282, "y": 100, "r": 160, "g": 55, "b": 35}]')
if conversion == "Phối trộn màu":
    st.info("Bạn đã chọn Phối trộn màu")
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def rgb_to_cmyk(r, g, b):
        if (r, g, b) == (0, 0, 0):
            return 0, 0, 0, 100
        c = 1 - r / 255
        m = 1 - g / 255
        y = 1 - b / 255
        k = min(c, m, y)
        c = (c - k) / (1 - k) if (1 - k) else 0
        m = (m - k) / (1 - k) if (1 - k) else 0
        y = (y - k) / (1 - k) if (1 - k) else 0
        return round(c * 100, 2), round(m * 100, 2), round(y * 100, 2), round(k * 100, 2)

    def average_rgb_blend(colors_rgb):
        n = len(colors_rgb)
        r = sum(c[0] for c in colors_rgb) // n
        g = sum(c[1] for c in colors_rgb) // n
        b = sum(c[2] for c in colors_rgb) // n
        return (r, g, b)

    num_colors = st.selectbox("Chọn số màu để trộn:", [2, 3, 4, 5], index=0)

    colors_hex = []
    for i in range(num_colors):
        color = st.color_picker(f"Màu {i+1}", "#ffffff")
        colors_hex.append(color)

    colors_rgb = []
    for idx, hex_color in enumerate(colors_hex):
        rgb = hex_to_rgb(hex_color)
        cmyk = rgb_to_cmyk(*rgb)
        colors_rgb.append(rgb)

    mixed_rgb = average_rgb_blend(colors_rgb)
    mixed_hex = rgb_to_hex(mixed_rgb)
    mixed_cmyk = rgb_to_cmyk(*mixed_rgb)

    rgb_str = ', '.join(str(x) for x in mixed_rgb)
    cmyk_str = ', '.join(f"{x:.2f}" for x in mixed_cmyk)

    st.markdown(f"""
    <p><strong style="color:black">RGB:</strong> 
       <span style="background-color:transparent; color:black; padding:3px 6px; border-radius:4px;">{rgb_str}</span></p>
    <p><strong style="color:black">HEX:</strong> 
       <span style="background-color:transparent; color:black; padding:3px 6px; border-radius:4px;">{mixed_hex}</span></p>
    <p><strong style="color:black">CMYK:</strong> 
       <span style="background-color:transparent; color:black; padding:3px 6px; border-radius:4px;">{cmyk_str}</span></p>
    """,
    unsafe_allow_html=True)
    
    text_color = "#fff" if sum(mixed_rgb) / 3 < 128 else "#000"
    st.markdown(
        f"""
        <div style="width:160px;height:160px;
                    background-color:{mixed_hex};
                    border:2px solid #000;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:{text_color};
                    font-weight:bold;">
        </div>
        """,
        unsafe_allow_html=True)
