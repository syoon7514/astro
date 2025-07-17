# doppler_streamlit.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="빛의 도플러 이동 시뮬레이터", layout="centered")

st.title("🔭 빛의 도플러 이동 시뮬레이터")
st.markdown("""
빛의 도플러 이동은 **광원과 관측자 사이의 상대 속도**에 따라 관측되는 빛의 파장이 달라지는 현상입니다.
""")

# 슬라이더로 광원의 속도 설정 (단위: km/s)
v = st.slider("🌌 광원의 속도 (양수: 멀어짐 → 적색편이, 음수: 가까워짐 → 청색편이)", -290000, 290000, 0, step=1000)

# 도플러 공식 적용 (비상대론적 근사: v << c)
c = 3e5  # 빛의 속도 km/s
λ0 = 500  # 정지 상태 기준 파장 (nm), 예: 500nm 초록색

# 도플러 이동된 파장 계산
λ_shifted = λ0 * (1 + v/c)

# 색상 범위 (대략적 RGB 기준)
colors = {
    '자주': (380, 450),
    '파랑': (450, 495),
    '초록': (495, 570),
    '노랑': (570, 590),
    '주황': (590, 620),
    '빨강': (620, 750)
}

def get_color(wavelength):
    for name, (low, high) in colors.items():
        if low <= wavelength <= high:
            return name
    return "가시광선 영역 밖"

# 색상 텍스트 출력
st.markdown(f"""
- **정지 상태 파장**: {λ0:.1f} nm → 🌈 {get_color(λ0)}  
- **이동 후 파장**: {λ_shifted:.1f} nm → 🌈 {get_color(λ_shifted)}  
""")

# 그래프 출력
fig, ax = plt.subplots(figsize=(6, 1.5))
ax.axvline(λ0, color='black', label='정지 상태 스펙트럼', lw=2)
ax.axvline(λ_shifted, color='red' if v > 0 else 'blue', label='이동 후 스펙트럼', lw=2)
ax.set_xlim(350, 750)
ax.set_xlabel("파장 (nm)")
ax.set_yticks([])
ax.set_title("스펙트럼 선 이동 시각화")
ax.legend()
st.pyplot(fig)

# 부가 설명
with st.expander("📘 도플러 공식 설명"):
    st.latex(r"""\lambda' = \lambda_0 \left(1 + \frac{v}{c}\right)""")
    st.markdown("""
    - λ': 관측된 파장  
    - λ₀: 원래의 파장  
    - v: 광원과의 상대속도 (양수는 멀어짐, 음수는 가까워짐)  
    - c: 빛의 속도 (약 300,000 km/s)  
    """)
