# kepler_streamlit_planets.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 태양계 행성 데이터 (이심률, 반장축 AU 기준)
planet_data = {
    "Mercury": {"a": 0.387, "e": 0.206},
    "Venus": {"a": 0.723, "e": 0.007},
    "Earth": {"a": 1.000, "e": 0.017},
    "Mars": {"a": 1.524, "e": 0.093},
    "Jupiter": {"a": 5.203, "e": 0.049},
    "Saturn": {"a": 9.537, "e": 0.056},
    "Uranus": {"a": 19.191, "e": 0.047},
    "Neptune": {"a": 30.07, "e": 0.009}
}

st.set_page_config(layout="wide")
st.title("🌞 케플러 궤도 시뮬레이터 (태양계 + 속도 벡터 포함)")

planet = st.selectbox("🌍 행성을 선택하세요", list(planet_data.keys()))
params = planet_data[planet]
a = params["a"]
e = params["e"]

st.markdown(f"**선택한 행성: {planet}**  \n이심률 **e = {e:.3f}**, 반장축 **a = {a:.3f} AU**")

# 태양 질량 (단위 맞추기 위해 상수화)
GMsun = 4 * np.pi**2  # AU³/yr²

# 궤도 방정식
theta = np.linspace(0, 2*np.pi, 1000)
r = a * (1 - e**2) / (1 + e * np.cos(theta))
x_orbit = r * np.cos(theta)
y_orbit = r * np.sin(theta)

# 프레임 선택 (행성 위치 θ)
frame = st.slider("🌐 공전 위치 조절 (0° ~ 360°)", 0, 360, 45, step=5)
theta_pos = np.radians(frame)
r_now = a * (1 - e**2) / (1 + e * np.cos(theta_pos))
x_now = r_now * np.cos(theta_pos)
y_now = r_now * np.sin(theta_pos)

# 속도 크기 (에너지 보존 법칙 기반)
v_now = np.sqrt(GMsun * (2/r_now - 1/a))  # AU/yr
vx = -v_now * np.sin(theta_pos)
vy = v_now * np.cos(theta_pos)

# 시각화
fig, ax = plt.subplots(figsize=(6,6))
ax.plot(x_orbit, y_orbit, 'gray', lw=1, label="궤도 경로")
ax.plot(0, 0, 'yo', markersize=10, label="태양")
ax.plot(x_now, y_now, 'bo', markersize=10, label=f"{planet}")

# 속도 벡터
ax.quiver(x_now, y_now, vx, vy, color='red', scale=10, label="속도 벡터")

# 세팅
ax.set_aspect('equal')
ax.set_xlabel("x (AU)")
ax.set_ylabel("y (AU)")
ax.set_title(f"{planet}의 궤도와 속도 벡터")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 수치 정보 출력
st.markdown(f"""
### 📊 현재 위치 정보
- 거리 r = **{r_now:.3f} AU**
- 속도 v = **{v_now:.3f} AU/yr**
- 방향 θ = **{frame}°**
""")
