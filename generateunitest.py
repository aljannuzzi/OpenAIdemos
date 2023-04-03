import os
import openai

# Get the OpenAI API key from a file
with open("./inputs/inputs.txt", "r") as f:
    inputs = dict(line.strip().split(":") for line in f)
openai_api_key = inputs["openai_api_key"]

# Set up the OpenAI API client
openai.api_key = openai_api_key

# Define the code snippet to generate unit tests for
code_snippet = """
def add(a, b):
    return a + b
"""

# Call the OpenAI API to generate unit tests for the code snippet
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Generate unit tests for this Python code:\n\n{code_snippet}",
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

# Print the generated unit tests
print(response.choices[0].text)
