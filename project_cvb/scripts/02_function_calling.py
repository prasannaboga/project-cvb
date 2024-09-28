import google.generativeai as genai

from project_cvb.config.settings import Settings

settings = Settings()


genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


# Sample custom function
def score_checker(score):
  if score > 0.5:
    return "Student passed the test"
  else:
    return "Student failed the test"


score_checker_declaration = {
    'name': "score_checker",
    'description': "Check if a score is a pass or fail",
    'parameters': {
        "type": "object",
        "properties": {
            "score": {
                "type": "number",
                "description": "The score to check"
            }
        },
        "required": [
            "score"
        ]
    },
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)


def basic_function_calling(prompt):
  response = model.generate_content(
      prompt,
      tools=[{
          'function_declarations': [score_checker_declaration],
      }]
  )
  function_call = response.candidates[0].content.parts[0].function_call
  args = function_call.args
  function_name = function_call.name

  if function_name == 'score_checker':
    result = score_checker(args['score'])

    response = model.generate_content(
        "Based on this information `" + result +
        "` respond to the student in a friendly manner.",
    )

    return response
  else:
    print("Function not called")
    return response


def main():
  welcome_message = f"### - 02_function_calling.py"
  print(welcome_message)

  while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
      break
    response = basic_function_calling(user_input)
    print(f"AI: {response.text}")


if __name__ == "__main__":
  main()
