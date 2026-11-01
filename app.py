import html as _html

import streamlit as st

from reviewer import create_review_chain
from assistant import create_assistant_chain


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Code Review AI",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HELPERS
# ============================================================

def render(markup: str):
    """
    Render raw HTML/CSS in Streamlit.

    Streamlit's markdown parser turns lines indented by 4+ spaces into
    code blocks, and blank lines break HTML blocks. So we strip all
    leading whitespace and drop empty lines before rendering.
    """
    cleaned = "\n".join(
        line.strip() for line in markup.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


def esc(value) -> str:
    """Escape model output so it can't break the HTML."""
    return _html.escape(str(value))


def review_card(title: str, items, empty_text: str = ""):
    """Render a whole card in ONE markdown call (divs must open+close together)."""
    if items:
        body = "".join(
            f'<div class="review-card-content">— {esc(i)}</div>' for i in items
        )
    elif empty_text:
        body = f'<div class="review-card-content">{esc(empty_text)}</div>'
    else:
        return

    render(
        f"""
        <div class="review-card">
        <div class="review-card-title">{esc(title)}</div>
        {body}
        </div>
        """
    )


# ============================================================
# CUSTOM CSS
# ============================================================

render(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: #111111;
        color: #ffffff;
        overflow-x: hidden;
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .block-container {
        padding-top: 0rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        padding-bottom: 0rem !important;
        max-width: 1500px !important;
    }

    /* ---------- NAV ---------- */
    .top-nav {
        width: 100%;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #ffffff;
    }
    .logo {
        font-family: 'DM Mono', monospace;
        font-size: 17px;
        font-weight: 500;
        letter-spacing: -1px;
    }
    .logo-line {
        width: 24px;
        height: 1px;
        background: #ffffff;
        margin-top: 3px;
    }
    .nav-center {
        display: flex;
        gap: 42px;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
    }
    .nav-item { color: #858585; transition: 0.3s; }
    .nav-item:hover { color: #ffffff; }
    .nav-contact { color: #ffffff; }

    /* ---------- HERO ---------- */
    .hero {
        min-height: 700px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .hero-circle {
        width: 82px;
        height: 82px;
        border-radius: 50%;
        background: #f5f5f5;
        color: #111111;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-family: 'Inter', sans-serif;
        position: relative;
        z-index: 3;
        margin-bottom: 55px;
        box-shadow: 0 0 0 1px rgba(255,255,255,0.15);
    }
    .circle-small { font-size: 12px; font-weight: 600; line-height: 14px; }
    .circle-text { font-size: 10px; color: #555555; line-height: 12px; }

    .vertical-line {
        position: absolute;
        width: 1px;
        height: 610px;
        background: rgba(255,255,255,0.16);
        top: 45px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1;
    }

    .hero-title {
        position: relative;
        z-index: 4;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: clamp(65px, 10vw, 145px);
        font-weight: 300;
        line-height: 0.85;
        letter-spacing: 15px;
        text-transform: uppercase;
        margin: 0;
        padding: 0;
        color: #f5f5f5;
    }
    .hero-title strong {
        font-family: 'DM Mono', monospace;
        font-weight: 500;
        font-size: 0.52em;
        letter-spacing: 13px;
        display: block;
        margin-top: 30px;
    }

    .hero-description {
        position: relative;
        z-index: 5;
        max-width: 430px;
        margin-top: 55px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        line-height: 1.8;
        color: #8d8d8d;
        letter-spacing: 0.5px;
    }

    .wave-section {
        position: absolute;
        bottom: -2px;
        left: -5%;
        width: 110%;
        height: 100px;
        background: #f5f5f5;
        clip-path: polygon(
            0% 55%, 5% 62%, 11% 58%, 17% 72%, 25% 65%, 32% 77%,
            40% 69%, 48% 84%, 55% 70%, 61% 80%, 69% 67%, 76% 74%,
            84% 61%, 91% 69%, 100% 57%, 100% 100%, 0% 100%
        );
        z-index: 10;
    }

    /* ---------- LIGHT REVIEW AREA (st.container(key="review_area")) ---------- */
    .st-key-review_area {
        background: #f5f5f5;
        color: #111111;
        width: 100vw;
        margin-left: calc(50% - 50vw);
        padding: 60px 8% 120px 8%;
        margin-top: -1rem;
    }
    .st-key-review_area [data-testid="stMarkdownContainer"],
    .st-key-review_area [data-testid="stMarkdownContainer"] p,
    .st-key-review_area [data-testid="stChatMessage"] {
        color: #111111;
    }

    .section-label {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #777777;
        margin-bottom: 20px;
    }
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: clamp(42px, 6vw, 90px);
        font-weight: 300;
        letter-spacing: -4px;
        line-height: 0.95;
        margin-bottom: 60px;
        color: #111111;
    }
    .divider {
        margin-top: 80px;
        border-top: 1px solid #111111;
        padding-top: 40px;
    }

    /* ---------- INPUTS ---------- */
    div[data-baseweb="select"] > div {
        background: #171717 !important;
        border: 1px solid #333333 !important;
        color: white !important;
    }
    textarea {
        background: #171717 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 13px !important;
    }
    textarea:focus { border-color: #ffffff !important; }
    label, label p {
        color: #777777 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }

    /* ---------- BUTTON ---------- */
    .stButton > button {
        background: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #111111 !important;
        border-radius: 0px !important;
        padding: 14px 30px !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        transition: 0.3s !important;
    }
    .stButton > button:hover {
        background: #333333 !important;
        border-color: #333333 !important;
    }

    /* ---------- REVIEW CARDS ---------- */
    .review-card {
        background: #ffffff;
        border-top: 1px solid #111111;
        padding: 30px 20px;
        margin-bottom: 20px;
    }
    .review-card-title {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
        color: #111111;
    }
    .review-card-content {
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        line-height: 1.7;
        color: #333333;
        margin-bottom: 6px;
    }

    /* ---------- SCORE ---------- */
    .score-container {
        display: flex;
        align-items: baseline;
        gap: 15px;
        margin-bottom: 60px;
        color: #111111;
    }
    .score {
        font-family: 'DM Mono', monospace;
        font-size: 90px;
        line-height: 1;
        letter-spacing: -8px;
    }
    .score-label {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        color: #777777;
        letter-spacing: 2px;
    }

    /* ---------- CHAT ---------- */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border-bottom: 1px solid #dddddd;
        border-radius: 0px;
        padding: 20px 0px;
    }
    [data-testid="stChatInput"] { border-radius: 0px !important; }

    /* ---------- MOBILE ---------- */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 20px !important;
            padding-right: 20px !important;
        }
        .nav-center { display: none; }
        .hero-title { font-size: 55px; letter-spacing: 7px; }
        .hero-title strong { letter-spacing: 5px; }
        .hero { min-height: 650px; }
        .st-key-review_area { padding-left: 25px; padding-right: 25px; }
    }
    </style>
    """
)


# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("review", None)
st.session_state.setdefault("code", "")
st.session_state.setdefault("language", "Python")
st.session_state.setdefault("messages", [])


# ============================================================
# NAV + HERO
# ============================================================

render(
    """
    <div class="top-nav">
    <div class="logo">CR<div class="logo-line"></div></div>
    <div class="nav-center">
    <div class="nav-item">REVIEW</div>
    <div class="nav-item">ASSISTANT</div>
    <div class="nav-item">ABOUT</div>
    </div>
    <div class="nav-contact">GET IN TOUCH</div>
    </div>
    """
)

render(
    """
    <section class="hero">
    <div class="vertical-line"></div>
    <div class="hero-circle">
    <div class="circle-small">AI</div>
    <div class="circle-text">for</div>
    <div class="circle-small">CODE</div>
    </div>
    <h1 class="hero-title">CODE<strong>REVIEWER</strong></h1>
    <div class="hero-description">
    Intelligent code analysis for modern developers.
    Find bugs, improve security, optimize performance,
    and build better software with AI.
    </div>
    <div class="wave-section"></div>
    </section>
    """
)


# ============================================================
# REVIEW AREA (light section)
# ============================================================

area = st.container(key="review_area")

with area:

    render(
        """
        <div class="section-label">01 — CODE ANALYSIS</div>
        <div class="section-title">Review<br>Your Code.</div>
        """
    )

    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "Java", "C++", "C", "HTML", "CSS", "SQL"],
    )

    code = st.text_area(
        "Your Code",
        height=420,
        placeholder="""Paste your code here...

Example:

def calculate_total(items):
    total = 0

    for item in items:
        total += item["price"]

    return total
""",
    )

    review_button = st.button("ANALYZE CODE →")

    if review_button:
        if not code.strip():
            st.warning("Please enter some code before starting the review.")
        else:
            try:
                with st.spinner("Analyzing your code..."):
                    review_chain = create_review_chain()
                    review = review_chain.invoke(
                        {"language": language, "code": code}
                    )

                st.session_state.review = review
                st.session_state.code = code
                st.session_state.language = language
                st.session_state.messages = []  # reset assistant on new review

                st.success("Code analysis completed.")

            except Exception as e:
                st.error(f"Review error: {e}")

    # --------------------------------------------------------
    # DISPLAY REVIEW
    # --------------------------------------------------------

    if st.session_state.review:
        review = st.session_state.review

        render(
            """
            <div class="divider">
            <div class="section-label">02 — ANALYSIS RESULT</div>
            </div>
            """
        )

        render(
            f"""
            <div class="score-container">
            <div class="score">{esc(review.score)}</div>
            <div class="score-label">/ 10<br>CODE QUALITY</div>
            </div>
            """
        )

        review_card("SUMMARY", [review.summary])
        review_card("BUGS", review.bugs, "No major bugs detected.")
        review_card("SECURITY", review.security, "No obvious security issues detected.")
        review_card("PERFORMANCE", review.performance, "No major performance problems detected.")
        review_card("READABILITY", review.readability, "Readability looks good.")
        review_card("SUGGESTIONS", review.suggestions)

        # ----------------------------------------------------
        # AI ASSISTANT
        # ----------------------------------------------------

        render(
            """
            <div class="divider" style="margin-top:120px;">
            <div class="section-label">03 — AI ASSISTANT</div>
            <div class="section-title">Talk<br>To Your Code.</div>
            </div>
            """
        )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


# chat_input is created OUTSIDE the container so it stays pinned to the bottom
question = None
if st.session_state.review:
    question = st.chat_input("Ask something about your code...")

if question:
    with area:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    assistant_chain = create_assistant_chain()
                    review_text = st.session_state.review.model_dump_json(indent=2)

                    response = assistant_chain.invoke(
                        {
                            "language": st.session_state.language,
                            "code": st.session_state.code,
                            "review": review_text,
                            "question": question,
                        }
                    )
                    answer = response.content

                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Assistant error: {e}")


# ============================================================
# FOOTER
# ============================================================

render(
    """
    <div style="
    background:#111111;
    color:#777777;
    width:100vw;
    margin-left:calc(50% - 50vw);
    padding:70px 8%;
    box-sizing:border-box;
    font-family:'DM Mono',monospace;
    font-size:10px;
    letter-spacing:2px;
    text-transform:uppercase;
    display:flex;
    justify-content:space-between;
    border-top:1px solid #333333;
    ">
    <div>CODE REVIEW AI</div>
    <div>POWERED BY LANGCHAIN × OPENROUTER</div>
    <div>2026</div>
    </div>
    """
)