import os
import random
import re
import ast
import streamlit as st; 
# Configure the layout and title of the web app page
st.set_page_config(page_title="Interactive AI Game", layout="centered")

# Safe imports and setup for Grok compatibility (try Grok SDK, fallback not assumed)
try:
    import grok as grok_module
    GROK_AVAILABLE = True
except Exception:
    GROK_AVAILABLE = False

SAMPLE_QUESTIONS = ["what is 20x10?", "what is 2+2?", "what is the capital of France?", "what is 7*8?"]

# Initialize Streamlit session state variables to preserve data between re-runs
if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "current_response" not in st.session_state:
    st.session_state.current_response = ""
if "generated" not in st.session_state:
    st.session_state.generated = False

# App Heading
st.title("🎮 Interactive AI Game")
st.markdown("This application transforms your Tkinter desktop script into an interactive web app. Adjust positions via the sliders in real-time!")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Game Controls")

# API Key handling safely within the interface
# Look for a Grok API key in the environment and sidebar input
env_api_key = os.environ.get("GROK_API_KEY", "")
api_key = st.sidebar.text_input("Grok API Key", value=env_api_key, type="password", help="Enter your Grok API key here if available.")

# Setup OpenAI client structure based on library version
client = None
if GROK_AVAILABLE and api_key:
    # Try to initialize a Grok client if the SDK exposes a client class, otherwise keep module reference
    try:
        # Some Grok SDKs may provide a client constructor; try common names
        if hasattr(grok_module, "Grok"):
            client = grok_module.Grok(api_key=api_key)
        elif hasattr(grok_module, "Client"):
            client = grok_module.Client(api_key=api_key)
        else:
            client = grok_module
    except Exception:
        client = grok_module

# Positioning Controls (Streamlit translates canvas clicking into reactive layout sliders!)
st.sidebar.subheader("📍 Coordinates (Canvas: 800x400)")

st.sidebar.markdown("**Question Placement**")
qx = st.sidebar.slider("Question X Position", min_value=0, max_value=800, value=50, step=10)
qy = st.sidebar.slider("Question Y Position", min_value=0, max_value=400, value=60, step=10)

st.sidebar.markdown("**Response Placement**")
tx = st.sidebar.slider("Response X Position", min_value=0, max_value=800, value=50, step=10)
ty = st.sidebar.slider("Response Y Position", min_value=0, max_value=400, value=220, step=10)


# --- DATA LOGIC FUNCTIONS ---
def _extract_arithmetic_expr(text: str):
    """Return a safe arithmetic expression found in text, or None.
    Accepts operators + - * / and integer/float numbers. Treats 'x' as '*'.
    """
    t = text.replace('x', '*').replace('X', '*')
    # find sequences like 2+1 or 3 * (4+5)
    m = re.search(r"(-?[0-9]+(?:\s*[\+\-\*\/]\s*-?[0-9]+)+)", t)
    if m:
        return m.group(1)
    return None


def _safe_eval(expr: str):
    """Safely evaluate a simple arithmetic expression using ast parsing.
    Raises ValueError if expression contains non-arithmetic nodes.
    """
    node = ast.parse(expr, mode='eval')
    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
                     ast.UAdd, ast.USub, ast.Load, ast.Expr, ast.Tuple)
    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError("Unsafe expression")
    return eval(compile(node, '<string>', 'eval'), {"__builtins__": {}}, {})

def generate_question():
    """Fetches a question via Grok if available, or selects from predefined fallback options."""
    if GROK_AVAILABLE and api_key:
        try:
            prompt = "Please produce a short, clear question suitable for a simple quiz."
            # Try several common client call patterns to stay SDK-agnostic
            try:
                if client and hasattr(client, "chat") and hasattr(client.chat, "completions"):
                    resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=30)
                    return resp.choices[0].message.content.strip()
                if client and hasattr(client, "Completion") and hasattr(client.Completion, "create"):
                    resp = client.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=30)
                    return resp.choices[0].text.strip()
                if hasattr(client, "complete"):
                    # some Grok-like SDKs offer a simple complete() function
                    resp = client.complete(prompt)
                    # try common shapes
                    if isinstance(resp, dict) and "text" in resp:
                        return resp["text"].strip()
                    return str(resp).strip()
            except Exception:
                pass
            return random.choice(SAMPLE_QUESTIONS)
        except Exception:
            return random.choice(SAMPLE_QUESTIONS)
    else:
        return random.choice(SAMPLE_QUESTIONS)

