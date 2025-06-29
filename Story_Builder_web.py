import streamlit as st
import random
import json
from datetime import datetime
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Story Builder", layout="wide")

# Data structures
if "session_data" not in st.session_state:
    st.session_state.session_data = {
        "characters": [],
        "plots": [],
        "scenes": [],
        "story_progression": []
    }

# Dark mode toggle
st.sidebar.title("Settings")
dark_mode = st.sidebar.checkbox("Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
        body { background-color: #222; color: #ddd; }
        .stButton>button { background-color: #555; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Character Builder
st.sidebar.title("Character Creator")
with st.sidebar.form("character_form"):
    name = st.text_input("Name")
    role = st.text_input("Role")
    description = st.text_area("Description")
    avatar_file = st.file_uploader("Upload Avatar Image", type=["png","jpg","jpeg"])
    moodboard_urls = st.text_area("Moodboard Image URLs (comma-separated)")
    submitted = st.form_submit_button("Add Character")
    if submitted:
        char = {
            "name": name,
            "role": role,
            "description": description,
            "avatar": avatar_file.getvalue() if avatar_file else None,
            "moodboard": [url.strip() for url in moodboard_urls.split(",") if url.strip()]
        }
        st.session_state.session_data["characters"].append(char)
        st.success(f"Character '{name}' added.")

# Plot Generator
st.sidebar.title("Plot Generator")
genres = ["Fantasy", "Sci-Fi", "Romance", "Mystery", "Horror"]
genre = st.sidebar.selectbox("Genre", genres)
if st.sidebar.button("Generate 3 Plot Ideas"):
    prompts = {
        "Fantasy": ["A hidden kingdom rises.", "An ancient relic awakens.", "A hero is betrayed by their closest ally."],
        "Sci-Fi": ["AI rebellion triggers interstellar war.", "Time travel causes paradox.", "A rogue planet threatens Earth's orbit."],
        "Romance": ["Childhood friends reunite unexpectedly.", "An arranged marriage turns genuine.", "Rivals fall in love during a festival."],
        "Mystery": ["A detective investigates a cryptic message.", "A missing artifact resurfaces.", "A secret society manipulates local events."],
        "Horror": ["An abandoned house hides a terrible secret.", "A town plagued by nightmares.", "A curse claims victims at midnight."]
    }
    for _ in range(3):
        plot = random.choice(prompts[genre])
        st.session_state.session_data["plots"].append({"genre": genre, "prompt": plot})
    st.sidebar.success("3 plot ideas generated.")

# Scene Builder
st.title("Scene Builder")
with st.form("scene_form"):
    scene_title = st.text_input("Scene Title")
    mood = st.text_input("Mood")
    actions = st.text_area("Key Actions")
    involved_chars = st.multiselect("Involved Characters", [c["name"] for c in st.session_state.session_data["characters"]])
    save_scene = st.form_submit_button("Add Scene")
    if save_scene:
        scene = {
            "title": scene_title,
            "mood": mood,
            "actions": actions,
            "characters": involved_chars
        }
        st.session_state.session_data["scenes"].append(scene)
        st.session_state.session_data["story_progression"].append(scene_title)
        st.success(f"Scene '{scene_title}' added.")

# Story Progression Tree
st.title("Story Progression")
if st.session_state.session_data["story_progression"]:
    st.write(st.session_state.session_data["story_progression"])
else:
    st.write("No scenes added yet.")

# Save/Load Session
st.title("Session Management")
save_name = st.text_input("Session Filename (without extension)")
if st.button("Download Session JSON"):
    json_data = json.dumps(st.session_state.session_data, indent=2)
    st.download_button(label="Download Story JSON", file_name=f"{save_name or 'story_session'}.json", mime="application/json", data=json_data)

# Export as TXT or PDF
def export_session(format_type):
    if format_type == "TXT":
        text_data = json.dumps(st.session_state.session_data, indent=2)
        st.download_button("Download as TXT", text_data, file_name=f"{save_name or 'story_session'}.txt")
    elif format_type == "PDF":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for section, content in st.session_state.session_data.items():
            pdf.cell(200, 10, txt=f"{section}", ln=1, align='L')
            pdf.multi_cell(0, 10, txt=json.dumps(content, indent=2))
        pdf_bytes = BytesIO()
        pdf.output(pdf_bytes, 'F')
        st.download_button("Download as PDF", pdf_bytes.getvalue(), file_name=f"{save_name or 'story_session'}.pdf")

export_session("TXT")
export_session("PDF")

# View Characters and Plots
st.title("Story Overview")
if st.session_state.session_data["characters"]:
    st.subheader("Characters")
    for char in st.session_state.session_data["characters"]:
        st.write(f"**{char['name']} ({char['role']})**")
        st.write(char["description"])
        if char["avatar"]:
            st.image(char["avatar"], width=120)
        if char["moodboard"]:
            st.image(char["moodboard"], width=120)
else:
    st.write("No characters created yet.")

if st.session_state.session_data["plots"]:
    st.subheader("Plot Ideas")
    for plot in st.session_state.session_data["plots"]:
        st.write(f"**{plot['genre']}:** {plot['prompt']}")
else:
    st.write("No plots generated yet.")
