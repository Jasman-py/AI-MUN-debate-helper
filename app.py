import os
import streamlit as st


from DebateEngine import generate_openings, generate_rebuttals, generate_closing
from utils import export_transcript_to_text, simple_fallacy_guessing

st.set_page_config(page_title="ArguMind — AI Debate Partner", layout="wide")

st.markdown( """ <style> .main > .block-container{padding-top:1rem;} .title {color:#FFD84A; font-weight:700;} .subtitle {color:#FFFFFF; opacity:0.85;} .procol {background:#170a2b;
 padding:12px; border-radius:8px;} .concol {background:#1c0f2f; padding:12px; border-radius:8px;} </style> """, unsafe_allow_html=True )

st.markdown("<h1 class='title'>ArguMind</h1><div class='subtitle'>Debating made easy</div>", unsafe_allow_html=True)
st.markdown("---")

with st.container():
    topic=st.text_input("Enter debate topic", value='Should Ai be regulated?')
    col1, col2, col3 = st.columns([1,1,0.4])
    with col1:
        rounds = st.number_input("Max Rebuttal Rounds", min_value=1, max_value=5, value=2)
    with col2:
        temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.4)
    with col3:
        st.write("")
        if st.button("Start Debarte"):
            if not topic.strip():
                st.warning("Please enter a topic")
            else:
                st.session_state['topic'] = topic.strip()
                st.session_state['rounds'] = 0
                st.session_state['transcript'] = ''
                with st.spinner('Opening arguments generating'):
                    openings = generate_openings(st.session_state['topic'])
                st.session_state['openings'] = openings
                st.session_state['transcripts']+="=== OPENINGS ===\n" + openings + "\n\n"
                st.rerun()

if 'openings' in st.session_state:
    st.markdown("### Opening Arguments")
    cols = st.columns(2)
    # naive split: split at "Against" or "AGAINST" etc. We'll show raw blocks to keep fast.
    left, right = st.session_state['openings'].split("\n\n", 1) if "\n\n" in st.session_state['openings'] else (st.session_state['openings'], "")
    cols[0].markdown(f"<div class='procol'><h3>For</h3><pre style='color:#fff'>{left}</pre></div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div class='concol'><h3>Against</h3><pre style='color:#fff'>{right}</pre></div>", unsafe_allow_html=True)

    # Rebuttal control
    if st.button("Run Rebuttal Round"):
        # extract pro and con text simply by splitting with heuristics
        full = st.session_state['openings']
        # try to separate by common tokens
        if "Against" in full or "AGAINST" in full or "Con" in full:
            # try to find index of "Against" ignoring case
            import re
            m = re.search(r"(Against|AGAINST|Con|CON|Against:)", full)
            if m:
                mid = m.start()
                pro_text = full[:mid].strip()
                con_text = full[mid:].strip()
            else:
                pro_text, con_text = full, ""
        else:
            # fallback: put first half / second half
            half = len(full)//2
            pro_text, con_text = full[:half], full[half:]
        with st.spinner("Generating rebuttals..."):
            rebuttals = generate_rebuttals(st.session_state['topic'], pro_text, con_text)
        st.session_state.setdefault('rebuttals', [])
        st.session_state['round'] += 1
        st.session_state['rebuttals'].append(rebuttals)
        st.session_state['transcript'] += f"=== REBUTTAL ROUND {st.session_state['round']} ===\n{rebuttals}\n\n"
        st.rerun()


if 'rebuttals' in st.session_state:
    st.markdown("### Rebuttals")
    for i, r in enumerate(st.session_state['rebuttals'], start=1):
        st.markdown(f"**Round {i}**")
        st.text_area(f"Rebuttal {i}", value=r, height=180)


st.markdown("---")
colx, coly = st.columns([1,1])
with colx:
    if st.button("Export Transcript (.txt)"):
        path = export_transcript_to_text(st.session_state.get('topic',''), st.session_state.get('transcript',''))
        st.success(f"Transcript exported: {path}")
with coly:
    if st.button("Suggest Fallacies (quick)"):
        # run simple heuristic on transcript
        suspects = simple_fallacy_guessing(st.session_state.get('transcript','') or "")
        if suspects:
            st.warning("Possible fallacies detected: " + ", ".join(suspects))
        else:
            st.success("No obvious fallacy triggers found (heuristic).")