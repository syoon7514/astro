import streamlit as st
import numpy as np

st.set_page_config(layout="wide")
st.title("🌌 케플러 행성 궤도와 속도 변화 시뮬레이터 (부채꼴 면적 포함)")

planet_data = {
    "수성": {"a": 0.387, "e": 0.206, "T": 0.241},
    "금성": {"a": 0.723, "e": 0.007, "T": 0.615},
    "지구": {"a": 1.000, "e": 0.017, "T": 1.000},
    "화성": {"a": 1.524, "e": 0.093, "T": 1.881},
    "목성": {"a": 5.203, "e": 0.049, "T": 11.862},
    "토성": {"a": 9.537, "e": 0.056, "T": 29.457},
    "천왕성": {"a": 19.191, "e": 0.047, "T": 84.011},
    "해왕성": {"a": 30.07, "e": 0.009, "T": 164.8}
}

e_scale = 5

st.subheader("🪐 행성을 선택하세요")
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

    GMsun = 4 * np.pi**2
    total_steps = 180
    dt = T / total_steps

    positions = []
    thetas = []
    rs = []

    for step in range(total_steps):
        t = step * dt
        theta = 2 * np.pi * (t / T)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        positions.append((x, y))
        thetas.append(theta)
        rs.append(r)

    def sector_area(r1, r2, dtheta):
        return 0.5 * r1 * r2 * abs(dtheta)

    steps_20 = int(total_steps * 0.2)
    start_area_sector = sum(
        sector_area(rs[i], rs[i+1], thetas[i+1] - thetas[i]) for i in range(steps_20-1)
    )
    end_area_sector = sum(
        sector_area(rs[-i-2], rs[-i-1], thetas[-i-1] - thetas[-i-2]) for i in range(steps_20-1)
    )

    st.markdown(f"""
    ### 📐 케플러 제2법칙: 부채꼴 면적 계산  
    - 선택한 행성: **{selected_planet}**  
    - 실제 이심률: {e_real:.3f} → 과장된 이심률: **{e:.3f}**

    ---
    - **공전 초반 20% 부채꼴 면적**: {start_area_sector:.5f} AU²  
    - **공전 마지막 20% 부채꼴 면적**: {end_area_sector:.5f} AU²  
    👉 두 면적이 유사함을 통해 **면적 속도 일정성(케플러 제2법칙)**을 확인할 수 있습니다.
    """)
else:
    st.info("행성을 선택하면 시뮬레이션이 시작됩니다.")
