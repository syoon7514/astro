import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("🔬 후성유전 조절과 mRNA 유도 발현 시뮬레이터")

st.markdown("""
이 시뮬레이터는 **mRNA 백신 기술**과 **후성유전학적 조절**이 단백질 발현(RFP) 양에 어떤 영향을 미치는지 시각화합니다.

아래에서 실험 조건을 설정해 보세요:
""")

# ------------------------
# 🌟 실험 조건 입력
# ------------------------
col1, col2 = st.columns(2)

with col1:
    mRNA = st.checkbox("외부 mRNA 도입 (백신 모사)", value=False)
    inhibitor = st.checkbox("HDAC 억제제 처리 (히스톤 탈아세틸화 억제)", value=False)

with col2:
    inhibitor_strength = st.slider("HDAC 억제제 강도 (%)", 0, 100, 0 if not inhibitor else 50)

# ------------------------
# 🔬 시뮬레이션 로직
# ------------------------
baseline = 10
mRNA_effect = 50 if mRNA else 0
epigenetic_effect = 30 * (inhibitor_strength / 100) if inhibitor else 0
total_expression = baseline + mRNA_effect + epigenetic_effect

# ------------------------
# 📊 발현량 시각화
# ------------------------
st.subheader("📊 RFP 단백질 발현량 결과")
fig, ax = plt.subplots()
ax.bar(["발현량"], [total_expression], color="#FF6F61")
ax.set_ylim(0, 100)
ax.set_ylabel("상대 발현량")
ax.set_title("총 단백질 발현 (RFP)")
st.pyplot(fig)

# ------------------------
# 🧬 염색질 상태 이미지 설명
# ------------------------
st.subheader("🧬 생물학적 해설 및 시각화")

if inhibitor:
    st.markdown("**HDAC 억제제 처리로 히스톤 아세틸화가 증가하여, 염색질이 이완된 상태(Euchromatin)가 되어 전사가 촉진됩니다.**")
    image1 = Image.open("/mnt/data/euchromatin.png")
    st.image(image1, caption="히스톤 아세틸화 → Euchromatin")
else:
    st.markdown("**히스톤 탈아세틸화로 인해 염색질이 응축된 상태(Heterochromatin)가 되어 전사가 억제됩니다.**")
    image2 = Image.open("/mnt/data/heterochromatin.png")
    st.image(image2, caption="히스톤 탈아세틸화 → Heterochromatin")

if mRNA:
    st.markdown("**외부 mRNA 주입은 핵 단계를 거치지 않고 바로 번역되어 단백질을 생성합니다.**")
    image3 = Image.open("/mnt/data/mrna_translation.png")
    st.image(image3, caption="주입된 mRNA → 세포질에서 번역 → 단백질 생성")

# ------------------------
# 📘 해설 요약
# ------------------------
st.subheader("📘 종합 해설")

st.markdown(f"""
- 대조군의 기본 발현량은 **{baseline}**입니다.  
- mRNA 도입 시 **{mRNA_effect}**만큼 번역이 유도됩니다.  
- 후성유전학적 조절(히스톤 변형)은 **{epigenetic_effect:.1f}**만큼 전사를 촉진합니다.  
- 최종 RFP 발현량은 **{total_expression:.1f}**입니다.

➡️ 이 결과는 유전자 발현이 **DNA 염기서열 변화 없이도 조절 가능함**을 보여줍니다.
""")
