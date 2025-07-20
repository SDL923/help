import git 
from pathlib import Path


def clone_repo(repo_url: str, dest_dir: Path)->Path:
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git',"")
    repo_path = dest_dir / repo_name
    
    if repo_path.exists():
        print(f"Repository already exists at {repo_path}")
        return repo_path
    
    print(f"Cloning {repo_url} into {repo_path} ...")
    try:
        git.Repo.clone_from(repo_url, repo_path)
        print("Clone complete.")
        return repo_path
    except Exception as e:
        print(f"Failed to clone: {e}")
        return None
