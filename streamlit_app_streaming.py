import streamlit as st
import httpx
import uuid
import json
import os
import asyncio
from dotenv import load_dotenv
import time

load_dotenv()

# 페이지 제목 설정
st.set_page_config(
    page_title="Database Agent ChatBot (Streaming)",
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

async def stream_response(query, session_id):
    """Database Agent API 스트리밍 호출"""
    url = f"{API_HOST}/query/stream"
    full_response = ""
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                url,
                json={"query": query, "session_id": session_id},
                headers={"Accept": "text/event-stream"},
                stream=True
            )
            
            response.raise_for_status()
            
            # 스트리밍 응답 처리
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]  # "data: " 제거
                    if data == "[DONE]":
                        break
                    
                    try:
                        chunk = json.loads(data)
                        if "content" in chunk:
                            full_response += chunk["content"]
                            yield chunk["content"], False
                    except json.JSONDecodeError:
                        pass
    
    except httpx.HTTPError as e:
        error_msg = f"API 요청 오류: {str(e)}"
        yield error_msg, True
        return
    
    yield full_response, True

# UI 헤더 설정
st.title("💬 Database Agent ChatBot (Streaming)")
st.markdown("""
이 챗봇은 자연어로 데이터베이스에 질의하고 SQL을 생성합니다. 스트리밍 버전은 응답을 실시간으로 보여줍니다.

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
        
        # 스트리밍 처리를 위한 코드
        full_response = ""
        
        # 스트리밍을 구현하기 위한 간소화된 방법 (비동기 대신)
        for chunk in st.empty():
            with st.spinner("생각 중..."):
                for i in range(10):  # 최대 10번의 청크를 시뮬레이션
                    # 실제로는 API 스트리밍 응답 코드로 대체됩니다
                    # 스트리밍 버전을 구현하기 위한 모의 코드
                    time.sleep(0.5)
                    full_response += f"응답 부분 {i+1}... "
                    message_placeholder.markdown(full_response + "▌")
        
        # 최종 응답 설정
        message_placeholder.markdown(full_response)
        # 봇 메시지 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})

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
    st.markdown("© 2025 Database Agent - NL to SQL Assistant")
