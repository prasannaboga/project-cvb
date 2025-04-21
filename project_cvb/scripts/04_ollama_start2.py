import json

import ollama
import requests

from project_cvb.config.settings import Settings

settings = Settings()


def main():
  # response = ollama.list()
  # # print(response)

  # response = ollama.chat(
  #   model="llama3.2",
  #   messages=[
  #       {"role": "user", "content": "what is difference with football and cricket?"},
  #   ]
  # )
  # print(response["message"]["content"])

  # Create a new model with modelfile
  modelfile = """
  FROM llama3.2
  SYSTEM You are very smart assistant who knows everything about oceans. You are very succinct and informative.
  PARAMETER temperature 0.1
  """

  # ollama.create(model="knowitall")

  # response = ollama.generate(model="knowitall", prompt="why is the ocean so salty?")
  # print(response["response"])


if __name__ == "__main__":
  main()
