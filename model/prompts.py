from typing import List
import re

class PromptTemplates:
    # System prompt cho chatbot
    SYSTEM_PROMPT = """Bạn là một trợ lý AI thông minh, có khả năng đọc và phân tích tài liệu PDF. 
    Nhiệm vụ của bạn là giúp người dùng tìm kiếm và trả lời các câu hỏi liên quan đến nội dung trong tài liệu.
    Hãy trả lời một cách chính xác, ngắn gọn và dễ hiểu.
    Nếu không tìm thấy thông tin trong tài liệu, hãy nói rõ điều đó."""

    # Prompt cho xử lý tài liệu
    DOCUMENT_PROMPT = """Dưới đây là nội dung của tài liệu:
    {document_content}
    
    Hãy phân tích và tóm tắt các thông tin chính trong tài liệu này."""

    # Prompt cho tìm kiếm thông tin
    SEARCH_PROMPT = """Dựa vào nội dung tài liệu sau:
    {document_content}
    
    Hãy trả lời câu hỏi: {question}
    
    Nếu thông tin không có trong tài liệu, hãy trả lời: "Tôi không tìm thấy thông tin này trong tài liệu.""""

    # Prompt cho so sánh tài liệu
    COMPARE_PROMPT = """Dưới đây là nội dung của hai tài liệu:
    
    Tài liệu 1:
    {doc1_content}
    
    Tài liệu 2:
    {doc2_content}
    
    Hãy so sánh và chỉ ra những điểm giống và khác nhau giữa hai tài liệu."""

    # Prompt cho tóm tắt tài liệu
    SUMMARIZE_PROMPT = """Hãy tóm tắt nội dung chính của tài liệu sau:
    {document_content}
    
    Tóm tắt cần ngắn gọn, súc tích và bao quát được các ý chính."""

    # Prompt cho giải thích thuật ngữ
    EXPLAIN_PROMPT = """Trong tài liệu có đề cập đến thuật ngữ: {term}
    
    Hãy giải thích ý nghĩa của thuật ngữ này dựa trên ngữ cảnh trong tài liệu."""

    # Prompt cho voice input
    VOICE_PROMPT = """Bạn vừa nghe được câu hỏi từ người dùng qua giọng nói:
    {voice_input}
    
    Hãy phân tích và trả lời câu hỏi này dựa trên nội dung tài liệu:
    {document_content}"""

    # Prompt cho lập trình
    CODING_PROMPT = """Bạn là một trợ lý lập trình thông minh.
    Dựa vào nội dung tài liệu:
    {document_content}
    
    Hãy trả lời câu hỏi về lập trình: {question}
    
    Nếu cần, hãy cung cấp code mẫu và giải thích chi tiết."""

    # Prompt cho sáng tạo nội dung
    CREATIVE_PROMPT = """Bạn là một trợ lý sáng tạo.
    Dựa vào nội dung tài liệu:
    {document_content}
    
    Hãy tạo nội dung sáng tạo theo yêu cầu: {question}"""

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
        ]
    }

    @staticmethod
    def detect_prompt_type(question: str) -> str:
        """Phát hiện loại prompt dựa trên nội dung câu hỏi"""
        question = question.lower().strip()
        
        for prompt_type, patterns in PromptTemplates.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, question):
                    return prompt_type
                    
        return "search"  # Mặc định là prompt tìm kiếm

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
            "creative": PromptTemplates.CREATIVE_PROMPT
        }
        
        if prompt_type not in templates:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
            
        return templates[prompt_type].format(**kwargs) 