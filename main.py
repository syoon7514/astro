import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# 페이지 제목
st.set_page_config(page_title="FITS 기반 별의 일생 시뮬레이터", layout="centered")
st.title("🌠 FITS 기반 별의 일생 시뮬레이터")
st.markdown("""
업로드된 **FITS 천체 이미지**를 분석하여 별의 밝기와 색지수를 추정하고,  
**H-R도(Hertzsprung–Russell Diagram)** 상의 위치를 표시하며,  
그 별의 **진화 경로**를 예측합니다.
""")

# -----------------------------
# 1. FITS 이미지 업로드
# -----------------------------
uploaded_file = st.file_uploader("📂 FITS 형식의 별 이미지를 업로드하세요", type=["fits", "fit"])

if uploaded_file:
    try:
        # FITS 파일 열기 및 데이터 추출
        with fits.open(uploaded_file) as hdul:
            data = hdul[0].data

        if data is None or len(data.shape) < 2:
            st.error("이 FITS 파일에는 2차원 이미지 데이터가 없습니다.")
            st.stop()

        # 결측치 제거
        data = np.nan_to_num(data)
        height, width = data.shape

        # -----------------------------
        # 2. 중심 부근 밝기 추정
        # -----------------------------
        center_crop = data[height//2 - 20:height//2 + 20, width//2 - 20:width//2 + 20]
        brightness = np.mean(center_crop)
        brightness_norm = brightness / np.max(data)

        # -----------------------------
        # 3. 광도 및 색지수 추정
        # -----------------------------
        log_L = 5 * brightness_norm  # 임의 스케일
        B_V = np.clip(2.0 - 4 * brightness_norm, -0.4, 2.0)  # 밝을수록 파랗게 추정

        # -----------------------------
        # 4. H-R도 시각화
        # -----------------------------
        st.subheader("📈 H-R도 상의 별 위치 (추정)")

        fig, ax = plt.subplots()
        ax.set_xlim(2.0, -0.4)  # B-V 좌표: 붉은 별 → 파란 별
        ax.set_ylim(-2, 6)  # log L
        ax.set_xlabel("색지수 (B - V)")
        ax.set_ylabel("밝기 (log L / L☉)")
        ax.set_title("Hertzsprung-Russell Diagram")
        ax.grid(True)
        ax.scatter(B_V, log_L, s=120, color='red', label="업로드한 별")
        ax.legend()
        st.pyplot(fig)

        # -----------------------------
        # 5. 별의 진화 경로 해석
        # -----------------------------
        L = 10 ** log_L  # 절대 광도로 복원

        st.subheader("🔭 별의 진화 경로 예측")
        if L > 1000:
            route = "고질량 별 → 주계열 → 초거성 → 초신성 → 중성자별 또는 블랙홀"
        elif L > 10:
            route = "중질량 별 → 주계열 → 거성 → 백색왜성"
        else:
            route = "저질량 별 → 주계열 → 적색거성 → 백색왜성"

        st.success(f"이 별은 대략적으로: **{route}** 경로를 따를 것으로 보입니다.")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("FITS 파일을 업로드하면 분석이 시작됩니다. 예: HST, SDSS 이미지 등")
