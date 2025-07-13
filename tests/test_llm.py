from llm_interface import query_ollama

if __name__ == "__main__":
    prompt = "What are the main steps to secure a web application?"
    response = query_ollama(prompt)
    print("\n🤖 Friday's Response:\n")
    print(response)
