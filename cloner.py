import git
import logging
from pathlib import Path

# 로거 설정
logger = logging.getLogger("repo_cloner")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def clone_repo(repo_url: str, dest_dir: Path) -> Path:
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', "")
    repo_path = dest_dir / repo_name

    if repo_path.exists():
        logger.info(f"Repository already exists at {repo_path}")
        return repo_path

    logger.info(f"Cloning {repo_url} into {repo_path} ...")
    try:
        git.Repo.clone_from(repo_url, repo_path)
        logger.info("Clone complete.")
        return repo_path
    except Exception as e:
        logger.error(f"Failed to clone: {e}")
        return None
