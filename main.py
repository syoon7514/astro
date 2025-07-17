import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("🌞 Kepler Orbit Simulator – Per-Planet Fixed Time Scale + Velocity Graph")

# 태양계 행성 데이터
planet_data = {
    "Mercury": {"a": 0.387, "e": 0.206, "T": 0.241},
    "Venus": {"a": 0.723, "e": 0.007, "T": 0.615},
    "Earth": {"a": 1.000, "e": 0.017, "T": 1.000},
    "Mars": {"a": 1.524, "e": 0.093, "T": 1.881},
    "Jupiter": {"a": 5.203, "e": 0.049, "T": 11.862},
    "Saturn": {"a": 9.537, "e": 0.056, "T": 29.457},
    "Uranus": {"a": 19.191, "e": 0.047, "T": 84.011},
    "Neptune": {"a": 30.07, "e": 0.009, "T": 164.8}
}

e_scale = 5

# 행성 선택 UI
st.subheader("🌍 Select a Planet")
cols = st.columns(len(planet_data))
selected_planet = None
for i, (name, _) in enumerate(planet_data.items()):
    if cols[i].button(name):
        selected_planet = name

# 시뮬레이터 실행
if selected_planet:
    a = planet_data[selected_planet]["a"]
    e_real = planet_data[selected_planet]["e"]
    e = min(e_real * e_scale, 0.9)
    T = planet_data[selected_planet]["T"]

    st.markdown(f"""
    **Selected Planet**: {selected_planet}  
    Real eccentricity: {e_real:.3f} → Scaled eccentricity: **{e:.3f}**  
    Semi-major axis: **a = {a:.3f} AU**, Orbital Period: **T = {T:.3f} yr**
    """)

    GMsun = 4 * np.pi**2
    theta_all = np.linspace(0, 2*np.pi, 500)
    r_all = a * (1 - e**2) / (1 + e * np.cos(theta_all))
    x_orbit = r_all * np.cos(theta_all)
    y_orbit = r_all * np.sin(theta_all)

    plot_area = st.empty()
    graph_area = st.empty()
    velocities = []
    times = []

    total_steps = 180
    dt = T / total_steps

    for step in range(total_steps):
        t = step * dt
        theta = 2 * np.pi * (t / T)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        v = np.sqrt(GMsun * (2/r - 1/a))
        vx = -v * np.sin(theta)
        vy = v * np.cos(theta)

        velocities.append(v * 30)
        times.append(t)

        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.plot(x_orbit, y_orbit, 'gray', lw=1, label='Orbit Path')
        ax1.plot(0, 0, 'yo', label='Sun')
        ax1.plot(x, y, 'bo', label='Planet')
        ax1.quiver(x, y, vx, vy, color='red', scale=15, width=0.007, label='Velocity Vector')
        ax1.set_aspect('equal')
        ax1.set_xlim(-2*a, 2*a)
        ax1.set_ylim(-1.5*a, 1.5*a)
        ax1.set_xlabel("x (AU)")
        ax1.set_ylabel("y (AU)")
        ax1.set_title(f"{selected_planet} – Time = {t:.2f} yr")
        ax1.legend()
        ax1.grid(True)

        fig2, ax2 = plt.subplots()
        ax2.plot(times, velocities, color='green')
        ax2.set_xlim(0, T)
        ax2.set_ylim(0, 60)
        ax2.set_xlabel("Time (years)")
        ax2.set_ylabel("Orbital Speed (scaled km/s)")
        ax2.set_title("Orbital Speed vs Time (Fixed Scale per Planet)")
        ax2.grid(True)

        with plot_area:
            st.pyplot(fig1)
        with graph_area:
            st.pyplot(fig2)

        time.sleep(0.05)
else:
    st.info("Click a planet above to begin the simulation.")
