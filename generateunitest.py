import os
import openai

# Get the OpenAI API key from a file c
with open("./inputs/inputs.txt", "r") as f:
    inputs = dict(line.strip().split(":") for line in f)
openai_api_key = inputs["openai_api_key"]

# Set up the OpenAI API client
openai.api_key = openai_api_key

# Define the code snippet to generate unit tests for
for filename in os.listdir('./sources'):
    with open(os.path.join('./sources', filename), 'r') as file:
        code_snippet = file.read()

        # Call the OpenAI API to generate unit tests for the code snippet
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate unit tests for this code:\n\n{code_snippet}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Write the generated unit tests to a file
        output_filename = filename + ".unittest"
        with open(os.path.join('./outputs', output_filename), 'w') as output_file:
            output_file.write(response.choices[0].text)
            print(f"Generated unit tests written to {output_filename}")
