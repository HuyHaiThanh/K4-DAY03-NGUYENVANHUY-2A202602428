"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
import re
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """Offline Mock Provider dùng để chạy thử mà không tốn API Key"""
    def __init__(self):
        self.model_name = "Offline-Mock-Model-2026"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return f"[Mock Chatbot Response]: Xin chào! Tôi đã nhận được câu hỏi '{prompt}'. (Chế độ Chatbot không có Tool tra cứu dữ liệu thời gian thực)."

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        # Tách câu hỏi gốc và observation do vòng lặp truyền lại.
        query, separator, history = prompt.partition("\nOBSERVATIONS:\n")
        observations = json.loads(history) if separator else []
        prompt_lower = query.lower()
        student = re.search(r"\bSV\d+\b", query, re.IGNORECASE)
        student_id = student.group().upper() if student else None
        if observations:
            result = observations[-1]["result"]
            if result.get("status") != "SUCCESS" or observations[-1]["tool_name"] == "schedule_appointment" or "đặt lịch" not in prompt_lower:
                # Observation giữ JSON cho log; câu trả lời cho sinh viên dùng văn bản.
                content = result.get("message") or result.get("error")
                if result.get("status") == "SUCCESS" and "data" in result:
                    data = result["data"]
                    content = (
                        f"Thông tin sinh viên {result.get('student_id', student_id)} "
                        f"({data.get('full_name', '')}): Lớp {data.get('class', '')}, "
                        f"GPA: {data.get('gpa', '')}, Email: {data.get('email', '')}, "
                        f"Trạng thái: {data.get('status', '')}, Cố vấn: {data.get('advisor', '')}."
                    )
                return {"type": "text", "content": content or "Tool chưa cung cấp thông tin trả lời.",
                        "thought": "Tổng hợp kết quả thực tế từ công cụ."}
        if not student_id:
            # Chỉ hỏi mã khi yêu cầu cần dữ liệu sinh viên; câu hỏi chung không cần mã.
            if "tra cứu" in prompt_lower or "đặt lịch" in prompt_lower:
                return {"type": "text", "content": "[Mock] Vui lòng cung cấp mã sinh viên để tra cứu hoặc đặt lịch.",
                        "thought": "Yêu cầu dùng tool còn thiếu mã sinh viên."}
            return {
                "type": "text",
                "content": "[Mock] Chào bạn! Quy chế học vụ thường bao gồm đăng ký học phần, "
                           "đánh giá kết quả học tập, cảnh báo học vụ và điều kiện tốt nghiệp. "
                           "Bản mô phỏng chưa có tài liệu quy chế VinUni để cung cấp các quy định cụ thể.",
                "thought": "Câu hỏi chung, trả lời trực tiếp không cần gọi tool."
            }
        
        # Mock nhận diện tên sau "với", dừng trước ngày giờ hoặc cuối câu.
        # Đây là quy tắc cho bài lab, không phải bộ hiểu ngôn ngữ tổng quát.
        advisor_match = re.search(
            r"\bvới\s+(.+?)(?=\s+(?:vào|lúc)\b|[,;!?]|$)", query, re.IGNORECASE
        )
        explicit_advisor = advisor_match.group(1).strip().rstrip(".") if advisor_match else None
        # "Cố vấn đó" là tham chiếu cần tra cứu, không phải tên người cụ thể.
        if explicit_advisor and re.match(r"^(?:cố vấn|giảng viên)(?:\s+(?:đó|này|của)\b|$)", explicit_advisor, re.IGNORECASE):
            explicit_advisor = None
        needs_lookup = "tra cứu" in prompt_lower or not explicit_advisor
        if "đặt lịch" in prompt_lower and (observations or not needs_lookup):
            # Ưu tiên tên người dùng chỉ định; chỉ lấy từ hồ sơ khi chưa có tên.
            hour = re.search(r"\b(?:[01]\d|2[0-3]):[0-5]\d\b", query)
            date = re.search(r"\b\d{2}/\d{2}/\d{4}\b", query)
            advisor = explicit_advisor or observations[-1]["result"].get("data", {}).get("advisor")
            if not hour or not date or not advisor:
                return {"type": "text", "content": "Chưa đủ ngày giờ hoặc thông tin cố vấn để đặt lịch."}
            return {
                "type": "tool_call",
                "tool_name": "schedule_appointment",
                "arguments": {"student_id": student_id, "datetime_str": f"{hour.group()} {date.group()}", "advisor_name": advisor},
                "thought": "Đã có đủ thông tin để đặt lịch theo yêu cầu."
            }
        elif student_id:
            return {
                "type": "tool_call",
                "tool_name": "academic_query",
                "arguments": {"student_id": student_id},
                "thought": "Tra cứu thông tin sinh viên và cố vấn trước khi thực hiện bước tiếp theo."
            }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không
            if response.function_calls:
                call = response.function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": response.text or "",
                    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            # Đọc endpoint từ .env để dùng NVIDIA hoặc dịch vụ tương thích OpenAI.
            # Khi không cấu hình endpoint, SDK dùng địa chỉ OpenAI mặc định.
            client = OpenAI(
                api_key=self.api_key,
                base_url=os.getenv("OPENAI_BASE_URL") or None,
            )
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            # Tool calling dùng cùng endpoint với phần trả lời văn bản ở trên.
            client = OpenAI(
                api_key=self.api_key,
                base_url=os.getenv("OPENAI_BASE_URL") or None,
            )

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()
