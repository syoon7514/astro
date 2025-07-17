import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("🌌 Kepler Planetary Orbit and Velocity Simulator")

# Planetary data
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

e_scale = 5  # exaggeration factor for eccentricity

# Planet selector
st.subheader("🪐 Select a Planet")
cols = st.columns(len(planet_data))
selected_planet = None
for i, (name, _) in enumerate(planet_data.items()):
    if cols[i].button(name):
        selected_planet = name

if selected_planet:
    a = planet_data[selected_planet]["a"]
    e_real = planet_data[selected_planet]["e"]
    e = min(e_real * e_scale, 0.9)
    T = planet_data[selected_planet]["T"]

    st.markdown(f"""
    **Selected Planet**: {selected_planet}  
    Actual Eccentricity: {e_real:.3f} → Exaggerated: **{e:.3f}**  
    Semi-major Axis a = {a:.3f} AU, Orbital Period T = {T:.3f} years
    """)

    GMsun = 4 * np.pi**2
    total_steps = 180
    dt = T / total_steps

    theta_all = np.linspace(0, 2*np.pi, 500)
    r_all = a * (1 - e**2) / (1 + e * np.cos(theta_all))
    x_orbit = r_all * np.cos(theta_all)
    y_orbit = r_all * np.sin(theta_all)

    positions = []
    velocities = []
    times = []
    thetas = []
    rs = []

    for step in range(total_steps):
        t = step * dt
        theta = 2 * np.pi * (t / T)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        v = np.sqrt(GMsun * (2/r - 1/a))
        vx = -v * np.sin(theta)
        vy = v * np.cos(theta)

        times.append(t)
        velocities.append(v * 30)  # scaled for visibility
        positions.append((x, y))
        thetas.append(theta)
        rs.append(r)

    plot_area = st.empty()
    graph_area = st.empty()

    for i in range(total_steps):
        x, y = positions[i]
        vx = -np.sin(2 * np.pi * (times[i] / T)) * velocities[i]
        vy = np.cos(2 * np.pi * (times[i] / T)) * velocities[i]

        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.plot(x_orbit, y_orbit, 'gray', lw=1, label='Orbit')
        ax1.plot(0, 0, 'yo', label='Sun')
        ax1.plot(x, y, 'bo', label='Planet')
        ax1.quiver(x, y, vx, vy, color='red', scale=15, width=0.007, label='Velocity Vector')
        ax1.set_aspect('equal')
        ax1.set_xlim(-2*a, 2*a)
        ax1.set_ylim(-1.5*a, 1.5*a)
        ax1.set_xlabel("x (AU)")
        ax1.set_ylabel("y (AU)")
        ax1.set_title(f"{selected_planet} - Time: {times[i]:.2f} yr")
        ax1.legend()
        ax1.grid(True)

        fig2, ax2 = plt.subplots()
        ax2.plot(times[:i+1], velocities[:i+1], color='green')
        ax2.set_xlim(0, T)
        ax2.set_ylim(0, 60)
        ax2.set_xlabel("Time (yr)")
        ax2.set_ylabel("Orbital Speed - km/s (scaled)")
        ax2.set_title("Speed - Time Graph")
        ax2.grid(True)

        with plot_area:
            st.pyplot(fig1)
        with graph_area:
            st.pyplot(fig2)

        time.sleep(0.03)

    def sector_area(r1, r2, dtheta):
        return 0.5 * r1 * r2 * abs(dtheta)

    steps_20 = int(total_steps * 0.2)
    start_area = sum(
        sector_area(rs[i], rs[i+1], thetas[i+1] - thetas[i]) for i in range(steps_20-1)
    )
    end_area = sum(
        sector_area(rs[-i-2], rs[-i-1], thetas[-i-1] - thetas[-i-2]) for i in range(steps_20-1)
    )

    st.markdown("### 📐 Kepler's Second Law: Sector Area Comparison")
    st.markdown(f"""
    - **First 20% of Orbit Area**: {start_area:.5f} AU²  
    - **Last 20% of Orbit Area**: {end_area:.5f} AU²  
    👉 These nearly equal areas support the **equal area in equal time** law.
    """)
else:
    st.info("Please select a planet to start the simulation.")
