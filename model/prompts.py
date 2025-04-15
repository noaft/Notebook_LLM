from typing import List
import re

class PromptTemplates:
    # System prompt cho chatbot
    SYSTEM_PROMPT = """Bạn là một trợ lý AI thông minh, có khả năng đọc và phân tích tài liệu PDF. 
    Nhiệm vụ của bạn là giúp người dùng tìm kiếm và trả lời các câu hỏi liên quan đến nội dung trong tài liệu.
    Hãy trả lời một cách chính xác, ngắn gọn và dễ hiểu.
    Nếu không tìm thấy thông tin trong tài liệu, hãy nói rõ điều đó."""

    # Prompt cho trò chuyện thông thường
    CHAT_PROMPT = """Bạn là một trợ lý AI thân thiện và hữu ích.
    Hãy trò chuyện với người dùng một cách tự nhiên và thân thiện.
    Câu hỏi của người dùng: {question}
    
    Hãy trả lời một cách ngắn gọn, rõ ràng và hữu ích."""

    # ... existing code ...

    # Các pattern để nhận diện loại câu hỏi
    PATTERNS = {
        "summary": [
            r"tóm tắt",
            r"tóm lược",
            r"tổng hợp",
            r"nội dung chính",
            r"ý chính"
        ],
        "explain": [
            r"giải thích",
            r"nghĩa là gì",
            r"hiểu như thế nào",
            r"định nghĩa"
        ],
        "compare": [
            r"so sánh",
            r"khác nhau",
            r"giống nhau",
            r"đối chiếu"
        ],
        "coding": [
            r"code",
            r"lập trình",
            r"viết chương trình",
            r"thuật toán",
            r"function",
            r"hàm"
        ],
        "creative": [
            r"viết",
            r"sáng tác",
            r"tạo",
            r"nghĩ ra",
            r"đề xuất"
        ],
        "chat": [
            r"chào",
            r"xin chào",
            r"hi",
            r"hello",
            r"bạn khỏe không",
            r"cảm ơn",
            r"tạm biệt",
            r"bye",
            r"goodbye"
        ]
    }

    @staticmethod
    def get_prompt(prompt_type: str, **kwargs) -> str:
        """Lấy prompt template dựa trên loại yêu cầu"""
        templates = {
            "system": PromptTemplates.SYSTEM_PROMPT,
            "document": PromptTemplates.DOCUMENT_PROMPT,
            "search": PromptTemplates.SEARCH_PROMPT,
            "compare": PromptTemplates.COMPARE_PROMPT,
            "summarize": PromptTemplates.SUMMARIZE_PROMPT,
            "explain": PromptTemplates.EXPLAIN_PROMPT,
            "voice": PromptTemplates.VOICE_PROMPT,
            "coding": PromptTemplates.CODING_PROMPT,
            "creative": PromptTemplates.CREATIVE_PROMPT,
            "chat": PromptTemplates.CHAT_PROMPT
        }
        
        if prompt_type not in templates:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
            
        return templates[prompt_type].format(**kwargs) 