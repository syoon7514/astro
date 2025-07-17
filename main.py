# kepler_orbit_simulator.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

st.set_page_config(layout="wide")
st.title("🌞 Kepler Orbit Simulator with Velocity Vectors")

# 태양계 행성 데이터
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

planet = st.selectbox("🌍 Choose a planet", list(planet_data.keys()))
a = planet_data[planet]["a"]
e = planet_data[planet]["e"]

st.markdown(f"**Selected Planet: {planet}**  \nEccentricity: **{e:.3f}**, Semi-major axis: **{a:.3f} AU**")

# 상수 설정
GMsun = 4 * np.pi**2  # AU³/yr²

# 궤도 경로
theta_full = np.linspace(0, 2*np.pi, 1000)
r_full = a * (1 - e**2) / (1 + e * np.cos(theta_full))
x_orbit = r_full * np.cos(theta_full)
y_orbit = r_full * np.sin(theta_full)

# 플롯 설정
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.6*a, 1.6*a)
ax.set_ylim(-1.6*a, 1.6*a)
ax.set_aspect('equal')
ax.set_xlabel("x (AU)")
ax.set_ylabel("y (AU)")
ax.set_title(f"{planet}'s Elliptical Orbit and Velocity Vector")
ax.grid(True)
ax.plot(x_orbit, y_orbit, 'gray', lw=1, label='Orbit Path')
ax.plot(0, 0, 'yo', label='Sun')

planet_dot, = ax.plot([], [], 'bo', markersize=8, label='Planet')
velocity_vector = ax.quiver([], [], [], [], color='red', scale=5, label='Velocity Vector')
ax.legend()

# 초기화
def init():
    planet_dot.set_data([], [])
    velocity_vector.set_UVC(0, 0)
    return planet_dot, velocity_vector

# 업데이트
def update(frame):
    theta = 2 * np.pi * frame / 360
    r = a * (1 - e**2) / (1 + e * np.cos(theta))
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    v = np.sqrt(GMsun * (2/r - 1/a))
    vx = -v * np.sin(theta)
    vy = v * np.cos(theta)

    planet_dot.set_data(x, y)
    velocity_vector.set_offsets([x, y])
    velocity_vector.set_UVC(vx, vy)

    return planet_dot, velocity_vector

# 애니메이션 실행
ani = animation.FuncAnimation(fig, update, frames=360, init_func=init, blit=True, interval=50)

# 스트림릿 출력
st.pyplot(fig)
