from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from AzureAiSearch import AzureAiSearch
from prompt import wafa_assurance_prompt


def perform_query_and_get_response(
        user_query,
        deployment_name="gpt-4o",
        k_nearest_neighbors=50,
        fields="text_vector",
        top_results=20):
    """
    Perform a vector-based search query on Azure Cognitive Search and get a response from Azure OpenAI.

    Args:
        user_query (str): The query text to search and process.
        deployment_name (str): The name of the OpenAI model deployment.
        k_nearest_neighbors (int): Number of nearest neighbors to consider for the vector query.
        fields (str): The vector fields to use for search.
        top_results (int): The maximum number of search results to return.

    Returns:
        str: The response from the OpenAI model.
        :param fields:
        :param chat_history:
    """
    load_dotenv()

    # Load environment variables
    endpoint = os.getenv("ENDPOINT_URL")
    search_endpoint = os.getenv("SEARCH_ENDPOINT")
    search_key = os.getenv("SEARCH_KEY")
    search_index = os.getenv("SEARCH_INDEX_NAME")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

    # Initialize clients
    openai_client = AzureOpenAI(
        api_version="2024-06-01",
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    search_client = AzureAiSearch(search_endpoint, search_index, search_key)
    sources_formatted = search_client.semantic_search(user_query, k_nearest_neighbors, top_results=top_results)

    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": wafa_assurance_prompt,
            },
            {
                "role": "user",
                "content": f"question: {user_query}\nsources: {sources_formatted}"
            }
        ],
        model=deployment_name,
    )

    return response.choices[0].message.content
