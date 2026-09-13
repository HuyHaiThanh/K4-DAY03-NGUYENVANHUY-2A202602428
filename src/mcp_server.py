"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        reconfigure = getattr(sys.stdout, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPAcademicServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol
    """
    def __init__(self, server_name: str = "vinuni-academic-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Nhận yêu cầu gọi tool và đóng gói kết quả trả về cho ứng dụng.

        tool_name: Tên tool đã khai báo trong schema, ví dụ "academic_query".
        arguments: Dictionary chứa tham số, ví dụ {"student_id": "SV2026001"}.
        Giá trị trả về là dictionary Python; ứng dụng có thể chuyển thành JSON.
        """
        # Bước 1: Nhờ hàm điều phối trong tools.py tìm hàm tương ứng qua TOOL_ROUTER.
        # Hàm điều phối dùng **arguments để tách dictionary thành tham số có tên:
        # {"student_id": "SV2026001"} -> execute_academic_query(student_id="SV2026001").
        # Kết quả nhận được là CHUỖI JSON, kể cả khi router báo UNKNOWN_TOOL
        # (không có tên tool) hoặc EXECUTION_ERROR (lỗi khi thực thi hàm).
        result_json = dispatch_tool_call(tool_name, arguments)

        # Bước 2: Chuyển chuỗi JSON thành dữ liệu Python để lồng vào phản hồi.
        # Ví dụ: '{"status": "SUCCESS"}' -> {"status": "SUCCESS"}.
        # json.loads chỉ giải mã JSON, không kiểm tra arguments theo tool schema.
        # Nếu result_json không hợp lệ, lỗi giải mã sẽ truyền ra nơi gọi call_tool.
        content = json.loads(result_json)

        # Bước 3: Đóng gói phản hồi theo cấu trúc mô phỏng dùng trong bài lab.
        # Đây chưa phải phản hồi JSON-RPC/MCP đầy đủ (ví dụ chưa có request id).
        return {
            # Nhãn phiên bản giao thức mà bài lab mô phỏng.
            "jsonrpc": "2.0",
            # Tên server xử lý yêu cầu, lấy từ lúc khởi tạo đối tượng.
            "server": self.server_name,
            # Tên tool vừa được yêu cầu thực thi.
            "tool": tool_name,
            # Dữ liệu đã giải mã, gồm kết quả thành công hoặc thông tin lỗi từ router.
            "result": content
        }


if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (vinuni-academic-mcp-server)")
    print("==========================================================")
    
    server = MCPAcademicServer()
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố: {len(tools)}")
    
    # Kiểm tra trạng thái TODO 1.2 (Tool Schema)
    sched_tool = next((t for t in tools if t.get("name") == "schedule_appointment"), None)
    if sched_tool and not sched_tool.get("parameters", {}).get("properties"):
        print("⏳ [TODO 1.2]: Tool 'schedule_appointment' chưa được định nghĩa properties trong 'src/tools.py'.")
    else:
        print("✅ [TODO 1.2]: Tool 'schedule_appointment' đã có schema đầy đủ.")

    # Kiểm tra trạng thái TODO 2.1 (call_tool)
    test_result = server.call_tool("academic_query", {"student_id": "SV2026001"})
    if not test_result:
        print("⏳ [TODO 2.1]: Hàm call_tool() đang trả về rỗng. Học viên hãy hoàn thiện TODO 2.1 trong 'src/mcp_server.py'!")
    else:
        print(f"✅ [TODO 2.1]: Test dispatch tool 'academic_query' thành công:")
        print(f"   Phản hồi JSON-RPC: {json.dumps(test_result, ensure_ascii=False)}")
