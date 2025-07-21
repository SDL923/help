import os
import pickle
import ast
from pathlib import Path

from src.configs.config import AST_DIR, REPO_DIR


def extract_function_code(func_name: str) -> list[dict]:
    """
    저장된 AST와 REPO 디렉토리를 기반으로 함수 정의 전체 코드를 추출합니다.

    Args:
        func_name (str): 추출할 함수 이름

    Returns:
        List[dict]: [
            {
                "function": str,
                "file": str,
                "code": str
            }
        ]
    """
    locations = find_function_location(func_name)
    results = []

    for loc in locations:
        source_path = find_file_by_relative_path(REPO_DIR, loc["file"])
        if not source_path:
            print(f"[!] 파일 경로를 찾을 수 없습니다: {loc['file']}")
            continue

        try:
            with open(source_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            start = loc["lineno"] - 1
            end = loc["end_lineno"] if loc["end_lineno"] else start + 1
            code_block = "".join(lines[start:end])

            results.append({
                "function": func_name,
                "file": str(source_path.relative_to(REPO_DIR)).replace("\\", "/"),
                "code": code_block.strip()
            })

        except Exception as e:
            print(f"[!] Error extracting {func_name} from {source_path}: {e}")

    return results


def find_file_by_relative_path(base_dir: Path, relative_path: str) -> Path | None:
    """
    base_dir 아래를 순회하면서 relative_path와 끝이 일치하는 파일을 찾는다.
    예: relative_path = "src/utils/helpers.py"

    Returns:
        전체 경로 Path 또는 None
    """
    relative_path = relative_path.replace("\\", "/")  # 윈도우 호환

    for root, _, files in os.walk(base_dir):
        for file in files:
            full_path = Path(root) / file
            try:
                rel = full_path.relative_to(base_dir).as_posix()
                if rel.endswith(relative_path):
                    return full_path
            except Exception:
                continue
    return None


def find_function_location(func_name: str) -> list[dict]:
    """
    저장된 .ast 파일들에서 주어진 함수 이름을 정의한 위치를 반환합니다.

    Args:
        func_name (str): 찾을 함수 이름

    Returns:
        List[dict]: [{"file": str, "lineno": int, "end_lineno": int}]
    """
    results = []

    for ast_file in AST_DIR.glob("*.ast"):
        try:
            with open(ast_file, "rb") as f:
                tree = pickle.load(f)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    result = {
                        "file": _restore_source_path(ast_file),
                        "lineno": node.lineno,
                        "end_lineno": getattr(node, "end_lineno", None)
                    }
                    results.append(result)

        except Exception as e:
            print(f"[!] Error reading AST file {ast_file.name}: {e}")

    return results


def _restore_source_path(ast_file: Path) -> str:
    """
    src__utils__helpers.py.ast → src/utils/helpers.py
    """
    name = ast_file.stem  # remove .ast
    return name.replace("__", "/")


# if __name__ == "__main__":
#     name = input("찾을 함수 이름 입력: ").strip()
#     locations = find_function_location(name)

#     if not locations:
#         print("[X] 해당 함수 정의를 찾을 수 없습니다.")
#     else:
#         for loc in locations:
#             print(f"[✓] {loc['file']}:{loc['lineno']}")
