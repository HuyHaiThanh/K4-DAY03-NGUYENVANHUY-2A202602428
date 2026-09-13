"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    # Tool 2: Schema cho chức năng đặt lịch hẹn với cố vấn học tập.
    # Mỗi property bên dưới là một tham số mà LLM phải trích xuất từ câu hỏi
    # của người dùng trước khi gọi hàm execute_schedule_appointment().
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
        "parameters": {
            "type": "object",
            "properties": {
                # Mã sinh viên là khóa định danh người cần đặt lịch.
                # Kiểu string vì mã sinh viên có cả chữ và số, ví dụ: SV2026001.
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')"
                },
                # Thời gian hẹn được truyền dưới dạng chuỗi để giữ linh hoạt
                # với nhiều cách nhập ngày giờ khác nhau từ người dùng.
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 15/09/2026')"
                },
                # Tên cố vấn học tập mà sinh viên muốn đặt lịch gặp.
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn học tập"
                }
            },
            # Các trường trong required bắt buộc phải có trước khi tool được gọi.
            # Danh sách này khớp với các tham số chính của execute_schedule_appointment().
            "required": ["student_id", "datetime_str", "advisor_name"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn học vụ"""
    # Chuẩn hóa mã giống hàm tra cứu: bỏ khoảng trắng hai đầu, đổi sang chữ hoa.
    student_id = student_id.strip().upper()
    # Tool tự kiểm tra dữ liệu trước khi đặt lịch, kể cả khi agent gọi trực tiếp.
    # Không bắt buộc agent phải gọi academic_query chỉ để kiểm tra mã tồn tại.
    if student_id not in MOCK_DATABASE:
        # Trả về sớm: không tạo booking_id hay báo thành công cho mã không tồn tại.
        return json.dumps({
            "status": "NOT_FOUND",
            "student_id": student_id,
            "message": f"Không thể đặt lịch: không tìm thấy sinh viên có mã '{student_id}'."
        }, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
