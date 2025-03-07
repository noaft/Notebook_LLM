from sentence_transformers import SentenceTransformer

class model:

    def __init__(self, model_name = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Init model from sqntence transfomer
        Args: 
            model_name (text): name of model from setence
        """
        self.model = SentenceTransformer(model_name)

    def embedding_text(self, sentences):
        """
        Embedding text to vector and matrix
        Args:
            Sentences (list): list of sentences want to embed
        Return:
            List of vector embedded
        """
        embeddings = model.encode(sentences)
        return embeddings