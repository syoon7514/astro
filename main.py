import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

# Streamlit 기본 설정
st.set_page_config(page_title="Animated H-R Diagram Simulator", layout="centered")
st.title("🌟 Animated H-R Diagram: Star Evolution")
st.markdown("""
Upload a star image and watch its **estimated life cycle** animate across the Hertzsprung–Russell (H-R) diagram!
""")

# 이미지 업로드
uploaded_file = st.file_uploader("📷 Upload a star image (JPG or PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Star Image", use_column_width=True)

    # RGB 평균 추출
    resized = image.resize((100, 100))
    pixels = np.array(resized)
    R, G, B = np.mean(pixels[:, :, 0]), np.mean(pixels[:, :, 1]), np.mean(pixels[:, :, 2])

    # 색지수 B–V 계산
    color_index = 0.85 * ((B - R) / 255)
    color_index = float(np.clip(color_index, -0.4, 2.0))  # 실제 B–V 값 범위로 제한
    temperature = 9000 / (color_index + 1.5)
    luminosity = (temperature / 5800) ** 4
    log_lum = np.log10(luminosity)

    st.subheader("📈 Animated H-R Diagram")

    # 진화 경로 설정
    if luminosity > 1000:
        # 고질량 별
        stages = [
            {"name": "Main Sequence", "B-V": color_index, "logL": log_lum},
            {"name": "Supergiant", "B-V": 1.8, "logL": 5.5},
            {"name": "Supernova", "B-V": 1.5, "logL": 3.0},
            {"name": "Neutron Star", "B-V": 0.2, "logL": 1.0},
        ]
    elif luminosity > 10:
        # 중질량 별
        stages = [
            {"name": "Main Sequence", "B-V": color_index, "logL": log_lum},
            {"name": "Giant", "B-V": 1.5, "logL": 3.5},
            {"name": "White Dwarf", "B-V": 0.0, "logL": -1.5},
        ]
    else:
        # 저질량 별
        stages = [
            {"name": "Main Sequence", "B-V": color_index, "logL": log_lum},
            {"name": "Red Giant", "B-V": 1.8, "logL": 3.0},
            {"name": "White Dwarf", "B-V": 0.3, "logL": -1.0},
        ]

    # 애니메이션 시각화
    fig, ax = plt.subplots()
    ax.set_xlim(2.0, -0.4)
    ax.set_ylim(-2, 6)
    ax.set_xlabel("Color Index (B - V)")
    ax.set_ylabel("Luminosity (log L / L☉)")
    ax.set_title("H-R Diagram")
    ax.grid(True)

    plot_placeholder = st.empty()

    for i, stage in enumerate(stages):
        ax.clear()
        ax.set_xlim(2.0, -0.4)
        ax.set_ylim(-2, 6)
        ax.set_xlabel("Color Index (B - V)")
        ax.set_ylabel("Luminosity (log L / L☉)")
        ax.set_title("H-R Diagram")
        ax.grid(True)

        # 지금까지의 경로 표시
        for j in range(i + 1):
            ci = stages[j]["B-V"]
            lum = stages[j]["logL"]
            label = stages[j]["name"]
            ax.scatter(ci, lum, s=120, label=label)

        ax.legend()
        plot_placeholder.pyplot(fig)
        time.sleep(1.2)  # 각 단계 사이 대기 시간

    st.success("✅ Star evolution animation complete!")

else:
    st.info("Please upload a star image (JPG or PNG) to start the animation.")
