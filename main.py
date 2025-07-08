import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Streamlit UI 구성
# -----------------------------
st.title("🌌 은하 회전 곡선 시뮬레이터")
st.markdown("""
이 시뮬레이터는 **은하의 회전 곡선**을 21cm 수소선 관측 데이터를 바탕으로 시각화하여, **암흑물질의 존재 가능성**을 탐구합니다.
""")

# -----------------------------
# 1. 사용자 입력: 반지름별 관측 파장 or 속도
# -----------------------------
st.header("📥 반지름별 수소선 관측값 입력")

with st.expander("입력 설명"):
    st.markdown("""
    - 반지름: 은하 중심에서의 거리 (kpc)
    - 관측 파장 λ<sub>obs</sub>: 관측된 21cm 수소선 파장 (단위: cm)  
      → 도플러 효과로부터 속도 계산됨  
    - 또는 공전 속도 (km/s)를 직접 입력할 수도 있음
    """)

# 기본 입력 테이블
st.markdown("#### 반지름, 관측 파장(옵션), 또는 속도 직접 입력")
sample_data = {
    "반지름 (kpc)": [2, 4, 6, 8, 10, 12, 14, 16],
    "관측 파장 λ_obs (cm)": [21.03, 21.05, 21.06, 21.08, 21.09, 21.10, 21.11, 21.12],
    "속도 (km/s, optional)": [None] * 8
}
data = st.data_editor(sample_data, num_rows="dynamic")

# 도플러 효과 계산
c = 3e5  # 빛의 속도 km/s
λ_0 = 21.0  # 수소선 기준 파장 (cm)

r_vals = []
v_obs = []

for row in data:
    r = row["반지름 (kpc)"]
    λ = row["관측 파장 λ_obs (cm)"]
    v_direct = row["속도 (km/s, optional)"]

    if r is not None:
        r_vals.append(r)
        if v_direct is not None:
            v_obs.append(v_direct)
        else:
            # 도플러 공식: v = c * (Δλ / λ₀)
            delta_lambda = λ - λ_0
            v = c * (delta_lambda / λ_0)
            v_obs.append(v)

r_vals = np.array(r_vals)
v_obs = np.array(v_obs)

# -----------------------------
# 2. 뉴턴 예측 속도 계산
# -----------------------------
st.header("⚖️ 뉴턴 역학 기반 예측 속도")

mass_distribution = st.selectbox("중심 질량 분포 가정", ["균등 구형 질량 분포 (M ∝ r³)", "중심 집중 질량 (M = const)"])

G = 4.3e-6  # 중력 상수 (kpc * (km/s)^2 / Msun)

if mass_distribution == "균등 구형 질량 분포 (M ∝ r³)":
    M_r = r_vals ** 3
else:
    M_r = np.full_like(r_vals, r_vals[0] ** 3)

v_newton = np.sqrt(G * M_r / r_vals)

# -----------------------------
# 3. 시각화
# -----------------------------
st.header("📈 회전 곡선 시각화")

fig, ax = plt.subplots()
ax.plot(r_vals, v_obs, 'o-', label="관측 속도 (21cm 수소선 기반)")
ax.plot(r_vals, v_newton, '--', label="뉴턴 역학 예측 속도")
ax.set_xlabel("반지름 (kpc)")
ax.set_ylabel("공전 속도 (km/s)")
ax.set_title("은하 회전 곡선: 관측 vs 예측")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# -----------------------------
# 4. 해설
# -----------------------------
st.header("🧠 결과 해석")
st.markdown(f"""
- **21cm 수소선 관측값**으로부터 도플러 효과를 이용해 속도를 계산했습니다.
- **뉴턴 역학 예측**에 따르면 속도는 반지름에 따라 **감소**해야 합니다.
- 하지만 실제 관측 결과는 속도가 일정하게 유지되어, 은하 외곽에도 질량이 존재함을 나타냅니다.
- 이 질량은 우리가 관측할 수 없는 물질로, **암흑물질(Dark Matter)**의 존재를 강하게 시사합니다.
""")

