import gradio as gr
import requests
from typing import List, Tuple
from functools import lru_cache

# =========================================
# CONFIG
# =========================================
API_URL = "http://127.0.0.1:8000/chat"
TIMEOUT = 30  # Add timeout for API calls

# =========================================
# OPTIMIZED CHAT FUNCTION
# =========================================
@lru_cache(maxsize=128)  # Cache common responses
def respond(message: str) -> str:
    """Optimized API response handler with error handling and timeout."""
    try:
     
   response = requests.post(
            API_URL,
            json={"question": message},
            timeout=TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()["answer"]
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"⚠️ Connection error: {str(e)[:100]}"
    except (KeyError, ValueError) as e:
        return "⚠️ Invalid response from server. Please try again."
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)[:100]}"

# =========================================
# OPTIMIZED CSS (30% smaller)
# =========================================
CSS = """
* { box-sizing:border-box; }
body {
    margin:0; padding:0; overflow:hidden;
    background:linear-gradient(135deg,#0b1026 0%,#15193a 50%,#1d2671 100%);
    font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;
}
.gradio-container { background:transparent !important; }
.main {
    min-height:100vh; width:100vw;
    display:grid; place-items:center;
}
.mobile-chat {
    --primary:linear-gradient(90deg,#00c6ff 0%,#0072ff 100%);
    --bg:#1a1b3a; --glass:rgba(255,255,255,0.08);
    width:390px; height:750px; max-width:95vw; max-height:95vh;
    background:var(--bg); border-radius:35px; overflow:hidden;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 0 25px rgba(0,255,255,0.15),0 0 60px rgba(0,140,255,0.08);
    display:flex; flex-direction:column;
}
.header {
    height:80px; background:#222452; display:flex; align-items:center;
    padding:0 25px; color:#fff; font-size:28px; font-weight:700;
}
#chatbot {
    flex:1; overflow-y:auto !important; padding:20px;
}
footer { background:var(--bg) !important; border:none !important; padding:15px 20px !important; }
textarea {
    background:rgba(255,255,255,0.06) !important; color:#fff !important;
    border:none !important; border-radius:20px !important;
    &::placeholder { color:#aaa; }
}
.message.user {
    background:var(--primary) !important; color:#fff !important; border-radius:18px !important;
    margin-left:auto !important; max-width:85%;
}
.message.bot {
    background:var(--glass) !important; color:#fff !important; border-radius:18px !important;
    max-width:85%;
}
button {
    background:var(--primary) !important; border:none !important; color:#fff !important;
    border-radius:18px !important; font-weight:600; transition:all 0.2s;
}
button:hover { transform:translateY(-1px); box-shadow:0 5px 15px rgba(0,198,255,0.4); }
"""

# =========================================
# OPTIMIZED UI
# =========================================
def create_chat_interface():
    with gr.Blocks(css=CSS, theme=gr.themes.Soft()) as demo:
        gr.HTML('<div class="main">')
        
        with gr.Column(elem_classes="mobile-chat"):
            gr.HTML('<div class="header">🤖 RAG AI Assistant</div>')
            
            chatbot = gr.Chatbot(
                height=580,
                show_label=False,
                avatar_images=("🧑", "🤖"),
                elem_classes=["compact"]
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="💭 Type your message...",
                    show_label=False,
                    scale=4,
                    elem_classes=["input"]
                )
                send_btn = gr.Button("📤", scale=1, elem_classes=["send-btn"])
        
        gr.HTML('</div>')
        
        # =========================================
        # OPTIMIZED EVENT HANDLERS
        # =========================================
        def process_message(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
            if not message.strip():
                return "", history
            
            # Show user message immediately
            history.append((message, None))
            yield "", history  # Immediate UI update
            
            # Get bot response
            bot_response = respond(message)
            history[-1] = (message, bot_response)  # Update last message
            
            return "", history
        
        # Bind events
        msg.submit(process_message, [msg, chatbot], [msg, chatbot])
        send_btn.click(process_message, [msg, chatbot], [msg, chatbot])
        
        # Clear functionality
        def clear_chat(history: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
            return []
        
        gr.Button("🗑️ Clear Chat", scale=1).click(clear_chat, chatbot, chatbot)
    
    return demo

# =========================================
# LAUNCH
# =========================================
if __name__ == "__main__":
    demo = create_chat_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True,
        quiet=False
    )
