"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
(.venv) PS C:\VIN_AI\LAB_04\K4A-Day03-Lab-Chatbot-vs-ReAct-A-NGUYENVANHUY-2A202602428> python src/app.py --all
==========================================================
🏫 VINUNI AI COURSE - DAY 03 LAB: CHATBOT VS REACT AGENT
==========================================================
🔌 LLM Provider: OpenAIProvider
🌐 MCP Server: vinuni-academic-mcp-server

✅ Đã tải thành công 5 Test Cases thử nghiệm.

🚀 [TEST SUITE MODE] Kiểm tra 5 Test Cases:

==================================================
🧪 [TC01] Loại test: direct_query (Độ phức tạp: Low)
📌 Kỳ vọng: Chatbot trả lời trực tiếp từ System Prompt, không cần gọi bất kỳ Tool nào.

🤖 [REACT AGENT] Câu hỏi: Chào bạn, bạn có thể giới thiệu quy chế học vụ cơ bản của Đại học VinUni không?

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
🏁 [Final Answer]: Quy chế học vụ ở Đại học VinUni chung bao gồm các chủ đề chính sau:

| T phạm | Nội dung chính | Lưu ý |
|--------|-----------------|-------|
| **Đăng ký học tập** | Hệ thống đăng ký tín chỉ, thời hạn đăng ký bài học, quy định về ký học, thay đổi môn học. | Thời hạn, quy trình và hạn mức tín chỉ thường được đăng tải trong hệ thống ám dương. |
| **Chấm điểm và cấp chứng chỉ** | Quy tắc chấm điểm, bảng điểm, thang điểm, làm lại, học phần thôi kỳ. | Mức điểm tối thiểu, điều kiện chuyển “đậu, chưa đủ” thường được quy định trong quy chế. |
| **Huyện sinh hoạt, thời gian giảng dạy** | Lịch học, giờ giảng, quản lý thời gian, nghỉ học, nghỉ cuối học, học kỳ, học kỳ giữa. | Lịch trình truyền thông qua portal sinh viên. |
| **Học bổng, hỗ trợ tài chính** | Quy định học bổng, xét duyệt, điều kiện, thời hạn nộp, giấy tờ cầnthiết. | Cập nhật thường thấy trên trang web chuyên theo từng đợt. |
| **Quy chế hành chính học tập** | Hình thức kỷ luật, quy tắc nghiêm nghị, hành vi bị cấm, quy trình xử lý. | Các mức hình thức kỷ luật (giãn học, đình chỉ, thôi học) thường được ghi chữ viết rõ ràng. |
| **Bảng điểm, chuyển sinh** | Quy trình xin bảng điểm, chuyển lớp, chuyển trường, chuyển học. | Thủycấp thường diễn ra theo chu kỳ học kỳ. |

Để biết đầy đủ, chính xác và cập nhật nhất, bạn nên tham khảo:
- **Hệ thống giao thông sinh viên (VINIS portal)** – các tài liệu PDF, thông báo và bảng điểm của bạn.
- **Hướng dẫn duyệt hệ thống học phần** trong thư viện số của VinUni.
- **Quy chế học vụ** và *Thư viện quy chế* (nếu có) của trường.

Nếu bạn muốn biết chi tiết cụ thể về một phần như thời hạn đăng ký hoặc thang điểm, hãy truy cập các tài liệu chính thức trên portal hoặc liên hệ trực tiếp với phòng Học vụ / Văn phòng Học viện.

==================================================
🧪 [TC02] Loại test: single_tool_query (Độ phức tạp: Medium)
📌 Kỳ vọng: Agent nhận diện nhu cầu tra cứu, tự động phát sinh Tool Call 'academic_query' với mã SV2026001.

🤖 [REACT AGENT] Câu hỏi: Hãy tra cứu thông tin học vụ của sinh viên SV2026001.

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: OpenAI quyết định gọi công cụ 'academic_query' với tham số: {"student_id": "SV2026001"}
🛠️ [Action Proposed]: academic_query({'student_id': 'SV2026001'})
👁️ [Observation từ MCP Server]: {"status": "SUCCESS", "student_id": "SV2026001", "data": {"full_name":"Nguyễn Văn An", "class": "AI-K4", "gpa": 3.85, "email": "an.nv@vinuni.edu.vn", "status": "Đang học","advisor": "PGS.TS Nguyễn Văn A"}}

--- 🔄 Vòng lặp ReAct Loop (Step 2/5) ---
🧠 [Thought]: OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
🏁 [Final Answer]: Sinh viên có mã **SV2026001**:
- **Họ và tên**: Nguyễn Văn An  
- **Lớp**: AI-K4  
- **Điểm trung bình (GPA)**: 3.85  
- **Email**: an.nv@vinuni.edu.vn  
- **Trạng thái học tập**: Đang học  
- **Cố vấn học tập**: PGS.TS Nguyễn Văn A

==================================================
🧪 [TC03] Loại test: appointment_booking (Độ phức tạp: Medium)
📌 Kỳ vọng: Agent gọi schedule_appointment với đầy đủ tham số.

