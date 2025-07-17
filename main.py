import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("🌞 Kepler Orbit Simulator (with Velocity Vector + Animation)")

planet_data = {
    "Mercury": {"a": 0.387, "e": 0.206},
    "Mars": {"a": 1.524, "e": 0.093},
    "Earth": {"a": 1.000, "e": 0.017},
    "Venus": {"a": 0.723, "e": 0.007},
}

planet = st.selectbox("🌍 Choose a planet", list(planet_data.keys()))
a = planet_data[planet]["a"]
e = planet_data[planet]["e"]

st.markdown(f"**Selected Planet: {planet}**  \nEccentricity: **{e:.3f}**, Semi-major axis: **{a:.3f} AU**")

# Constants
GMsun = 4 * np.pi**2  # AU^3 / yr^2

# Full orbit
theta_all = np.linspace(0, 2*np.pi, 500)
r_all = a * (1 - e**2) / (1 + e * np.cos(theta_all))
x_orbit = r_all * np.cos(theta_all)
y_orbit = r_all * np.sin(theta_all)

# Animation container
plot_area = st.empty()

# Animation loop
for deg in range(0, 360, 2):
    theta = np.radians(deg)
    r = a * (1 - e**2) / (1 + e * np.cos(theta))
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Velocity vector
    v = np.sqrt(GMsun * (2/r - 1/a))
    vx = -v * np.sin(theta)
    vy = v * np.cos(theta)

    # Draw frame
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x_orbit, y_orbit, 'gray', lw=1, label='Orbit Path')
    ax.plot(0, 0, 'yo', label='Sun')
    ax.plot(x, y, 'bo', label='Planet')
    ax.quiver(x, y, vx, vy, color='red', scale=8, label='Velocity Vector')

    ax.set_aspect('equal')
    ax.set_xlim(-1.6*a, 1.6*a)
    ax.set_ylim(-1.2*a, 1.2*a)
    ax.set_xlabel("x (AU)")
    ax.set_ylabel("y (AU)")
    ax.legend()
    ax.set_title(f"{planet} Orbit – θ = {deg}°")
    ax.grid(True)

    plot_area.pyplot(fig)
    time.sleep(0.05)
