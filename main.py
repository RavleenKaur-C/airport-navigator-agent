from agent.airport_agent import chat_with_agent

print("Welcome to your Airport Assistant!")
print("Type your travel plan (e.g., 'I'm flying from Chicago to Paris to Dubai') or say 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = chat_with_agent(user_input)
    print(response)
    print()
