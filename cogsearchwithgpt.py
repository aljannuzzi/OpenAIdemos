#!/usr/bin/python3.8

import requests
import json
import sys
import uuid

def read_api_key(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

api_key_file_path = "api_key.txt.azure"  # Replace with the path to your API key text file
chatgpt_api_key = read_api_key(api_key_file_path)
azure_search_api_key = read_api_key("azure_search_key.txt")  # Replace with the path to your Azure Search API key text file

azure_search_service_name = "<name>"  # Replace with your Azure Cognitive Search service name

headers = {
    "Content-Type": "application/json",
    "api-key": chatgpt_api_key,
}

chatgpt_url = "https://<URL>"

def chatgpt_query(prompt):
    payload = {
#        "engine": "jann-gpt4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.8,
        "top_p": 1,
        "stop": None,
#        "frequency_penalty": 0,
#        "presence_penalty": 0,
    }

    response = requests.post(chatgpt_url, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()
    else:
        print(f"An error occurred while calling ChatGPT API: {response.status_code}")
        print(f"Response content: {response.content}")
        return ""

def azure_search_query(search_query_text):
    try:
        url = f"https://{azure_search_service_name}.search.windows.net/indexes/janndata-index/docs/search?api-version=2021-04-30-Preview"
        payload = {
            "search": search_query_text,
            "top": 3,
        }

        headers = {"api-key": azure_search_api_key, "Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        results = response.json()["value"]

        # Find the highest scored result
        highest_score = -1
        highest_score_text = ""
        for result in results:
            if result["@search.score"] > highest_score:
                highest_score = result["@search.score"]
                highest_score_text = result["content"]

        return highest_score_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# The upsert function may not be required for Azure Cognitive Search as indexing can be managed separately
def chatgpt_with_azure_search(search_query_text):
    triggers = ["Dev Squad", "CSU"]

    if any(trigger in search_query_text for trigger in triggers):
        search_response = azure_search_query(search_query_text)
        prompt = f"Using the following text from an Azure Cognitive Search query: '{search_response}', please generate a well-informed and human-like answer for the question: '{search_query_text}'. If demanded in the question, use your knowledge based on previous training to create an analysis or make a comparizon"
        chatgpt_response = chatgpt_query(prompt)
    else:
        chatgpt_response = chatgpt_query(search_query_text)

    return chatgpt_response

if __name__ == "__main__":
    input_text = sys.stdin.read().strip()
    response = chatgpt_with_azure_search(input_text)
    print(response)

