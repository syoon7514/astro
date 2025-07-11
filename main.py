import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import io

# Streamlit 설정
st.set_page_config(page_title="Star Evolution on H-R Diagram", layout="centered")
st.title("🌠 Star Evolution on the H-R Diagram (with Animated Path)")
st.markdown("""
Upload a **star image (JPG/PNG)** to estimate its color and brightness.  
This app will animate the **life cycle of a star** across the **Hertzsprung–Russell diagram**.
""")

# 1. 이미지 업로드
uploaded_file = st.file_uploader("📷 Upload a star image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # 이미지 로드 및 시각화
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Star Image", use_column_width=True)

    # 2. RGB 평균값 추출
    resized = image.resize((100, 100))
    pixels = np.array(resized)
    R, G, B = np.mean(pixels[:, :, 0]), np.mean(pixels[:, :, 1]), np.mean(pixels[:, :, 2])

    # 3. 색지수(B–V), 광도 계산
    color_index = 0.85 * ((B - R) / 255)
    color_index = float(np.clip(color_index, -0.4, 2.0))
    temperature = 9000 / (color_index + 1.5)
    luminosity = (temperature / 5800) ** 4
    log_lum = np.log10(luminosity)

    st.subheader("📽️ Animated Stellar Evolution on H-R Diagram")

    # 4. 별 진화 경로 설정 (예시 경로)
    path = {
        "Main Sequence": {"B-V": color_index, "logL": log_lum},
        "Red Giant": {"B-V": 1.5, "logL": 3.5},
        "Helium Burning": {"B-V": 0.8, "logL": 2.5},
        "White Dwarf": {"B-V": 0.2, "logL": -1.0}
    }

    labels = list(path.keys())
    BVs = [path[k]["B-V"] for k in labels]
    logLs = [path[k]["logL"] for k in labels]

    # 5. 애니메이션용 H-R도 설정
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(2.0, -0.4)
    ax.set_ylim(-2, 6)
    ax.set_xlabel("Color Index (B - V)")
    ax.set_ylabel("Luminosity (log L / L☉)")
    ax.set_title("Hertzsprung–Russell Diagram")
    ax.grid(True)
    ax.plot(BVs, logLs, linestyle='dashed', color='gray', alpha=0.7, label='Evolution Path')

    point, = ax.plot([], [], 'ro', markersize=10)
    label_text = ax.text(0.05, 0.92, '', transform=ax.transAxes)

    # 초기화 함수
    def init():
        point.set_data([], [])
        label_text.set_text('')
        return point, label_text

    # 프레임 업데이트 함수
    def update(frame):
        x = BVs[frame]
        y = logLs[frame]
        point.set_data(x, y)
        label_text.set_text(f"Stage: {labels[frame]}")
        return point, label_text

    # 6. 애니메이션 생성
    ani = FuncAnimation(fig, update, frames=len(labels), init_func=init,
                        blit=True, repeat=False, interval=1200)

    # 7. GIF로 저장해서 Streamlit에 표시
    gif_buffer = io.BytesIO()
    ani.save(gif_buffer, format='gif', fps=1)
    gif_buffer.seek(0)

    st.image(gif_buffer, caption="🌟 Star Evolution Animation", use_column_width=False)

    st.success("✅ Animation complete! The star's evolution has been visualized.")

else:
    st.info("Please upload a star image (JPG or PNG) to begin.")
