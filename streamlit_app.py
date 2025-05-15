import streamlit as st
import httpx
import uuid
import json
import os
from dotenv import load_dotenv

load_dotenv()

# 페이지 제목 설정
st.set_page_config(
    page_title="Database Agent ChatBot",
    page_icon="🤖",
    layout="wide"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# API 설정
API_HOST = os.getenv("API_HOST", "http://localhost:10001")

def query_database_agent(query, session_id):
    """Database Agent API 호출"""
    url = f"{API_HOST}/query"
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                url,
                json={"query": query, "session_id": session_id}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"API 요청 오류: {str(e)}")
        return {"content": f"오류가 발생했습니다: {str(e)}", "require_user_input": True}

# UI 헤더 설정
st.title("💬 Database Agent ChatBot")
st.markdown("""
이 챗봇은 자연어로 데이터베이스에 질의하고 SQL을 생성합니다.
예시 질문:
- 데이터베이스 스키마를 보여줘
- 고객 테이블의 구조가 어떻게 되나요?
- 매출이 가장 높은 상위 5명의 고객을 보여줘
""")

# 채팅 이력 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("SQL을 생성할 자연어 질문을 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 봇 응답 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 생각 중...")
        
        # API 호출
        response = query_database_agent(prompt, st.session_state.session_id)
        
        if "content" in response:
            # 응답 표시
            message_placeholder.markdown(response["content"])
            # 봇 메시지 저장
            st.session_state.messages.append({"role": "assistant", "content": response["content"]})
        else:
            message_placeholder.markdown("응답 형식이 올바르지 않습니다.")

# 사이드바에 세션 정보 및 컨트롤 추가
with st.sidebar:
    st.subheader("세션 정보")
    st.text(f"세션 ID: {st.session_state.session_id}")
    
    if st.button("대화 내용 지우기"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("새 세션 시작"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")
    st.markdown("2025 Database Agent - NL to SQL Assistant")
