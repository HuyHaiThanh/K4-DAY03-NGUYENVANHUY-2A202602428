# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Văn Huy
>
> **Mã Sinh Viên / Mã Học viên:** 2A202602428
>
> **Chủ đề Lựa chọn:** Trợ lý Học vụ Sinh viên VinUni

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5 / 5 | TC04 phải tra cứu hồ sơ để tìm cố vấn, lấy kết quả làm đầu vào cho bước đặt lịch rồi mới tổng hợp câu trả lời. |
| **2. Tool Interaction** | 5 / 5 | Agent dùng `academic_query` để đọc dữ liệu học vụ và `schedule_appointment` để thực hiện đặt lịch qua MCP Server. |
| **3. Dynamic Decision** | 5 / 5 | Agent chọn trả lời trực tiếp hoặc gọi Tool; bước đặt lịch trong TC04 phụ thuộc vào tên cố vấn từ Observation trước đó. |
| **4. Long Horizon Goal** | 3 / 5 | Agent giữ mục tiêu qua nhiều vòng Thought–Action–Observation, nhưng tác vụ chỉ kéo dài vài bước và chưa cần bộ nhớ dài hạn. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | Bài toán đạt trên 12/20 và phù hợp triển khai Agentic System. |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

Đã chạy `python src/app.py --all` bằng API thật qua NVIDIA OpenAI-compatible endpoint, model `openai/gpt-oss-20b`. Đoạn dưới trích TC04 vì thể hiện đầy đủ chuỗi tra cứu cố vấn rồi đặt lịch:

```json
[
  {
    "step": 1,
    "query": "Tra cứu cố vấn của sinh viên SV2026001, sau đó đặt lịch tư vấn vào 09:00 20/09/2026 với cố vấn đó.",
    "action_type": "TOOL_EXECUTION",
    "thought": "OpenAI quyết định gọi công cụ 'academic_query' với tham số student_id=SV2026001.",
    "tool_name": "academic_query",
    "arguments": {
      "student_id": "SV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026001",
      "data": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "advisor": "PGS.TS Nguyễn Văn A"
      }
    },
    "latency_ms": 6568.29
  },
  {
    "step": 2,
    "query": "Tra cứu cố vấn của sinh viên SV2026001, sau đó đặt lịch tư vấn vào 09:00 20/09/2026 với cố vấn đó.",
    "action_type": "TOOL_EXECUTION",
    "thought": "OpenAI quyết định gọi công cụ 'schedule_appointment' với đầy đủ tham số.",
    "tool_name": "schedule_appointment",
    "arguments": {
      "student_id": "SV2026001",
      "datetime_str": "09:00 20/09/2026",
      "advisor_name": "PGS.TS Nguyễn Văn A"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-SV2026001-99",
      "student_id": "SV2026001",
      "datetime": "09:00 20/09/2026",
      "advisor": "PGS.TS Nguyễn Văn A"
    },
    "latency_ms": 4581.41
  },
  {
    "step": 3,
    "query": "Tra cứu cố vấn của sinh viên SV2026001, sau đó đặt lịch tư vấn vào 09:00 20/09/2026 với cố vấn đó.",
    "action_type": "FINAL_ANSWER",
    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Sinh viên SV2026001 có cố vấn là PGS.TS Nguyễn Văn A. Lịch tư vấn đã được đặt thành công vào 09:00 20/09/2026. Mã đặt lịch: BK-SV2026001-99.",
    "latency_ms": 5830.85
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã cấu hình API Key thật và xác nhận Agent chạy bằng NVIDIA OpenAI-compatible API, không fallback về Mock.
- **Model nghiệm thu:** `openai/gpt-oss-20b`.
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt (`academic_query`: 3, `schedule_appointment`: 2).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
