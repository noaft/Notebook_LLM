import faiss
import numpy as np
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer

class PDFEmbeddingFAISS:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding model from SentenceTransformer
        """
        self.model = SentenceTransformer(model_name)
        self.index = None  # FAISS Index
    
    def read_pdf(self, pdf_file):
        """
        Read a PDF file and extract text page by page
        """
        loader = PyPDFLoader(pdf_file)
        pages = loader.load()
        return [page.page_content for page in pages]  # Return a list of text passages

    def embed_texts(self, texts):
        """
        Convert a list of texts into embeddings
        """
        return self.model.encode(texts, convert_to_numpy=True)

    def save_data(self, embeddings, filename="faiss_index.bin"):
        """
        Save FAISS index to a file
        """
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        faiss.write_index(self.index, filename)
        print(f"FAISS index has been saved to {filename}") 

    def save_multil(self, embeddings, filename="faiss_index.bin"):
        dimension = embeddings[0].shape[0]
        print(dimension)
        self.index = faiss.IndexFlatL2(dimension) # init index

        for embedding in embeddings:
            self.index.add(embedding.reshape(1, -1))

        faiss.write_index(self.index, filename)
        print(f"FAISS index has been saved to {filename}") 

    def load_data(self, query, filename="faiss_index.bin", k=1):
        """
        Load FAISS index and search for similar texts
        """
        if self.index is None:
            self.index = faiss.read_index(filename)  # Load FAISS from file
        
        query_embedding = self.embed_texts([query])
        D, I = self.index.search(query_embedding, k)  # Find k nearest results
        return I[0]  # Return indices of matching text passages