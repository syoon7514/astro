import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Streamlit UI 기본 설정
st.set_page_config(page_title="별의 일생 시뮬레이터", layout="centered")
st.title("🌟 별의 일생 시뮬레이터 (H-R도 기반)")
st.markdown("""
업로드한 별 이미지로부터 색과 밝기를 추정해,  
H-R도에서 별의 위치와 예상되는 진화 경로를 시각화합니다.
""")

# 1. 이미지 업로드
uploaded_file = st.file_uploader("📷 별 이미지를 업로드하세요 (JPG or PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="업로드한 별 이미지", use_column_width=True)

    # 2. 이미지 RGB 평균 추출
    resized = image.resize((100, 100))  # 빠른 처리
    pixels = np.array(resized)
    R, G, B = np.mean(pixels[:, :, 0]), np.mean(pixels[:, :, 1]), np.mean(pixels[:, :, 2])

    # 3. 색지수(B-V), 온도, 광도 추정
    color_index = 0.85 * ((B - R) / 255)
    color_index = np.clip(color_index, -0.4, 2.0)

    temperature = 9000 / (color_index + 1.5)  # 근사 공식
    luminosity = (temperature / 5800) ** 4  # 태양 대비 밝기

    log_lum = np.log10(luminosity)

    # 4. H-R도 시각화
    st.subheader("📈 H-R도 상의 별 위치")

    fig, ax = plt.subplots()
    ax.set_xlim(2.0, -0.4)
    ax.set_ylim(-2, 6)
    ax.set_xlabel("색지수 (B - V)")
    ax.set_ylabel("밝기 (log L / L☉)")
    ax.set_title("H-R Diagram")
    ax.grid(True)

    ax.scatter(color_index, log_lum, color='red', s=100, label="현재 별")
    ax.legend()
    st.pyplot(fig)

    # 5. 진화 경로 예측
    st.subheader("🔭 예상되는 별의 진화 경로")
    if luminosity > 1000:
        stage = "고질량 별 → 주계열 → 초거성 → 초신성 → 중성자별 or 블랙홀"
    elif luminosity > 10:
        stage = "중질량 별 → 주계열 → 거성 → 백색왜성"
    else:
        stage = "저질량 별 → 주계열 → 적색거성 → 백색왜성"

    st.success(f"🔎 이 별은 대략적으로: **{stage}** 경로를 따를 것으로 보입니다.")
else:
    st.info("먼저 별 이미지를 업로드해주세요. JPG 또는 PNG 형식이 가능합니다.")
