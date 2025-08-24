import streamlit as st

# --- Must be first Streamlit command ---
st.set_page_config(
    page_title="QuantumGuard • BB84 QKD Simulator",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Imports ---
from quantumguard.components import header, sidebar_nav, footer
from quantumguard.simulator import run_simulation, sweep_eve
from quantumguard.visuals import plot_match_hist, plot_qber_curve, plot_bloch_preview
from quantumguard.utils import build_run_dataframe, download_buttons

# --- Header & Sidebar ---
header()
page, params, cmds = sidebar_nav()

# --- Main Router ---
if page == "Dashboard":
    st.info("Use **Simulator** to run BB84. Dashboard shows quick tips and KPIs once you have a run.")

elif page == "Simulator":
    res = run_simulation(params, cmds)
    if res:
        # --- KPI Row ---
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sifted", f"{len(res['sift_idx'])}", help="Positions where bases matched")
        c2.metric("Sampled", f"{len(res['sample_positions'])}")
        c3.metric("QBER", f"{res['qber']*100:.2f}%")
        c4.metric("Decision", res['decision'])

        st.markdown("---")
        left, right = st.columns(2)

        # --- Left column visuals ---
        with left:
            plot_match_hist(res['alice_bases'] == res['bob_bases'])
            plot_bloch_preview(res['alice_bases'], res['alice_bits'])

        # --- Right column visuals ---
        with right:
            if cmds.get('sweep'):
                pts = sweep_eve(params)
                st.session_state['qber_curve'] = pts

            if 'qber_curve' in st.session_state:
                plot_qber_curve(st.session_state['qber_curve'])
            else:
                st.info("Click **Parameter Sweep** in sidebar to generate QBER curve.")

        st.markdown("---")
        st.subheader("Export Results")
        df = build_run_dataframe(res)
        st.dataframe(df, use_container_width=True, height=320)
        download_buttons(df, res)

else:
    # --- Static Pages ---
    from quantumguard.components import section_theory, section_team, section_faq, section_contact
    if page == "Theory":
        section_theory()
    elif page == "Team":
        section_team()
    elif page == "FAQ":
        section_faq()
    elif page == "Contact":
        section_contact()

# --- Footer ---
footer()