def ask_openai_answer(question):
    """Answers the question using Grok (if available), or falls back to standard keyword checking matching the original code logic."""
    # Check for simple arithmetic first and evaluate locally
    try:
        expr = _extract_arithmetic_expr(question)
        if expr:
            try:
                val = _safe_eval(expr)
                # return integer style if whole number
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                return str(val)
            except Exception:
                pass
    except Exception:
        pass
    if GROK_AVAILABLE and api_key:
        try:
            prompt = f"Answer this question concisely: {question}"
            try:
                if client and hasattr(client, "chat") and hasattr(client.chat, "completions"):
                    resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=100)
                    return resp.choices[0].message.content.strip()
                if client and hasattr(client, "Completion") and hasattr(client.Completion, "create"):
                    resp = client.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)
                    return resp.choices[0].text.strip()
                if hasattr(client, "complete"):
                    resp = client.complete(prompt)
                    if isinstance(resp, dict) and "text" in resp:
                        return resp["text"].strip()
                    return str(resp).strip()
            except Exception:
                pass
            return "(Grok request failed; no answer.)"
        except Exception:
            return "(Grok request failed; no answer.)"
    else:
        # Local keyword parser fallback matching original code structure
        q = question.lower().strip()
        if "20x10" in q or "20 x 10" in q:
            return "200"
        if "2+2" in q or "2 + 2" in q:
            return "4"
        if "capital of france" in q:
            return "Paris"
        if "7*8" in q or "7 * 8" in q:
            return "56"
        return "(No local answer available.)"


# --- MAIN SCREEN INTERACTION ---
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🚀 Generate Content", use_container_width=True):
        with st.spinner("Processing AI query..."):
            st.session_state.current_question = generate_question()
            st.session_state.current_response = ask_openai_answer(st.session_state.current_question)
            st.session_state.generated = True
            st.rerun()

with col2:
    if st.button("🔄 Reset System", use_container_width=True):
        st.session_state.current_question = ""
        st.session_state.current_response = ""
        st.session_state.generated = False
        st.rerun()
# --- CUSTOM QUESTION INPUT ---

# Allow the user to type any question manually and use it instead of generating one
custom_q = st.text_input("Or enter your own question:", value="", key="custom_input")
if st.button("Use Custom Question"):
    if not custom_q.strip():
        st.warning("Please type a question before using this feature.")
    else:
        with st.spinner("Answering custom question..."):
            st.session_state.current_question = custom_q
            st.session_state.current_response = ask_openai_answer(custom_q)
            st.session_state.generated = True
            st.rerun()

# --- INTERACTIVE CANVAS RENDERING ---
st.subheader("🖼️ Simulated Digital Canvas")

# Render a beautiful absolute-positioned HTML space mimicking the original Tkinter canvas
canvas_html = f"""
<div style="
    width: 100%;
    max-width: 800px;
    height: 400px;
    background-color: #ffffff;
    border: 2px solid #e6e6e6;
    border-radius: 12px;
    position: relative;
    box-shadow: inset 0 4px 12px rgba(0,0,0,0.03);
    overflow: hidden;
">
    <!-- Visual Target Markers -->
    <div style="position: absolute; left: {qx}px; top: {qy}px; transform: translate(-50%, -50%); text-align: center;">
        <div style="width: 10px; height: 10px; background-color: #ff4b4b; border-radius: 50%; display: inline-block; box-shadow: 0 0 6px #ff4b4b;"></div>
        <div style="font-size: 10px; color: #777; background: rgba(255,255,255,0.8); padding: 1px 4px; border-radius: 4px; font-family: sans-serif; white-space: nowrap;">Q Target</div>
    </div>
    
    <div style="position: absolute; left: {tx}px; top: {ty}px; transform: translate(-50%, -50%); text-align: center;">
        <div style="width: 10px; height: 10px; background-color: #00d26a; border-radius: 50%; display: inline-block; box-shadow: 0 0 6px #00d26a;"></div>
        <div style="font-size: 10px; color: #777; background: rgba(255,255,255,0.8); padding: 1px 4px; border-radius: 4px; font-family: sans-serif; white-space: nowrap;">Ans Target</div>
    </div>

    <!-- Active Text Layer Injection -->
    {f'<div style="position: absolute; left: {qx}px; top: {qy}px; color: #1e3a8a; font-family: Arial, sans-serif; font-size: 18px; font-weight: 700; white-space: pre-wrap; padding-top: 12px;">{st.session_state.current_question}</div>' if st.session_state.current_question else ""}
    {f'<div style="position: absolute; left: {tx}px; top: {ty}px; color: #065f46; font-family: Arial, sans-serif; font-size: 16px; font-weight: 500; white-space: pre-wrap; padding-top: 12px;">{st.session_state.current_response}</div>' if st.session_state.current_response else ""}
</div>
"""

from streamlit.components.v1 import html as st_html

# Render the canvas HTML using the components HTML renderer to avoid showing raw markup
st_html(canvas_html, height=420)

# --- REFACTORING ORIGINAL BUTTON FUNCTIONALITY ---
if st.session_state.generated:
    st.subheader("📋 Response Workspace")
    st.markdown("Use the code-block helper below to copy the response to your system clipboard instantly via its native copy tool.")
    st.code(st.session_state.current_response, language="text")
    st.success("Status: Generation complete. Drag layout coordinates to realign dynamically.")
else:
    st.info("Status: Canvas initialized. Provide an API key if desired, then click 'Generate Content' to begin.")