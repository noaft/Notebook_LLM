from typing import List, Dict, Any, Optional
import re
from enum import Enum

class PromptType(Enum):
    SYSTEM = "system"
    CHAT = "chat"
    DOCUMENT = "document"
    SEARCH = "search"
    COMPARE = "compare"
    SUMMARIZE = "summarize"
    EXPLAIN = "explain"
    VOICE = "voice"
    CODING = "coding"
    CREATIVE = "creative"
    TRANSLATE = "translate"
    ANALYZE = "analyze"
    CLASSIFY = "classify"
    GENERATE = "generate"
    QA = "qa"
    MATH = "math"
    DEFAULT = "default"

class PromptTemplates:
    # System prompts
    SYSTEM_PROMPTS = {
        "default": """Bạn là một trợ lý AI thông minh, có khả năng đọc và phân tích tài liệu PDF. 
        Nhiệm vụ của bạn là giúp người dùng tìm kiếm và trả lời các câu hỏi liên quan đến nội dung trong tài liệu.
        Hãy trả lời một cách chính xác, ngắn gọn và dễ hiểu.
        Nếu không tìm thấy thông tin trong tài liệu, hãy nói rõ điều đó.""",
        
        "expert": """Bạn là một chuyên gia trong lĩnh vực của tài liệu. 
        Hãy sử dụng kiến thức chuyên môn để phân tích và trả lời các câu hỏi.
        Đảm bảo độ chính xác và tính chuyên môn trong câu trả lời.""",
        
        "friendly": """Bạn là một trợ lý AI thân thiện và hữu ích.
        Hãy giao tiếp với người dùng một cách tự nhiên, thân thiện và dễ hiểu.
        Sử dụng ngôn ngữ đơn giản và gần gũi."""
    }

    # Prompt templates
    TEMPLATES = {
        PromptType.CHAT.value: """Bạn là một trợ lý AI thân thiện và hữu ích.
        Hãy trò chuyện với người dùng một cách tự nhiên và thân thiện.
        Câu hỏi của người dùng: {question}
        
        Hãy trả lời một cách ngắn gọn, rõ ràng và hữu ích.""",

        PromptType.DOCUMENT.value: """Dưới đây là nội dung của tài liệu:
        {document_content}
        
        Hãy phân tích và tóm tắt các thông tin chính trong tài liệu này.
        Chú ý đến các điểm quan trọng và mối quan hệ giữa các thông tin.""",

        PromptType.SEARCH.value: """Dựa vào nội dung tài liệu sau:
        {document_content}
        
        Hãy trả lời câu hỏi: {question}
        
        Yêu cầu:
        1. Trả lời chính xác và đầy đủ
        2. Nếu thông tin không có trong tài liệu, hãy trả lời: `Tôi không tìm thấy thông tin này trong tài liệu.`
        3. Có thể tham khảo thêm kiến thức bên ngoài nếu cần thiết""",

        PromptType.COMPARE.value: """Dưới đây là nội dung của hai tài liệu:
        
        Tài liệu 1:
        {doc1_content}
        
        Tài liệu 2:
        {doc2_content}
        
        Hãy so sánh và chỉ ra:
        1. Những điểm giống nhau
        2. Những điểm khác nhau
        3. Đánh giá ưu nhược điểm của mỗi tài liệu
        4. Kết luận và đề xuất""",

        PromptType.SUMMARIZE.value: """Hãy tóm tắt nội dung chính của tài liệu sau:
        {document_content}
        
        Yêu cầu tóm tắt:
        1. Ngắn gọn, súc tích
        2. Bao quát được các ý chính
        3. Giữ được thông tin quan trọng
        4. Có thể chia thành các phần nhỏ nếu cần""",

        PromptType.EXPLAIN.value: """Trong tài liệu có đề cập đến thuật ngữ: {term}
        
        Hãy giải thích:
        1. Ý nghĩa của thuật ngữ này
        2. Ngữ cảnh sử dụng trong tài liệu
        3. Ví dụ minh họa (nếu có)
        4. Các thuật ngữ liên quan""",

        PromptType.VOICE.value: """Bạn vừa nghe được câu hỏi từ người dùng qua giọng nói:
        {voice_input}
        
        Hãy phân tích và trả lời câu hỏi này dựa trên nội dung tài liệu:
        {document_content}
        
        Lưu ý: Có thể cần xử lý lỗi nghe nhầm hoặc thiếu thông tin trong câu hỏi.""",

        PromptType.CODING.value: """Bạn là một trợ lý lập trình thông minh.
        Dựa vào nội dung tài liệu:
        {document_content}
        
        Hãy trả lời câu hỏi về lập trình: {question}
        
        Yêu cầu:
        1. Cung cấp code mẫu nếu cần
        2. Giải thích chi tiết cách hoạt động
        3. Đề xuất các phương án tối ưu
        4. Cảnh báo về các vấn đề có thể gặp phải""",

        PromptType.CREATIVE.value: """Bạn là một trợ lý sáng tạo.
        Dựa vào nội dung tài liệu:
        {document_content}
        
        Hãy tạo nội dung sáng tạo theo yêu cầu: {question}
        
        Yêu cầu:
        1. Sáng tạo và độc đáo
        2. Phù hợp với ngữ cảnh
        3. Có tính thực tế
        4. Dễ hiểu và hấp dẫn""",

        PromptType.TRANSLATE.value: """Hãy dịch nội dung sau từ {source_lang} sang {target_lang}:
        {content}
        
        Yêu cầu:
        1. Dịch chính xác và tự nhiên
        2. Giữ nguyên ý nghĩa gốc
        3. Phù hợp với văn phong của ngôn ngữ đích
        4. Giải thích các thuật ngữ đặc biệt nếu cần""",

        PromptType.ANALYZE.value: """Hãy phân tích nội dung sau:
        {content}
        
        Yêu cầu phân tích:
        1. Phân tích cấu trúc và tổ chức
        2. Đánh giá nội dung chính
        3. Chỉ ra các điểm mạnh và điểm yếu
        4. Đề xuất cải tiến nếu có""",

        PromptType.CLASSIFY.value: """Hãy phân loại nội dung sau:
        {content}
        
        Yêu cầu:
        1. Xác định thể loại/chủ đề chính
        2. Phân loại thành các nhóm nhỏ
        3. Giải thích tiêu chí phân loại
        4. Đề xuất các nhãn phù hợp""",

        PromptType.GENERATE.value: """Hãy tạo nội dung theo yêu cầu:
        {requirements}
        
        Yêu cầu:
        1. Sáng tạo và độc đáo
        2. Phù hợp với mục đích sử dụng
        3. Có cấu trúc rõ ràng
        4. Dễ hiểu và hấp dẫn""",

        PromptType.QA.value: """Hãy trả lời câu hỏi sau:
        {question}
        
        Yêu cầu:
        1. Trả lời chính xác và đầy đủ
        2. Cung cấp bằng chứng hoặc ví dụ
        3. Giải thích rõ ràng
        4. Đề xuất thêm thông tin liên quan""",

        PromptType.MATH.value: """Hãy giải quyết bài toán sau:
        {problem}
        
        Yêu cầu:
        1. Trình bày lời giải chi tiết
        2. Giải thích từng bước
        3. Kiểm tra kết quả
        4. Đề xuất cách giải khác nếu có"""
    }

    # Các pattern để nhận diện loại câu hỏi
    PATTERNS = {
        PromptType.SUMMARIZE.value: [
            r"tóm tắt",
            r"tóm lược",
            r"tổng hợp",
            r"nội dung chính",
            r"ý chính",
            r"summary",
            r"summarize"
        ],
        PromptType.EXPLAIN.value: [
            r"giải thích",
            r"nghĩa là gì",
            r"hiểu như thế nào",
            r"định nghĩa",
            r"explain",
            r"define",
            r"meaning"
        ],
        PromptType.COMPARE.value: [
            r"so sánh",
            r"khác nhau",
            r"giống nhau",
            r"đối chiếu",
            r"compare",
            r"difference",
            r"similar"
        ],
        PromptType.CODING.value: [
            r"code",
            r"lập trình",
            r"viết chương trình",
            r"thuật toán",
            r"function",
            r"hàm",
            r"program",
            r"algorithm"
        ],
        PromptType.CREATIVE.value: [
            r"viết",
            r"sáng tác",
            r"tạo",
            r"nghĩ ra",
            r"đề xuất",
            r"write",
            r"create",
            r"generate"
        ],
        PromptType.CHAT.value: [
            r"chào",
            r"xin chào",
            r"hi",
            r"hello",
            r"bạn khỏe không",
            r"cảm ơn",
            r"tạm biệt",
            r"bye",
            r"goodbye",
            r"thanks",
            r"thank you"
        ],
        PromptType.TRANSLATE.value: [
            r"dịch",
            r"translate",
            r"chuyển ngữ",
            r"convert language"
        ],
        PromptType.ANALYZE.value: [
            r"phân tích",
            r"đánh giá",
            r"analyze",
            r"evaluate",
            r"review"
        ],
        PromptType.CLASSIFY.value: [
            r"phân loại",
            r"nhóm",
            r"classify",
            r"categorize",
            r"group"
        ],
        PromptType.MATH.value: [
            r"tính toán",
            r"giải",
            r"toán",
            r"math",
            r"calculate",
            r"solve"
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
                    
        return PromptType.SEARCH.value  # Mặc định là prompt tìm kiếm

    @staticmethod
    def get_prompt(prompt_type: str, system_prompt: str = "default", **kwargs) -> str:
        """Lấy prompt template dựa trên loại yêu cầu"""
        if prompt_type not in PromptTemplates.TEMPLATES:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
            
        if system_prompt not in PromptTemplates.SYSTEM_PROMPTS:
            raise ValueError(f"Unknown system prompt: {system_prompt}")
            
        # Kết hợp system prompt và template
        full_prompt = f"{PromptTemplates.SYSTEM_PROMPTS[system_prompt]}\n\n"
        full_prompt += PromptTemplates.TEMPLATES[prompt_type]
        
        return full_prompt.format(**kwargs)

    @staticmethod
    def get_available_prompt_types() -> List[str]:
        """Lấy danh sách các loại prompt có sẵn"""
        return list(PromptTemplates.TEMPLATES.keys())

    @staticmethod
    def get_available_system_prompts() -> List[str]:
        """Lấy danh sách các system prompt có sẵn"""
        return list(PromptTemplates.SYSTEM_PROMPTS.keys()) 