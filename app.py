import os
import streamlit as st

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
                    pass

