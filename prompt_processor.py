import requests
import json
import os
from config import MODEL, TEMPERATURE, MODEL_API_URL # Import model, temperature, and API URL

class PromptProcessor:
    def __init__(self, output_folder):
        self.model = MODEL # Use the model from config.py
        self.temperature = TEMPERATURE # Use the temperature from config.py
        self.messages = []
        self.output_folder = output_folder

    def load_prompts_from_json(self, json_file):
        """Load prompts from a JSON file."""
        with open(json_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
            self.messages = config['messages']  # Load the messages

    def process_messages(self, content, file_name):
        """Send messages to the model and get the response."""
        messages = self._format_messages(content)

        payload = {
            "model": self.model,
            "messages": messages,
            "options": {
                "temperature": self.temperature,
                "keep_alive": "1h"
            },
            "stream": True
        }

        response = requests.post(MODEL_API_URL, json=payload, stream=True)
        final_response = self._get_response_content(response)

        self._save_response(file_name, final_response)
        return final_response

    def _format_messages(self, content):
        """Format messages with the provided content."""
        return [
            {
                "role": message['role'],
                "content": "\n".join([part['text'] for part in message['content']]).format(content=content)
            }
            for message in self.messages
        ]

    def _get_response_content(self, response):
        """Extract the content from the model's response."""
        final_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                if 'message' in data and 'content' in data['message']:
                    print(data['message']['content'], end='', flush=True)
                    final_response += data['message']['content']
        return final_response

    def _save_response(self, file_name, content):
        """Save the model's response to a file."""
        output_path = os.path.join(self.output_folder, file_name) # Use the relative path directly
        output_path = os.path.splitext(output_path)[0] + ".md"  # Ensure .md extension
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(content)

    def run(self, initial_content, file_name):
        """Run the processor with the initial content and file name."""
        print(f"\n********************* Thinking...\n")
        return self.process_messages(initial_content, file_name)