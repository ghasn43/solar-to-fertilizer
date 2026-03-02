"""
Page 5: Quantum-Ready
"""
import streamlit as st
import pandas as pd
from core.quantum_stub import get_scorer, QUANTUM_CANDIDATES
from core.constants import COMPANY_NAME, COMPANY_LOCATION, IP_NOTICE

st.set_page_config(page_title="5. Quantum-Ready | S2F-DT", layout="wide")

st.markdown(f"<div style='color:#003366'><h1>⚛️ Quantum-Ready Catalyst Scoring</h1></div>", unsafe_allow_html=True)

st.markdown("""
Evaluate catalyst candidates using a **surrogate quantum model** (mock implementation).  
This module is **designed to be swapped** with real IBM Quantum or other quantum chemistry engines.
""")

st.markdown("---")

# What is Quantum Catalyst Scoring
st.markdown("### 🔬 What is Quantum Catalyst Scoring?")

st.markdown("""
Quantum chemistry can predict catalyst properties (energy barriers, reaction rates, selectivity) 
with **ab initio** calculations. Traditional approaches (DFT) take hours to days per candidate; 
**quantum computers** could accelerate this 100–1000×.

#### The Vision
1. **Feed** candidate catalyst structure (SMILES / 3D coordinates)
2. **Quantum Algorithm** computes energy barriers & reaction dynamics
3. **Score** = lower energy barrier = better catalyst
4. **Feedback** → Optimize structure → Iterate

#### This Implementation
Our **quantum_stub.py** is a **surrogate model** (mock quantum):
- Seeded RNG for reproducibility
- Rapid evaluation (~10 ms per candidate)
- Ready to be replaced with IBM Qiskit, AWS Braket, etc.

**Current Status**: 🔴 Surrogate / Placeholder  
**Next Phase**: 🟡 Connect to IBM Quantum Experience (requires credentials + queue time)  
**Future**: 🟢 Full production quantum-chemistry pipeline
""")

st.markdown("---")

# Catalyst Ranking
st.markdown("### 🏅 Catalyst Rankings (Quantum-Scored)")

scorer = get_scorer()
ranked_catalysts = scorer.rank_candidates()

# Display as table
catalyst_data = []
for i, cat in enumerate(ranked_catalysts, 1):
    catalyst_data.append({
        "Rank": i,
        "Catalyst Name": cat["name"],
        "Quantum Score": f"{cat['quantum_score']:.1f}",
        "Energy Barrier (kcal/mol)": f"{cat['energy_barrier_kcal_mol']:.2f}",
        "Confidence": f"{cat['confidence']:.0%}",
        "Type": cat["calculation_type"],
    })

catalyst_df = pd.DataFrame(catalyst_data)
st.dataframe(catalyst_df, use_container_width=True)

st.markdown("---")

# Detailed Analysis of Top 3
st.markdown("### 💡 Top 3 Catalysts — Detailed Analysis")

top_3 = ranked_catalysts[:3]

col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    cat = top_3[0]
    st.markdown(f"""
#### 🥇 Rank 1: {cat['name']}
- **Quantum Score**: {cat['quantum_score']:.1f}/100
- **Energy Barrier**: {cat['energy_barrier_kcal_mol']:.2f} kcal/mol
- **Confidence**: {cat['confidence']:.0%}
- **Notes**: {cat['notes']}

**Implication**: Lower energy barrier → faster reaction → higher efficiency
    """)

with col_t2:
    cat = top_3[1]
    st.markdown(f"""
#### 🥈 Rank 2: {cat['name']}
- **Quantum Score**: {cat['quantum_score']:.1f}/100
- **Energy Barrier**: {cat['energy_barrier_kcal_mol']:.2f} kcal/mol
- **Confidence**: {cat['confidence']:.0%}
- **Notes**: {cat['notes']}

**Implication**: Trade-off between performance and maturity
    """)

with col_t3:
    cat = top_3[2]
    st.markdown(f"""
#### 🥉 Rank 3: {cat['name']}
- **Quantum Score**: {cat['quantum_score']:.1f}/100
- **Energy Barrier**: {cat['energy_barrier_kcal_mol']:.2f} kcal/mol
- **Confidence**: {cat['confidence']:.0%}
- **Notes**: {cat['notes']}

**Implication**: Emerging candidate; higher risk, higher potential reward
    """)

st.markdown("---")

# Integration Example
st.markdown("### 🔌 How to Integrate with Real Quantum")

