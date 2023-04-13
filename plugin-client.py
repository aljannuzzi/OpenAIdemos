import requests
import json
import sys


def read_api_key(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

api_key_file_path = "api_key.txt"  # Replace with the path to your API key text file
chatgpt_api_key = read_api_key(api_key_file_path)

plugin_server_base_url = "http://<URL>:3333"  # Replace with your plugin server's base URL

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {chatgpt_api_key}",
}

chatgpt_url = "https://api.openai.com/v1/engines/text-davinci-003/completions"


def chatgpt_query(prompt):
    payload = {
        "prompt": prompt,
        "max_tokens": 1500,
        "temperature": 0.7,
        "top_p": 1,
#        "frequency_penalty": 0,
#        "presence_penalty": 0,
    }

    response = requests.post(chatgpt_url, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["text"].strip()
    else:
        print(f"An error occurred while calling ChatGPT API: {response.status_code}")
        print(f"Response content: {response.content}")
        return ""


def plugin_query(plugin_query_text):
    try:
        url = "http://<URL>:3333/query"
        payload = {
            "queries": [
                {
                    "query": plugin_query_text,
                    "top_k": 3
                }
            ]
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        results = response.json()["results"][0]["results"]

        # Find the highest scored result
        highest_score = -1
        highest_score_text = ""
        for result in results:
            if result["score"] > highest_score:
                highest_score = result["score"]
                highest_score_text = result["text"]

        return highest_score_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def chatgpt_with_plugin(plugin_query_text):
    triggers = ["Dev Squad", "CSU"]

    if any(trigger in plugin_query_text for trigger in triggers):
        plugin_response = plugin_query(plugin_query_text)
        prompt = f"Considering this text as an answer: {plugin_response} How could you provide a human-like response for this question: {plugin_query_text}"
        chatgpt_response = chatgpt_query(prompt)
    else:
        chatgpt_response = chatgpt_query(plugin_query_text)

    return chatgpt_response


if __name__ == "__main__":
    input_text = sys.stdin.read().strip()
    response = chatgpt_with_plugin(input_text)
    print(response)

