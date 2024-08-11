from project_cvb.config.settings import Settings, CustomSettings
import google.generativeai as genai

settings = Settings()
custom_settings = CustomSettings() 
print(custom_settings.model_dump())

genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel("gemini-pro")


def hello_world(user_input):
  model = genai.GenerativeModel("gemini-pro")
  prompt = "Tell a joke in two lines"
  response = model.generate_content(prompt)
  return response.text


def main():
  welcome_message = f"""
  ************************************************************
  Chat with the Hello World model!
  ENV[{settings.environment}]
  Type 'exit' to quit.
  ************************************************************
  """
  print(welcome_message)

  while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
      break
    # response = hello_world(user_input)
    print(f"AI: {user_input}")


if __name__ == "__main__":
  main()
