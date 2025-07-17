# doppler_wave_2d.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("🌊 2D 도플러 효과 시뮬레이터")

st.markdown("""
광원이 2D 공간 중앙에 고정되어 있고, 관측자가 특정 방향으로 이동하면  
그에 따라 도달하는 **파장의 길이(주기)**가 변하는 모습을 시각화합니다.
""")

# 설정
c = 300000  # 빛의 속도 km/s
f0 = 6e14   # 기본 주파수 (Hz)
λ0 = c / f0

# 관측자 속도 (슬라이더로 조절, 단위: km/s)
v_obs = st.slider("🔭 관측자의 속도 (양수: 광원 접근, 음수: 멀어짐)", -100000, 100000, 0, step=1000)

# 도플러 이동 주파수 (비상대론적 근사)
f_shift = f0 * (1 + v_obs / c)
λ_shift = c / f_shift

# 시각화용 파형 데이터 생성
x = np.linspace(0, 10, 1000)
wave_0 = np.sin(2 * np.pi * x / λ0 * 1e-6)
wave_shift = np.sin(2 * np.pi * x / λ_shift * 1e-6)

# 플롯
fig, ax = plt.subplots()
ax.plot(x, wave_0, label="정지 상태 파형 (λ₀)", lw=2)
ax.plot(x, wave_shift, label=f"관측된 파형 (λ'={λ_shift:.1f}nm)", lw=2, linestyle='--')
ax.set_xlabel("공간")
ax.set_ylabel("진폭")
ax.legend()
ax.set_title("파장 변화 시각화")
st.pyplot(fig)
