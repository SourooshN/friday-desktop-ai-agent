# tests/test_model_selection.py

from core.brain.model_selector import select_model_for_intent

samples = [
    "Please write a Python function to add two numbers",
    "How would one hack a website for security testing?",
    "Tell me a joke about penguins",
]

for text in samples:
    model = select_model_for_intent(text)
    print(f"Input: {text!r}\n→ Selected model: {model}\n")
