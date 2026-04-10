import streamlit as st
import requests
import pandas as pd
from streamlit_lottie import st_lottie

import random

def glass_box(content):
    return f"""
    <div style="
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    ">
    {content}
    </div>
    """
st.set_page_config(page_title="AI Journal", layout="wide")

# -------------------------------
# BACKGROUND IMAGES
# -------------------------------
bg_images = [
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
    "https://images.unsplash.com/photo-1493244040629-496f6d136cc3",
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    "https://images.unsplash.com/photo-1470770841072-f978cf4d019e",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba",
    "https://images.unsplash.com/photo-1493558103817-58b2924bce98",
    "https://images.unsplash.com/photo-1502082553048-f009c37129b9"
]

bg = random.choice(bg_images)

# -------------------------------
# APPLY BACKGROUND
# -------------------------------
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(20,20,30,0.65), rgba(20,20,30,0.65)),
    url("{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}}
</style>
""", unsafe_allow_html=True)
# -------------------------------
#  HEADER
# -------------------------------
st.markdown("""
<h1 style='text-align:center; font-size:42px; font-weight:600;'>
 AI Journal Assistant
</h1>
""", unsafe_allow_html=True)
st.markdown("""
<style>
h1 {
    text-shadow: 0 0 10px rgba(255,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🌿QUOTES (STABLE)
# -------------------------------

def generate_quote(mood="calm"):
    try:
        res = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": f"Give one short calming journaling quote for someone feeling {mood}. Keep it under 15 words.",
                "stream": False
            }
        )
        return res.json().get("response", "").strip()
    except:
        return "🌿 Take a deep breath. You’re doing okay."
quote = generate_quote("calm")
st.markdown(glass_box(f" 🌿{quote}"), unsafe_allow_html=True)

# 🎵 MUSIC OPTIONS
yt_suggestions = {
    "None": None,
    "Om Chanting": "https://www.youtube.com/watch?v=8sYK7lm3UKg&list=RD8sYK7lm3UKg&start_radio=1",
    "Deep Meditation": "https://www.youtube.com/watch?v=inpok4MKVLM",
    "Relaxing Flute": "https://www.youtube.com/watch?v=1ZYbU82GVz4"
}

yt_choice = st.sidebar.selectbox("🎧 Quick Play (YouTube)", list(yt_suggestions.keys()))

if yt_choice != "None":
    st.markdown("🎵 Now Playing: *" + yt_choice + "*")
    st.video(yt_suggestions[yt_choice])


# -------------------------------
#  CUSTOM YOUTUBE INPUT (ADDED)
# -------------------------------
yt_url = st.sidebar.text_input("🔗 Paste YouTube meditation/music link")

if yt_url:
    if "youtube.com" in yt_url or "youtu.be" in yt_url:
        st.markdown("🎵 Now Playing from YouTube")
        st.video(yt_url)
    else:
        st.warning("Please enter a valid YouTube link")
# -------------------------------
# BEAUTIFUL CALENDAR
# -------------------------------
import calendar
from datetime import datetime
import streamlit as st

# -------------------------------
# 📅 TOGGLE STATE
# -------------------------------
if "show_calendar" not in st.session_state:
    st.session_state.show_calendar = False

if st.sidebar.button("📅 View Calendar", key="calendar_toggle_btn"):
    st.session_state.show_calendar = not st.session_state.show_calendar


# -------------------------------
# 📅 SHOW CALENDAR
# -------------------------------
if st.session_state.show_calendar:

    now = datetime.now()
    month_days = calendar.monthcalendar(now.year, now.month)

    cal_html = f"<h3 style='text-align:center;'>📅 {now.strftime('%B %Y')}</h3>"
    cal_html += "<table style='width:100%; text-align:center;'>"

    days = ["Mo","Tu","We","Th","Fr","Sa","Su"]
    cal_html += "<tr>" + "".join([f"<th>{d}</th>" for d in days]) + "</tr>"

    for week in month_days:
        cal_html += "<tr>"
        for day in week:
            if day == 0:
                cal_html += "<td></td>"
            else:
                highlight = "background:#cdb4db; border-radius:6px;" if day == now.day else ""
                cal_html += f"<td style='{highlight}'>{day}</td>"
        cal_html += "</tr>"

    cal_html += "</table>"

    st.markdown(glass_box(cal_html), unsafe_allow_html=True)


# 🌸 Soft Feminine Theme CSS
st.markdown("""
<style>

/* User message */
.chat-user {
    background: rgba(255, 255, 255, 0.8);
    color: #2d2d2d;  /* dark text */
    font-weight: 500;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}

/* AI message */
.chat-ai {
    background: rgba(255, 255, 255, 0.85);
    color: #1f1f1f;  /* darker for clarity */
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: left;
}

/* Improve expander text */
details {
    color: #111 !important;
}

/* Fix markdown text inside boxes */
.chat-user *, .chat-ai * {
    color: inherit !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Header */
.header {
    text-align: center;
    font-size: 36px;
    font-weight: 600;
    color: #5a4e7c;
    margin-bottom: 10px;
}

/* Quote Box */
.quote-box {
    background: rgba(255,255,255,0.7);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    font-size: 18px;
    font-style: italic;
    color: #6d597a;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}


/* Button */
.stButton button {
    background: #cdb4db;
    color: black;
    border-radius: 10px;
    border: none;
    padding: 8px 16px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
input {
    background-color: rgba(255,255,255,0.9) !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)
# 🌿 Sidebar
st.sidebar.markdown("""
## 🌿 Your Space
- Write freely  
- Reflect deeply  
- Grow gently  
""")

#---------------------------------------------------------------
use_memory = st.sidebar.checkbox("🧠 Use Memory", value=True)
page = st.sidebar.radio("Navigate", ["Chat", "Insights", "History","Memory"])


# ---------------- CHAT ----------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if page == "Chat":
    st.subheader("📝 Write your thoughts")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("How was your day?", value=st.session_state.input_text)

    if st.button("Send"):
        if user_input.strip():
            with st.spinner("Thinking..."):

                try:
                    res = requests.post(
                        "http://localhost:8000/chat",
                        json={
                            "user_id": "1",
                            "message": user_input,
                            "use_memory": use_memory
                        }
                    )

                    if res.status_code == 200:
                        data = res.json()

                        st.session_state.chat.append({
                            "user": user_input,
                            "bot": data.get("response", "No response"),
                            "suggestion": data.get("suggestion") ,
                            "memories": data.get("memories_used", []),
                            "trace": data.get("trace", {})
                            
                        })

                    else:
                        st.error(f"Backend error: {res.status_code}")
                        st.write(res.text)

                except Exception as e:
                    st.error("Failed to connect to backend")
                    st.write(e)

    #  Chat display
        for chat in reversed(st.session_state.chat):

            st.markdown(f"""
            <div class="chat-user">
                🧑 {chat['user']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="chat-ai">
                🤖 {chat['bot']}
            </div>
            """, unsafe_allow_html=True)
            # 🌿 Journaling Suggestion
            if chat.get("suggestion"):
                st.markdown("""
                    <div style="
                        background: rgba(33, 156, 159,0.4);
                        padding:5px;
                        border-radius:5px;
                        margin-top:8px;
                    ">
                        <b>🌿 Journaling Suggestion</b><br><br>
                    </div>
                    """, unsafe_allow_html=True)

                # 🎯 Clickable suggestion button
                if st.button(f"🌿 {chat['suggestion']}", key=f"sugg_{chat['user']}"):
                    st.session_state.input_text = chat["suggestion"]
                    st.rerun()

        
            # 🌸 Memory indicator
            if chat.get("memories"):
                st.success("✨ Personalized using your memory")


            # 🔍 Expandable details (ONLY ONE expander)
            with st.expander("🔍 View Details"):

                # 🧠 Memories Section
                if chat.get("memories"):
                    st.markdown("### 🧠 Memories Used")
                    for m in chat["memories"]:
                        st.markdown(f"- {m}")

                # ⚙️ Harness Trace Section
                trace = chat.get("trace", {})

                if trace:
                    st.markdown("### ⚙️ AI Decision Process")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**🧭 Intent:** {trace.get('intent', 'N/A')}")
                        st.markdown(f"**📊 Sentiment:** {trace.get('sentiment', 'N/A')}")

                    with col2:
                        st.markdown(f"**🧠 Memory Used:** {trace.get('memory_used', False)}")
                        st.markdown(f"**📌 Memory Count:** {trace.get('memory_count', 0)}")

                st.divider()
            
              # ---------------- INSIGHTS ----------------
elif page == "Insights":
    st.subheader("Mood Insights")

    try:
        response = requests.get("http://localhost:8000/insights/1")

        if response.status_code == 200:
            data = response.json()

            if data:
                df = pd.DataFrame(list(data.items()), columns=["Mood", "Count"])
                st.bar_chart(df.set_index("Mood"))
            else:
                st.info("No data yet. Start journaling to see insights.")
        else:
            st.error(f"Backend error: {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error("Failed to connect to backend")
        st.write(e)
    st.divider()    
    #  Patterns
    st.subheader(" Detected Patterns")

    patterns = requests.get("http://localhost:8000/patterns/1").json()

    for p in patterns["patterns"]:
        st.info(p)

    st.divider()

    # Weekly Reflection
    st.subheader("Weekly Reflection")

    if st.button("Generate Reflection"):
        with st.spinner("Analyzing your week..."):
            res = requests.get("http://localhost:8000/weekly-reflection/1").json()

        st.success(res["reflection"])    

# ---------------- HISTORY ----------------
elif page == "History":
    st.subheader(" Journal History")

    entries = requests.get("http://localhost:8000/entries/1").json()

    for e in entries["entries"]:
        st.write(f" {e['content']} — *{e['sentiment']}*")
elif page == "Memory":
    st.subheader("Your Memory Bank")

    entries = requests.get("http://localhost:8000/entries/1").json()

    for i, e in enumerate(entries["entries"]):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"📝 {e['content']} — *{e['sentiment']}*")

        with col2:
            if st.button("❌", key=f"del_{e['id']}"):
                requests.delete(f"http://localhost:8000/delete/{e['id']}")
                st.rerun()
    if st.button("🧹 Clear All Memory"):
        requests.delete("http://localhost:8000/clear/1")
        st.success("All memory cleared")
        st.rerun()            