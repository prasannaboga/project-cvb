import google.generativeai as genai

from project_cvb.config.settings import Settings

settings = Settings()


genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def add(a: float, b: float):
  return a + b


def subtract(a: float, b: float):
  return (a - b)


def multiply(a: float, b: float):
  return a * b


def divide(a: float, b: float):
  return a / b


math_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", tools=[add, subtract, multiply, divide]
)


def basic_function_calling(prompt):
  chat = math_model.start_chat(enable_automatic_function_calling=True)
  response = chat.send_message(prompt)
  print("*** ***")
  for content in chat.history:
    print(content.role, "->", [type(part).to_dict(part)
          for part in content.parts])
    print("-" * 80)
  return response


def main():
  welcome_message = f"### - {__file__}"
  print(welcome_message)

  while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
      break
    response = basic_function_calling(user_input)
    print(f"AI: {response.text}")


if __name__ == "__main__":
  main()
