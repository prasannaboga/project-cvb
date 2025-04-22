import json

import requests

from project_cvb.config.settings import Settings

settings = Settings()


def main():
  url = "http://localhost:11434/api/generate"

  data = {
      "model": "llama3.2",
      "prompt": "tell me a short story horror and suspense.",
  }

  response = requests.post(
      url, json=data, stream=True
  )

  if response.status_code == 200:
    print("Generated Text:", end=" ", flush=True)
    for line in response.iter_lines():
      if line:
        decoded_line = line.decode("utf-8")
        result = json.loads(decoded_line)
        generated_text = result.get("response", "")
        print(generated_text, end="", flush=True)
  else:
    print("Error:", response.status_code, response.text)


if __name__ == "__main__":
  main()
