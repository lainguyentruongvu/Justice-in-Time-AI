from __future__ import annotations

import streamlit as st

from engine.config import MODEL
from engine.prompt_builder import PromptBuilder
from engine.registry import REGISTRY
from engine.runner import RunnerError, run


st.set_page_config(
    page_title="Justice in Time AI",
    page_icon="⚖️",
    layout="wide",
)


def reset_chat() -> None:
    """Xóa lịch sử hội thoại hiện tại."""
    st.session_state.messages = []


def build_conversation(messages: list[dict[str, str]]) -> str:
    """Ghép lịch sử trò chuyện thành đầu vào cho Engine."""
    parts: list[str] = []

    for message in messages:
        role = message["role"].upper()
        content = message["content"].strip()
        parts.append(f"{role}:\n{content}")

    parts.append(
        "\nContinue the conversation by responding to the latest USER message. "
        "Do not repeat previous answers unless necessary."
    )

    return "\n\n".join(parts)


# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.title("⚖️ Justice in Time AI")
    st.caption("True Crime Content Engine")

    task_names = list(REGISTRY.keys())

    selected_task = st.selectbox(
        "Chọn tác vụ",
        options=task_names,
        index=task_names.index("jit_script")
        if "jit_script" in task_names
        else 0,
        format_func=lambda task: (
            f"{task} — {REGISTRY[task].description}"
        ),
    )

    selected_model = st.text_input(
        "Model",
        value=MODEL,
        help="Model được lấy từ file .env. Có thể thay đổi cho phiên làm việc này.",
    )

    brand = st.text_input(
        "Brand",
        value="Justice in Time",
    )

    language = st.selectbox(
        "Ngôn ngữ đầu ra",
        options=["English", "Vietnamese", "Bilingual English-Vietnamese"],
        index=0,
    )

    tone = st.selectbox(
        "Phong cách",
        options=[
            "Documentary",
            "Investigative",
            "Emotional but factual",
            "Professional",
            "Conversational",
        ],
        index=0,
    )

    show_prompt = st.checkbox(
        "Hiển thị System Prompt",
        value=False,
    )

    if st.button(
        "＋ Cuộc trò chuyện mới",
        use_container_width=True,
    ):
        reset_chat()
        st.rerun()

    st.divider()

    st.caption(f"Task hiện tại: `{selected_task}`")
    st.caption(f"Model hiện tại: `{selected_model}`")


# =========================
# MAIN CHAT UI
# =========================

st.title("Justice in Time AI")
st.caption(REGISTRY[selected_task].description)

variables = {
    "brand": brand,
    "language": language,
    "tone": tone,
}

try:
    prompt_builder = PromptBuilder(
        selected_task,
        variables=variables,
    )
    system_prompt = prompt_builder.build()
    token_estimate = prompt_builder.token_estimate()
except Exception as exc:
    st.error(f"Không thể tạo System Prompt: {exc}")
    st.stop()


col1, col2 = st.columns([1, 1])

with col1:
    st.metric(
        "System Prompt Tokens",
        f"{token_estimate:,}",
    )

with col2:
    st.metric(
        "Số tin nhắn",
        len(st.session_state.messages),
    )


if show_prompt:
    with st.expander(
        "System Prompt đã được Engine tổng hợp",
        expanded=False,
    ):
        st.code(system_prompt, language="markdown")


# Hiển thị lịch sử hội thoại
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            """
Xin chào! Tôi là **Justice in Time AI**.

Hãy nhập yêu cầu, ví dụ:

> Create a 25-minute documentary script about the Isabella Guzman case for a U.S. audience aged 25–45.

Bạn có thể đổi tác vụ ở thanh bên trái để tạo hook, tiêu đề, mô tả, bình luận hoặc phân tích video.
"""
        )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Ô nhập chat
user_input = st.chat_input(
    "Nhập yêu cầu cho Justice in Time AI..."
)

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    conversation_input = build_conversation(
        st.session_state.messages
    )

    with st.chat_message("assistant"):
        with st.spinner("Justice in Time AI đang xử lý..."):
            try:
                answer = run(
                    system_prompt=system_prompt,
                    user_prompt=conversation_input,
                    model=selected_model.strip(),
                )
            except RunnerError as exc:
                answer = f"⚠️ **Không thể tạo nội dung:**\n\n{exc}"
            except Exception as exc:
                answer = f"⚠️ **Đã xảy ra lỗi:**\n\n{exc}"

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )