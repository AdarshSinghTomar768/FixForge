from fastapi import APIRouter
from pydantic import BaseModel
from agents.repo_agent import clone_repository

router = APIRouter()


class RepoRequest(BaseModel):
    repo_url: str


@router.get("/")
def health_check():
    return {"status": "backend running"}


@router.post("/clone")
def clone_repo(data: RepoRequest):
    path = clone_repository(data.repo_url)
    return {"message": "Repo cloned successfully", "path": path}
