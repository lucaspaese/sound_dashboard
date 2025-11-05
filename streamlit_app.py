mport streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Dynamic Soundboard", page_icon="🎛️")

st.title("🎛️ Dynamic Soundboard")

uploaded_files = st.file_uploader(
    "Upload one or more sound files (MP3/WAV):",
    type=["mp3", "wav"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("⬆️ Upload some sounds to start.")
else:
    # Convert uploaded sounds to base64
    sounds = {}
    for file in uploaded_files:
        b64 = base64.b64encode(file.read()).decode()
        sounds[file.name] = b64

    # Generate dynamic HTML
    html_buttons = ""
    js_listeners = ""
    for i, (name, b64) in enumerate(sounds.items()):
        audio_id = f"sound{i}"
        btn_id = f"btn{i}"
        html_buttons += f"""
            <audio id="{audio_id}" src="data:audio/mp3;base64,{b64}"></audio>
            <button id="{btn_id}" style="
                background-color:#4CAF50;
                border:none;
                color:white;
                padding:10px 20px;
                margin:5px;
                border-radius:8px;
                cursor:pointer;
            ">{name}</button>
        """
        js_listeners += f"""
            document.getElementById("{btn_id}").addEventListener("click", () => {{
                const s = document.getElementById("{audio_id}");
                s.currentTime = 0;
                s.play();
            }});
        """

    html_code = f"""
    <!DOCTYPE html>
    <html>
      <body style="font-family:sans-serif; text-align:center;">
        {html_buttons}
        <script>{js_listeners}</script>
      </body>
    </html>
    """

    components.html(html_code, height=200 + len(sounds) * 60)
