import subprocess

def query_ollama(prompt: str, model: str = "nous-hermes:13b") -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120  # prevent hanging
        )

        if result.returncode != 0:
            return f"[❌ ERROR] Ollama error: {result.stderr.decode().strip()}"

        # Filter out Ollama startup banners and just return the generated text
        output = result.stdout.decode().split("\n")
        answer_lines = [line for line in output if not line.startswith(">>>")]
        return "\n".join(answer_lines).strip()

    except subprocess.TimeoutExpired:
        return "[⏱️] Ollama timed out. Try a shorter or different prompt."
    except Exception as e:
        return f"[❗] Unexpected error: {str(e)}"
