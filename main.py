import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🌌 은하 회전 곡선 시뮬레이터")
st.markdown("""
이 시뮬레이터는 은하 내 별들의 공전 속도를 반지름에 따라 나타낸 그래프를 통해, 암흑물질의 존재 가능성을 시각적으로 보여줍니다.
""")

# -----------------------------
# 1. 입력 데이터 설정
# -----------------------------
st.header("🔧 반지름-속도 데이터 설정")

default_r = np.linspace(0.1, 20, 100)
default_v_obs = np.concatenate([
    np.sqrt(default_r[:30] * 50),
    np.full(70, np.sqrt(30 * 50))
])

# 사용자 커스터마이즈
r = st.slider("반지름 범위 (kpc)", 5, 50, 20)
mass_distribution = st.selectbox("질량 분포 가정", ["구형 분포 (M∝r³)", "균등 분포 (M∝r)"])

r_vals = np.linspace(0.1, r, 100)

# -----------------------------
# 2. 뉴턴 예측 속도 계산
# -----------------------------
G = 4.3e-6  # kpc (km/s)^2 / Msun, 은하 단위에 맞춘 중력상수
if mass_distribution == "구형 분포 (M∝r³)":
    M = r_vals ** 3
else:
    M = r_vals

v_newton = np.sqrt(G * M / r_vals)

# -----------------------------
# 3. 관측 속도 설정 (플랫한 속도 곡선)
# -----------------------------
# 관측 속도는 r=5kpc 이후부터는 평평한 속도 유지
v_obs = np.concatenate([
    np.sqrt(r_vals[:30] * 50),
    np.full(len(r_vals) - 30, np.sqrt(30 * 50))
])

# -----------------------------
# 4. 시각화
# -----------------------------
st.header("📊 회전 곡선 그래프")

fig, ax = plt.subplots()
ax.plot(r_vals, v_newton, label="예측 속도 (뉴턴 역학)", linestyle='--')
ax.plot(r_vals, v_obs, label="관측 속도", linestyle='-')
ax.set_xlabel("반지름 (kpc)")
ax.set_ylabel("공전 속도 (km/s)")
ax.set_title("은하 회전 곡선 비교")
ax.legend()
st.pyplot(fig)

# -----------------------------
# 5. 해설
# -----------------------------
st.header("📚 해설")
st.markdown("""
- 뉴턴 역학에 따르면 중심 질량 분포만을 고려했을 때 별의 속도는 반지름에 따라 **감소**해야 합니다.
- 그러나 실제 관측된 속도는 **일정하게 유지**됩니다.
- 이는 중심 외곽에 **관측되지 않는 질량(암흑물질)** 이 존재함을 시사합니다.
""")
