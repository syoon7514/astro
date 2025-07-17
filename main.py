# kepler_animated_planets.py
# 실행: streamlit run kepler_animated_planets.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("🌞 Kepler Orbit Simulator – Planet Selector + Scaled Eccentricity + Velocity Graph")

# 실제 태양계 행성 데이터 (반장축 a [AU], 이심률 e)
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

# 이심률 과장 배율
e_scale = 5  # 실제 이심률에 곱해서 시각적 차이 강조

# 행성 선택 UI
st.subheader("🌍 Select a Planet")
cols = st.columns(len(planet_data))
selected_planet = None
for i, (name, _) in enumerate(planet_data.items()):
    if cols[i].button(name):
        selected_planet = name

# 시뮬레이션 실행
if selected_planet:
    a = planet_data[selected_planet]["a"]
    e_real = planet_data[selected_planet]["e"]
    e = min(e_real * e_scale, 0.9)  # 과장된 이심률

    st.markdown(f"""
    **Selected Planet**: {selected_planet}  
    Real eccentricity: {e_real:.3f} → Scaled eccentricity: **{e:.3f}**  
    Semi-major axis **a = {a:.3f} AU**
    """)

    GMsun = 4 * np.pi**2  # AU^3 / yr^2

    theta_all = np.linspace(0, 2*np.pi, 500)
    r_all = a * (1 - e**2) / (1 + e * np.cos(theta_all))
    x_orbit = r_all * np.cos(theta_all)
    y_orbit = r_all * np.sin(theta_all)

    plot_area = st.empty()
    graph_area = st.empty()
    velocities = []
    angles_deg = []

    for deg in range(0, 360, 2):
        theta = np.radians(deg)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        v = np.sqrt(GMsun * (2/r - 1/a))
        vx = -v * np.sin(theta)
        vy = v * np.cos(theta)

        velocities.append(v * 30)
        angles_deg.append(deg)

        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.plot(x_orbit, y_orbit, 'gray', lw=1, label='Orbit Path')
        ax1.plot(0, 0, 'yo', label='Sun')
        ax1.plot(x, y, 'bo', label='Planet')
        ax1.quiver(x, y, vx, vy, color='red', scale=8, label='Velocity Vector')
        ax1.set_aspect('equal')
        ax1.set_xlim(-2*a, 2*a)
        ax1.set_ylim(-1.5*a, 1.5*a)
        ax1.set_xlabel("x (AU)")
        ax1.set_ylabel("y (AU)")
        ax1.set_title(f"{selected_planet} – θ = {deg}°")
        ax1.legend()
        ax1.grid(True)

        fig2, ax2 = plt.subplots()
        ax2.plot(angles_deg, velocities, color='green')
        ax2.set_xlabel("Orbital Angle θ (°)")
        ax2.set_ylabel("Orbital Speed (scaled km/s)")
        ax2.set_title("Orbital Speed vs Angle")
        ax2.grid(True)

        with plot_area:
            st.pyplot(fig1)
        with graph_area:
            st.pyplot(fig2)

        time.sleep(0.05)
else:
    st.info("Click a planet above to begin the simulation.")
