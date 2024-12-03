import os

from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents._generated.models import VectorizableTextQuery
from utils import extract_page_number
from dotenv import load_dotenv

load_dotenv()


class AzureAiSearch:
    def __init__(self, search_endpoint, search_index, search_key):
        self.index = search_index
        self.search_key = search_key
        self.credential = AzureKeyCredential(search_key)
        self.client = SearchClient(
            endpoint=search_endpoint,
            index_name=search_index,
            credential=AzureKeyCredential(search_key),
        )

    def semantic_search(self, query, k_nearest_neighbors, top_results=10):
        vector_query = VectorizableTextQuery(
            text=query,
            k_nearest_neighbors=k_nearest_neighbors,
            fields="text_vector",
        )
        search_results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            select=["title", "chunk", "chunk_id"],
            top=top_results,

        )
        print(search_results.get_answers())


        sources_formatted = "=================\n".join(
            [f',PDF_link: {"https://wafacrcdocument.blob.core.windows.net/wafadocumentcontainer/" + document["title"]+"#page="+ str(extract_page_number(document["chunk_id"]))}, CONTENT: {document["chunk"]}' for document in search_results])
        return sources_formatted