🤖 [REACT AGENT] Câu hỏi: Đặt lịch tư vấn cho sinh viên SV2026001 với PGS.TS Nguyễn Văn A vào 14:00 15/09/2026.

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: OpenAI quyết định gọi công cụ 'schedule_appointment' với tham số: {"student_id": "SV2026001", "datetime_str": "14:00 15/09/2026", "advisor_name": "PGS.TS Nguyễn Văn A"}
🛠️ [Action Proposed]: schedule_appointment({'student_id': 'SV2026001', 'datetime_str': '14:00 15/09/2026', 'advisor_name': 'PGS.TS Nguyễn Văn A'})
👁️ [Observation từ MCP Server]: {"status": "SUCCESS", "booking_id": "BK-SV2026001-99", "student_id": "SV2026001", "datetime": "14:00 15/09/2026", "advisor": "PGS.TS Nguyễn Văn A", "message": "Đặt lịch thành công cho sinh viên SV2026001 với PGS.TS Nguyễn Văn A vào lúc 14:00 15/09/2026."}

--- 🔄 Vòng lặp ReAct Loop (Step 2/5) ---
🧠 [Thought]: OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
🏁 [Final Answer]: Đặt lịch thành công cho sinh viên **SV2026001** với PGS.TS Nguyễn Văn A vào **14:00 15/09/2026**.  
Mã đặt lịch: **BK-SV2026001-99**.

==================================================
🧪 [TC04] Loại test: multi_step_reasoning (Độ phức tạp: High)
📌 Kỳ vọng: Agent tra cứu thông tin trước rồi đặt lịch với cố vấn tìm được.

🤖 [REACT AGENT] Câu hỏi: Tra cứu cố vấn của sinh viên SV2026001, sau đó đặt lịch tư vấn vào 09:00 20/09/2026 với cố vấn đó.

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: OpenAI quyết định gọi công cụ 'academic_query' với tham số: {"student_id": "SV2026001"}
🛠️ [Action Proposed]: academic_query({'student_id': 'SV2026001'})
👁️ [Observation từ MCP Server]: {"status": "SUCCESS", "student_id": "SV2026001", "data": {"full_name":"Nguyễn Văn An", "class": "AI-K4", "gpa": 3.85, "email": "an.nv@vinuni.edu.vn", "status": "Đang học","advisor": "PGS.TS Nguyễn Văn A"}}

--- 🔄 Vòng lặp ReAct Loop (Step 2/5) ---
🧠 [Thought]: OpenAI quyết định gọi công cụ 'schedule_appointment' với tham số: {"student_id": "SV2026001", "datetime_str": "09:00 20/09/2026", "advisor_name": "PGS.TS Nguyễn Văn A"}
🛠️ [Action Proposed]: schedule_appointment({'student_id': 'SV2026001', 'datetime_str': '09:00 20/09/2026', 'advisor_name': 'PGS.TS Nguyễn Văn A'})
👁️ [Observation từ MCP Server]: {"status": "SUCCESS", "booking_id": "BK-SV2026001-99", "student_id": "SV2026001", "datetime": "09:00 20/09/2026", "advisor": "PGS.TS Nguyễn Văn A", "message": "Đặt lịch thành công cho sinh viên SV2026001 với PGS.TS Nguyễn Văn A vào lúc 09:00 20/09/2026."}

--- 🔄 Vòng lặp ReAct Loop (Step 3/5) ---
🧠 [Thought]: OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
🏁 [Final Answer]: Sinh viên **SV2026001** có cố vấn là **PGS.TS Nguyễn Văn A**.  

Lịch tư vấn đã được đặt thành công vào **09:00 20/09/2026**. Mã đặt lịch: **BK-SV2026001-99**.

==================================================
🧪 [TC05] Loại test: edge_case_handling (Độ phức tạp: Medium)
📌 Kỳ vọng: Agent nhận NOT_FOUND và không tự tạo dữ liệu sinh viên.

🤖 [REACT AGENT] Câu hỏi: Hãy tra cứu thông tin học vụ của sinh viên SV9999999.

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: OpenAI quyết định gọi công cụ 'academic_query' với tham số: {"student_id": "SV9999999"}
🛠️ [Action Proposed]: academic_query({'student_id': 'SV9999999'})
👁️ [Observation từ MCP Server]: {"status": "NOT_FOUND", "message": "Không tìm thấy dữ liệu sinh viên có mã 'SV9999999'"}

--- 🔄 Vòng lặp ReAct Loop (Step 2/5) ---
🧠 [Thought]: OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
🏁 [Final Answer]: Mã sinh viên SV9999999 không tồn tại trong cơ sở dữ liệu học vụ của VinUni.

==================================================
📊 [KẾT QUẢ TEST SUITE]: Đã thực thi 5/5 Test Cases | 0 Test Cases đang chờ điền câu hỏi (TODO)
📊 [OBSERVABILITY]: Đã lưu 10 sự kiện Waterfall Trace tại 'C:\VIN_AI\LAB_04\K4A-Day03-Lab-Chatbot-vs-ReAct-A-NGUYENVANHUY-2A202602428\docs\trace_waterfall.json'!
💡 Để trò chuyện trực tiếp từng câu: Chạy 'python src/app.py --interactive'
(.venv) PS C:\VIN_AI\LAB_04\K4A-Day03-Lab-Chatbot-vs-ReAct-A-NGUYENVANHUY-2A202602428> import re
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
