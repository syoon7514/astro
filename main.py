# streamlit_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 상수
G = 4.302e-6  # 중력 상수 (kpc·(km/s)^2)/(Msun)

st.title("🌌 우리은하 속도 곡선 vs 이론 모델 시뮬레이터")
st.markdown("""
이 시뮬레이터는 우리은하 내 별의 **공전 속도 곡선**을 이론적 예측과 실제 관측값을 비교하여,
**암흑물질의 존재 가능성**을 시각적으로 보여줍니다.
""")

# 사용자 입력: 질량 분포 모델 선택
model = st.radio("질량 분포 모델을 선택하세요", ["중심집중 질량 (뉴턴역학)", "질량 선형 증가 모델"])

# 반지름 설정
r = np.linspace(0.1, 20, 500)  # kpc

# 질량 설정 (단순 모델)
if model == "중심집중 질량 (뉴턴역학)":
    M = np.ones_like(r) * 1e11  # 중심에 고정된 질량 10^11 Msun
elif model == "질량 선형 증가 모델":
    M = 5e9 * r  # 중심에서부터 선형 증가

# 속도 계산: v = sqrt(GM/r)
v_model = np.sqrt(G * M / r)

# 실제 관측된 은하 속도 곡선 (대략적)
r_obs = np.linspace(0.1, 20, 100)
v_obs = np.ones_like(r_obs) * 220  # 실제 은하는 속도가 거의 일정함 (평탄한 곡선)

# 그래프 출력
fig, ax = plt.subplots()
ax.plot(r, v_model, label=f"이론 속도곡선 ({model})", lw=2)
ax.plot(r_obs, v_obs, 'r--', label="관측된 속도곡선", lw=2)
ax.set_xlabel("중심으로부터 거리 (kpc)")
ax.set_ylabel("공전 속도 (km/s)")
ax.set_title("은하 회전 곡선 비교")
ax.legend()
ax.grid(True)
st.pyplot(fig)
