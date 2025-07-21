from src.configs.config import REPO_DIR
from src.repo.cloner import clone_repo
from src.summarizer.file_summarizer import summarize_files
from src.ast.ast_generator import process_repo_ast 
from src.ast.function_locator import extract_function_code


def main():
#     repo_url = input("Enter Git repo URL: ").strip()
#     repo_path = clone_repo(repo_url, BASE_REPO_DIR)

#     if not repo_path:
#         print("\n[X] Repository clone failed.")
#         return

#     print(f"\n[✓] Repository ready at: {repo_path}")

#     summarize_files(repo_path)
    
#     process_repo_ast(repo_path)
    
    name = input("함수 이름을 입력하세요: ").strip()
    functions = extract_function_code(name)

    if not functions:
        print("[X] 해당 함수를 찾을 수 없습니다.")
    else:
        for func in functions:
            print(f"\n[✓] {func['file']}")
            print(func['code'])
    


if __name__ == "__main__":
    main()
