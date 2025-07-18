import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# === LOAD ENV ===
load_dotenv()
client = OpenAI()

# === CONFIG ===
SUMMARY_DIR = Path("summaries")
OUTPUT_PATH = Path("repo_summary.json")


def load_summaries(summary_dir: Path):
    summaries = []
    for file in summary_dir.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                summaries.append(data)
        except Exception as e:
            print(f"[!] Failed to load {file.name}: {e}")
    return summaries


def generate_repo_summary(summaries: list) -> str:
    system_prompt = """
    당신은 Python 레포지토리 분석 전문가입니다.
    """

    user_prompt_template = """
    다음은 여러 Python 파일들의 요약입니다. 이 레포지토리 전체의 구조와 기능을 분석하여 다음 정보를 요약해주세요:

    - 전체 레포의 주요 목적
    - 주요 기능 영역 (예: 인증, 라우팅, 문서화 등)
    - 각 기능에 연관된 파일 이름
    - 기능 간 관계나 의존성이 중요한 경우 간단히 언급

    가능하면 주요 기능과 파일 매핑 정보를 JSON 형태로도 출력해주세요.

    ```json
    {summaries_json}
    ```
    """

    summaries_json = json.dumps(summaries, indent=2, ensure_ascii=False)
    user_prompt = user_prompt_template.format(summaries_json=summaries_json)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    summaries = load_summaries(SUMMARY_DIR)

    if not summaries:
        print("[X] 요약본이 없습니다. 먼저 summarize_python_files.py 를 실행하세요.")
        exit(1)

    print(f"[*] 총 요약 파일 수: {len(summaries)}")
    result = generate_repo_summary(summaries)

    print("\n[✓] 전체 레포 요약 결과:\n")
    print(result)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"\n[✓] 저장 완료: {OUTPUT_PATH}")
