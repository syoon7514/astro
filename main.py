import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("🔬 Epigenetic Regulation vs. mRNA Vaccine-driven Expression Simulator")

st.markdown("""
이 시뮬레이터는 **mRNA 백신 기술**과 **후성유전학적 조절**이 단백질 발현(RFP)에 어떤 영향을 미치는지 비교할 수 있게 해줍니다.

외부 mRNA의 주입 유무, 그리고 **히스톤 탈아세틸화 억제제(HDAC inhibitor)**의 적용 및 강도를 조절하여 다양한 분자적 조건에서의 유전자 발현 결과를 시각화할 수 있습니다.
""")

# ------------------------
# 🌟 Experiment Parameters
# ------------------------
col1, col2 = st.columns(2)

with col1:
    mRNA = st.checkbox("Inject external mRNA (vaccine mimic)", value=False)
    inhibitor = st.checkbox("Apply HDAC inhibitor (blocks histone deacetylation)", value=False)

with col2:
    inhibitor_strength = st.slider("HDAC Inhibitor Intensity (%)", 0, 100, 0 if not inhibitor else 50)

# ------------------------
# 🔬 Simulation Logic
# ------------------------
baseline = 10  # baseline expression
mRNA_effect = 50 if mRNA else 0  # protein expression from direct mRNA translation
epigenetic_effect = 30 * (inhibitor_strength / 100) if inhibitor else 0  # transcription enhancement from euchromatin state

total_expression = baseline + mRNA_effect + epigenetic_effect

# ------------------------
# 📊 Expression Bar Graph
# ------------------------
st.subheader("📊 RFP Protein Expression Result")
fig, ax = plt.subplots(figsize=(4, 2))
ax.bar(["RFP Expression"], [total_expression], color="#FF6F61")
ax.set_ylim(0, 100)
ax.set_xlabel("Condition")
ax.set_ylabel("Expression Level")
ax.set_title("Total RFP Protein Expression")
st.pyplot(fig)

# ------------------------
# 🧬 Mechanism and Visuals
# ------------------------
st.subheader("🧬 Molecular Mechanism and Visual Explanation")

if inhibitor:
    st.markdown("**HDAC 억제제는 히스톤 아세틸화를 증가시켜 염색질을 이완시켜 전사를 촉진합니다.**")
    image1 = Image.open("/mnt/data/euchromatin.png")
    st.image(image1, caption="Histone acetylation → Euchromatin")
else:
    st.markdown("**억제제가 없을 경우 히스톤 탈아세틸화로 인해 염색질이 응축되어 전사가 억제됩니다.**")
    image2 = Image.open("/mnt/data/heterochromatin.png")
    st.image(image2, caption="Histone deacetylation → Heterochromatin")

if mRNA:
    st.markdown("**주입된 mRNA는 핵을 거치지 않고 세포질에서 직접 번역되어 RFP 단백질을 생성합니다.**")
    image3 = Image.open("/mnt/data/mrna_translation.png")
    st.image(image3, caption="Injected mRNA → Cytoplasmic translation → Protein synthesis")

# ------------------------
# 📘 Summary Explanation
# ------------------------
st.subheader("📘 Summary Explanation")

st.markdown(f"""
- Baseline expression: **{baseline}**  
- Additional expression from injected mRNA: **{mRNA_effect}**  
- Transcription enhancement via histone acetylation: **{epigenetic_effect:.1f}**  
- 👉 Final RFP expression level: **{total_expression:.1f}**

이 시뮬레이션은 DNA 염기서열을 변화시키지 않고도 유전자 발현을 조절할 수 있는 두 가지 메커니즘을 시각적으로 보여줍니다.

mRNA는 번역을 통해 직접 단백질을 발현시키고, 후성유전학은 전사 가능성을 조절함으로써 유전자 발현에 영향을 줍니다. 이 두 방식은 생명공학 및 의학적 응용에서 중요한 유전자 조절의 층위를 보여줍니다.
""")
