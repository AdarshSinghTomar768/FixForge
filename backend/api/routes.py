from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

from agents.repo_agent import clone_repository
from agents.test_agent import run_tests
from agents.fix_agent import apply_fix
from agents.autonomous_loop import autonomous_healing_loop

router = APIRouter()


# =========================
# REQUEST MODELS
# =========================

class RepoRequest(BaseModel):
    repo_url: str


class TestRequest(BaseModel):
    repo_path: str


class FixRequest(BaseModel):
    repo_path: str
    failure: dict


class LoopRequest(BaseModel):
    repo_path: str
    max_retries: int = 5


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


# =========================
# APPLY FIX ENDPOINT
# =========================

@router.post("/apply-fix")
def fix_code(data: FixRequest):
    result = apply_fix(data.repo_path, data.failure)
    return result


# =========================
# AUTONOMOUS LOOP ENDPOINT
# =========================

@router.post("/run-agent")
def run_autonomous_agent(data: LoopRequest):
    result = autonomous_healing_loop(
        data.repo_path,
        data.max_retries
    )
    return result


# =========================
# LIVE RESULTS POLLING ENDPOINT
# =========================

@router.get("/results")
def get_results():
    try:
        results_path = os.path.join("results", "results.json")

        if not os.path.exists(results_path):
            return {"status": "no_results"}

        with open(results_path, "r") as f:
            return json.load(f)

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
