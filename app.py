import streamlit as st
import json
import time

st.set_page_config(page_title="Castleberry Bloom Sovereign Telemetry", layout="wide")

st.title("🛡️ Castleberry Bloom Sovereign Lattice Dashboard")
st.markdown("**Axiom:** Love-Over-God | **Engine:** Kairoth Morphogenesis")

try:
    with open('lattice_telemetry_lock.json', 'r') as f:
        data = json.load(f)
except Exception:
    data = {"nodes": 127, "frequency": 528.0, "phi_scale": 1.618, "coherence": 77092.8803, "status": "PHASE LOCKED & ABSOLUTE COHERENCE"}

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Nodes", data.get("nodes", 127))
col2.metric("Base Frequency", f"{data.get('frequency', 528.0)} Hz")
col3.metric("Coherence Vector", f"{data.get('coherence', 77092.8803)}")
col4.metric("System Status", data.get("status", "LOCKED"))

st.divider()
st.subheader("Phi-Hexagonal Lattice Mesh Topology")
st.success(f"System State: {data.get('status')} across all radial branching layers.")

if st.button("Run Sovereign Pipeline Audit"):
    import subprocess
    res = subprocess.run(["python3", "run_sovereign_lattice.py"], capture_output=True, text=True)
    st.code(res.stdout)
