import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

from config import BASE_REPO_DIR

# === LOAD ENV ===
load_dotenv()

# === CONFIG ===
SUMMARY_DIR = Path("summaries")
SUMMARY_DIR.mkdir(exist_ok=True)

LLAMA_API_URL = "https://llama.company.com/api/chat"  # 예시용
LLAMA_API_KEY = "your-llama-api-key"  # 예시용

# === FILTERING ===
EXCLUDED_DIRS = {
    "tests", "test", "__pycache__", "venv", ".venv", "build", "dist",
    "migrations", "bin", ".git", ".github", "github", "git", "libs", "third_party"
}
EXCLUDED_FILES = {"__init__.py", "setup.py"}


def should_summarize(filepath: Path) -> bool:
    if not filepath.suffix == ".py":
        return False
    if filepath.name in EXCLUDED_FILES:
        return False
    if any(part in EXCLUDED_DIRS for part in filepath.parts):
        return False
    if filepath.stat().st_size < 30:
        return False
    return True


# === LLM PROMPT ===
SYSTEM_PROMPT = """
당신은 Python 코드를 구조적으로 분석해서 요약하는 전문가입니다.
"""

USER_PROMPT_TEMPLATE = """
다음은 하나의 Python 파일입니다. 이 파일의 핵심 구조와 기능을 요약해 주세요.

요약 결과는 반드시 **JSON 형식**으로 작성하며, 다음 항목을 포함해야 합니다:

- file: (string) 파일 이름
- description: (string) 이 파일이 수행하는 주요 역할, 기능 설명
- key_functions: (list of strings) 핵심 함수 이름 목록
- key_classes: (list of strings) 핵심 클래스 이름 목록
- depends_on: (list of strings) 이 파일이 import한 외부 모듈 또는 다른 내부 파일 이름

⚠️ 반드시 JSON으로만 응답하고, 주석이나 설명을 추가하지 마세요.

파일명: {filename}

```python
{code}
```
"""


# === LLAMA 요약 함수 ===
def summarize_file_with_llm(filepath: Path) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    prompt = USER_PROMPT_TEMPLATE.format(filename=str(filepath.name), code=code[:6000])

    payload = {
        "model": "llama-3-chat",  # 실제 모델 이름에 맞게 수정
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(LLAMA_API_URL, headers=headers, json=payload)
        res.raise_for_status()
        summary = res.json()["choices"][0]["message"]["content"].strip()

        if summary.startswith("```json"):
            summary = summary.lstrip("`json\n").rstrip("`").strip()
        elif summary.startswith("```"):
