from langchain_community.document_loaders import PyPDFLoader
from langchain_google_vertexai import VertexAIEmbeddings


class PDFEmbeddingFAISS:
    def __init__(self, model_name="text-embedding-004", dims = 1536):
        """
        Initialize the embedding model from SentenceTransformer
        """
        self.embeddings_model = VertexAIEmbeddings(model=model_name)
        self.dims = dims

    def read_pdf(self, pdf_file):
        """
        Read a PDF file and extract text page by page
        """
        self.loader = PyPDFLoader(pdf_file)
        self.pages = self.loader.load_and_split()

    def embed_texts(self, texts):
        """
        Convert a list of texts into embeddings
        """

    def init_index(self, embeddings):
        """
        Save FAISS index to a file
        """

    def save_multil(self,name_file, texts):
        """
        Save multiple texts to a FAISS index
        """

    def search(self, query, filenames, k=1):
        """
        Load FAISS index and search for similar texts
        """
    
    def get_text(self, id, text_file ):
        pass