with st.expander("📖 Integration Code Example"):
    st.markdown("""
```python
# Future: Replace quantum_stub with IBM Quantum

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibmq import IBMQ

def quantum_chemistry_solver(catalyst_smiles: str):
    '''
    Run quantum circuit on IBM Quantum Experience to compute
    energy barriers for catalyst candidate.
    '''
    # Load IBMQ provider (requires credentials)
    IBMQ.load_account()
    provider = IBMQ.get_provider()
    backend = provider.get_backend('ibm_qx5')
    
    # Construct quantum circuit for molecular simulation
    # (Variational Quantum Eigensolver, VQE, or similar)
    qc = build_vqe_circuit(catalyst_smiles)
    
    # Submit to quantum device
    job = backend.run(qc, shots=1024)
    result = job.result()
    
    # Extract energy eigenvalue
    energy_barrier = extract_energy(result)
    
    return {"score": energy_barrier, "confidence": 0.95}

# Current: Use surrogate instead
from core.quantum_stub import get_scorer
scorer = get_scorer()
score = scorer.score_catalyst({"name": "Ruthenium-Carbon", ...})
```
    """)

st.markdown("---")

# Custom Catalyst Scoring
st.markdown("### 🧪 Score Your Own Catalyst")

with st.expander("Score a Custom Catalyst Candidate"):
    col_input_a, col_input_b = st.columns([2, 1])
    
    with col_input_a:
        custom_catalyst_name = st.text_input(
            "Catalyst Name",
            placeholder="e.g., 'Graphene-Supported Nickel'",
            help="Name of your catalyst candidate"
        )
        custom_catalyst_notes = st.text_area(
            "Notes",
            placeholder="e.g., 'Experimental, high surface area, toxic precursor'",
            height=3,
            help="Description of catalyst properties"
        )
    
    with col_input_b:
        if st.button("🔬 Score Catalyst", use_container_width=True):
            if custom_catalyst_name:
                custom_cat = {
                    "name": custom_catalyst_name,
                    "notes": custom_catalyst_notes
                }
                score_result = scorer.score_catalyst(custom_cat)
                
                st.markdown(f"""
**Quantum Score Result:**
- **Name**: {score_result['name']}
- **Quantum Score**: {score_result['quantum_score']:.1f}/100
- **Energy Barrier**: {score_result['energy_barrier_kcal_mol']:.2f} kcal/mol
- **Confidence**: {score_result['confidence']:.0%}
- **Calculation Type**: {score_result['calculation_type']}

*Note: This is a **mock quantum score**. In production, connect to IBM Quantum 
Experience or other quantum chemistry engines.*
                """)
            else:
                st.warning("Please enter a catalyst name.")

st.markdown("---")

# Roadmap
st.markdown("### 🗺️ Quantum Integration Roadmap")

col_roadmap = st.columns(4)

with col_roadmap[0]:
    st.markdown("""
#### Phase 1️⃣ (Current)
**Surrogate Model**
- ✅ Fast evaluation (~10ms)
- ✅ Seeded reproducibility
- ❌ No real quantum
- 🎯 Placeholder
    """)

with col_roadmap[1]:
    st.markdown("""
#### Phase 2️⃣ (Next)
**IBM Quantum (Easy)**
- ⏳ IBM Qiskit integration
- ⏳ VQE for energy barriers
- ⏳ Requires API key
- ⏳ ~5-10 min per evaluation
    """)

with col_roadmap[2]:
    st.markdown("""
#### Phase 3️⃣ (Future)
**Hybrid Classical-Quantum**
- ⏳ Parametrized VQE
- ⏳ Classical optimizer
- ⏳ Feedback loop
- ⏳ ~1-5 day full search
    """)

with col_roadmap[3]:
    st.markdown("""
#### Phase 4️⃣ (Far Future)
**Fault-Tolerant Quantum**
- ⏳ Full quantum simulation
- ⏳ >1000 qubits
- ⏳ Error corrections
- ⏳ Real ab initio performance
    """)

st.markdown("---")

# Key Insights
st.markdown("### 💎 Key Insights")

st.markdown("""
1. **Current Bottleneck**: Finding the "magic" catalyst structure takes months/years of testing.
2. **Quantum Promise**: Could reduce this to weeks/days via hardware-accelerated quantum algorithms.
3. **This App**: Shows how S2F-DT is **architecture-ready** for quantum integration.
4. **Cost Impact**: Better catalyst → lower synthesis energy → lower OpEx → competitive pricing.
5. **Competitive Edge**: First movers with quantum-optimized catalysts will dominate green ammonia market.

---

### 🚀 Next Steps
- Monitor quantum hardware announcements (IBM Quantum, Google Willow, etc.)
- Engage quantum chemistry experts for catalyst design
- Plan integration path (phase 1 → 2 → 3 → 4)
- Explore partnerships with quantum cloud providers
""")

st.markdown("---")

# Footer
st.markdown(f"""
<div style='text-align: center; font-size: 0.75rem; color: #666; border-top: 1px solid #ddd; padding-top: 1rem; margin-top: 2rem;'>
<p><strong style='color: #003366'>{COMPANY_NAME}</strong> | {COMPANY_LOCATION}</p>
<p>{IP_NOTICE}</p>
</div>
""", unsafe_allow_html=True)
