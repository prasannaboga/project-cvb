import argparse
import json

import requests
from ollama import Client

from project_cvb.config.settings import Settings

settings = Settings()


def main():
  print("Sentiment Analysis\n")

  parser = argparse.ArgumentParser(description="Perform sentiment analysis on input text.")
  parser.add_argument("input_txt", type=str, help="The text to analyze sentiment for.")

  args = parser.parse_args()
  input_txt = args.input_txt

  print(f"Input text: {input_txt}\n")

  client = Client(host='http://localhost:11434')
  prompt = f"Classify the sentiment of this text as positive, negative, or neutral: {input_txt}. Just response only in one word, no need explaination."
  response = client.generate(model='llama3.2', prompt=prompt)
  print(f"Generated Text: {response["response"]}")


if __name__ == "__main__":
  main()
