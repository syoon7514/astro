import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="은하 회전 곡선 시뮬레이터", layout="centered")
st.title("🌌 은하 회전 곡선 시뮬레이터")
st.markdown("""
이 시뮬레이터는 **21cm 수소선 관측값**을 바탕으로 **도플러 효과**를 적용하여 은하 내 별들의 공전 속도를 계산하고,  
이를 **뉴턴 역학 기반 속도**와 비교하여 **암흑물질의 존재**를 시각적으로 탐구합니다.
""")

# -----------------------------
# 1. 사용자 입력: 관측 데이터 입력
# -----------------------------
st.header("📥 반지름별 수소선 관측값 입력")

sample_data = {
    "반지름 (kpc)": [2, 4, 6, 8, 10, 12, 14, 16],
    "관측 파장 λ_obs (cm)": [21.0001, 21.0002, 21.0003, 21.0004, 21.0005, 21.0006, 21.0007, 21.0008],
    "속도 (km/s, optional)": [None] * 8
}
data = st.data_editor(sample_data, num_rows="dynamic", use_container_width=True)

# -----------------------------
# 2. 도플러 효과 계산
# -----------------------------
c = 3e5  # 빛의 속도 (km/s)
λ_0 = 21.0  # 수소선 기준 파장 (cm)

r_vals = []
v_obs = []

for index, row in data.iterrows():
    r = row["반지름 (kpc)"]
    λ = row["관측 파장 λ_obs (cm)"]
    v_direct = row["속도 (km/s, optional)"]

    if pd.notnull(r):
        r_vals.append(r)
        if pd.notnull(v_direct):
            v_obs.append(v_direct)
        else:
            if pd.notnull(λ):
                delta_lambda = λ - λ_0
                v = c * (delta_lambda / λ_0)
                v_obs.append(v)
            else:
                v_obs.append(0)  # 기본값

r_vals = np.array(r_vals)
v_obs = np.array(v_obs)

if len(r_vals) == 0:
    st.warning("입력된 반지름 값이 없습니다. 데이터를 입력해주세요.")
    st.stop()

# -----------------------------
# 3. 뉴턴 예측 속도 계산
# -----------------------------
st.header("⚖️ 뉴턴 역학 기반 예측 속도")

mass_distribution = st.selectbox("질량 분포 가정", ["균등 구형 분포 (M ∝ r³)", "중심 집중 질량 (M = const)"])

G = 4.3e-6  # (kpc km^2 / s^2 Msun) — 은하 단위 중력 상수

if mass_distribution == "균등 구형 분포 (M ∝ r³)":
    M_r = r_vals ** 3
else:
    M_r = np.full_like(r_vals, r_vals[0] ** 3)

v_newton = np.sqrt(G * M_r / r_vals)

# -----------------------------
# 4. 시각화
# -----------------------------
st.header("📈 회전 곡선 시각화")

fig, ax = plt.subplots()
ax.plot(r_vals, v_obs, 'o-', label="관측 속도 (21cm 수소선 기반)", linewidth=2)
ax.plot(r_vals, v_newton, '--', label="뉴턴 예측 속도", linewidth=2)
ax.set_xlabel("반지름 (kpc)")
ax.set_ylabel("공전 속도 (km/s)")
ax.set_title("은하 회전 곡선: 관측 vs 예측")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# -----------------------------
# 5. 결과 해설
# -----------------------------
st.header("🧠 결과 해설")
st.markdown("""
- 21cm 수소선의 **관측 파장 λ<sub>obs</sub>**를 이용해, 도플러 효과 공식을 적용하여 **은하 내 별의 속도**를 계산했습니다.
- **뉴턴 역학**에 따르면 속도는 중심에서 멀어질수록 **감소**해야 합니다. (질량이 대부분 중심에 있을 경우)
- 하지만 실제로는 속도가 일정하게 유지되는 패턴을 보이며, 이는 **관측되지 않는 질량(암흑물질)**이 분포하고 있음을 시사합니다.
- 이와 같은 회전 곡선은 은하 바깥까지 암흑물질이 퍼져 있음을 보여주는 **강력한 우주론적 증거**입니다.
""", unsafe_allow_html=True)

