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

    def init_index(self, embeddings):
        """
        Save FAISS index to a file
        """
        dimension = embeddings.shape[1]
        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension))
        print(f"FAISS index inited") 

    def save_multil(self, texts, faiss_file="faiss_index.bin"):
        vectors = self.embed_texts(texts) # embbed
        ids = np.array(range(len(texts)))  # create id

        dimension = vectors.shape[1]
        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension)) # init index id map

        self.index.add_with_ids(vectors, ids.astype(np.int64)) # add to index

        faiss.write_index(self.index, faiss_file)

        print(f"FAISS index has been saved to {faiss_file}") 

    def search(self, query, filename="faiss_index.bin", k=1):
        """
        Load FAISS index and search for similar texts
        """
        if self.index is None:
            self.index = faiss.read_index(filename)  # Load FAISS from file
        
        query_embedding = self.embed_texts([query])
        D, I = self.index.search(query_embedding, k)  # Find k nearest results
        return I[0]  # Return indices of matching text passages