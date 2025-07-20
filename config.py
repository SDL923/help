from pathlib import Path

BASE_DATA_DIR = Path(__file__).parent.parent.parent / "data"
BASE_REPO_DIR = BASE_DATA_DIR / "cloned_repo"
SUMMARY_DIR = BASE_DATA_DIR / "summaries"

BASE_REPO_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
