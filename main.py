from src.configs.config import BASE_REPO_DIR
from src.repo.cloner import clone_repo
from src.summarizer.file_summarizer import summarize_files


def main():
    repo_url = input("Enter Git repo URL: ").strip()
    repo_path = clone_repo(repo_url, BASE_REPO_DIR)

    if not repo_path:
        print("\n[X] Repository clone failed.")
        return

    print(f"\n[✓] Repository ready at: {repo_path}")

    summarize_files(repo_path)


if __name__ == "__main__":
    main()
