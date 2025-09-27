import streamlit as st

st.set_page_config(layout="wide")

# Check if the user is logged in
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to view your profile.")
else:
    st.title(f"Style Profile for {st.session_state.username}")
    
    # --- User Profile Sidebar ---
    st.sidebar.header("Your Style Profile")

    skin_tone = st.sidebar.selectbox(
        "Select your skin tone:",
        ("Warm", "Cool", "Neutral")
    )

    body_shape = st.sidebar.selectbox(
        "Select your body shape:",
        ("Rectangle", "Inverted Triangle", "Triangle", "Oval", "Athletic")
    )
    
    # You can save these to session_state as well
    st.session_state['skin_tone'] = skin_tone
    st.session_state['body_shape'] = body_shape

    st.sidebar.write("---")
    st.sidebar.write("Your profile is saved for this session.")
    
    st.write("Use the controls in the sidebar to set up your style profile. This information will be used for future recommendations.")