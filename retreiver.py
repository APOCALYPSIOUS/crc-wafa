from langchain_core.vectorstores import VectorStore
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SimpleField, SearchFieldDataType, SearchIndex, VectorField, VectorSearchAlgorithmConfiguration
)

class AzureSearchVectorStore(VectorStore):
    def __init__(self, search_endpoint: str, api_key: str, index_name: str, vector_dim: int):
        self.index_name = index_name
        self.vector_dim = vector_dim
        self.search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=api_key)
        self.index_client = SearchIndexClient(endpoint=search_endpoint, credential=api_key)
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        """Ensure the search index with vector capabilities is created."""
        try:
            self.index_client.get_index(self.index_name)
        except:
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                VectorField(name="vector", vector_dim=self.vector_dim, algorithm_config=VectorSearchAlgorithmConfiguration(name="hnsw"))
            ]
            index = SearchIndex(name=self.index_name, fields=fields)
            self.index_client.create_index(index)

    def add_texts(self, texts, embeddings, ids):
        """Add texts with their embeddings to the Azure AI Search index."""
        documents = [
            {"id": str(id_), "vector": embedding}
            for id_, embedding in zip(ids, embeddings)
        ]
        self.search_client.upload_documents(documents)

    def similarity_search(self, query_embedding, top_k=5):
        """Perform a similarity search on the vector store."""
        results = self.search_client.search(
            search_text="*",
            vector={"value": query_embedding, "fields": "vector"},
            top=top_k
        )
        return [result for result in results]

    def delete(self, ids):
        """Delete entries from the vector store by their IDs."""
        self.search_client.delete_documents(documents=[{"id": id_} for id_ in ids])

# Usage example
search_endpoint = "https://<your-search-instance>.search.windows.net"
api_key = "<your-api-key>"
index_name = "vectorstore"
vector_dim = 768  # Adjust based on your embedding size

azure_vector_store = AzureSearchVectorStore(
    search_endpoint=search_endpoint,
    api_key=api_key,
    index_name=index_name,
    vector_dim=vector_dim
)

# Adding texts and embeddings
texts = ["Example text 1", "Example text 2"]
embeddings = [[0.1, 0.2, 0.3, ...], [0.4, 0.5, 0.6, ...]]  # Replace with your embeddings
ids = ["1", "2"]
azure_vector_store.add_texts(texts, embeddings, ids)

# Performing a similarity search
query_embedding = [0.15, 0.25, 0.35, ...]  # Replace with your query embedding
results = azure_vector_store.similarity_search(query_embedding, top_k=3)
print(results)
