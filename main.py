import logging
from src.configs.config import BASE_REPO_DIR
from src.repo.cloner import clone_repo
from src.summarizer.file_summarizer import summarize_files

# 로거 설정
logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    repo_url = input("Enter Git repo URL: ").strip()
    repo_path = clone_repo(repo_url, BASE_REPO_DIR)

    if not repo_path:
        logger.error("Repository clone failed.")
        return

    logger.info(f"Repository ready at: {repo_path}")
    summarize_files(repo_path)


if __name__ == "__main__":
    main()
