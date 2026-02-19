from fastapi import APIRouter
from pydantic import BaseModel

from agents.repo_agent import clone_repository
from agents.test_agent import run_tests

router = APIRouter()


# =========================
# REQUEST MODELS
# =========================

class RepoRequest(BaseModel):
    repo_url: str


class TestRequest(BaseModel):
    repo_path: str


# =========================
# HEALTH CHECK
# =========================

@router.get("/")
def health_check():
    return {"status": "backend running"}


# =========================
# REPO CLONE ENDPOINT
# =========================

@router.post("/clone")
def clone_repo(data: RepoRequest):
    path = clone_repository(data.repo_url)
    return {
        "message": "Repo cloned successfully",
        "path": path
    }


# =========================
# RUN TESTS ENDPOINT
# =========================

@router.post("/run-tests")
def run_repo_tests(data: TestRequest):
    result = run_tests(data.repo_path)
    return result
