from config.settings import Settings


def hello_world():
  print("Hello, world!")
  return "from hello_world"

def main():
  print("Chat with the Hello World model! Type 'exit' to quit.")
  while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
      break
    response = hello_world(user_input)
    print(f"AI: {response}")


if __name__ == "__main__":
  main()
