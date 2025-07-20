import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

from src.configs.config import BASE_REPO_DIR, SUMMARY_DIR

# === ENV & CLIENT ===
load_dotenv()
client = OpenAI()

# === 필터 규칙 ===
EXCLUDED_DIRS = {
    "tests", "test", "__pycache__", "venv", ".venv", "build", "dist",
    "migrations", "examples", "bin", ".git", ".github",
    "libs", "third_party", ".mypy_cache", ".pytest_cache",
    ".idea", ".vscode", "node_modules", "logs", "notebooks"
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

반드시 JSON으로만 응답하고, 주석이나 설명을 추가하지 마세요.

파일명: {filename}

```python
{code}
```
"""

def summarize_file_with_llm(filepath: Path) -> dict:
    try:
        code = filepath.read_text(encoding="utf-8")
        prompt = USER_PROMPT_TEMPLATE.format(filename=str(filepath.name), code=code[:6000])

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        summary = response.choices[0].message.content.strip()
        if summary.startswith("```json"):
            summary = summary.lstrip("`json\n").rstrip("`").strip()
        elif summary.startswith("```"):
            summary = summary.lstrip("`").strip()

        #print(f"[DEBUG] LLM response for {filepath.name}:\n{summary}\n")
        return json.loads(summary)
    except Exception as e:
        print(f"[!] Error summarizing {filepath}: {e}")
        return None

def summarize_files(repo_path: Path):
    print(f"[*] Summarizing Python files in: {repo_path}")
    for root, _, files in os.walk(repo_path):
        for file in files:
            path = Path(root) / file
            if should_summarize(path):
                print(f"[+] Summarizing: {path.relative_to(repo_path)}")
                summary = summarize_file_with_llm(path)
                if summary:
                    rel_path = path.relative_to(repo_path)
                    safe_name = str(rel_path).replace("/", "__").replace("\\", "__")
                    save_path = SUMMARY_DIR / (safe_name + ".json")
                    with open(save_path, "w", encoding="utf-8") as f:
                        json.dump(summary, f, indent=2, ensure_ascii=False)
