from agents.test_agent import run_tests
from agents.fix_agent import apply_fix
from services.results_service import save_results


def autonomous_healing_loop(repo_path: str, max_retries: int = 5):
    """
    Autonomous loop:
    run tests → detect failures → apply fixes → repeat
    """

    history = []

    for iteration in range(1, max_retries + 1):

        print(f"\n🔁 Iteration {iteration}")

        test_result = run_tests(repo_path)

        history.append({
            "iteration": iteration,
            "return_code": test_result.get("return_code"),
            "failures": test_result.get("failures", [])
        })

        # ✅ tests passed
        if test_result.get("return_code") == 0:

            result = {
                "status": "PASSED",
                "iterations": iteration,
                "history": history
            }

            save_results(result)   # 🔥 save results.json
            return result

        # ❌ no failures detected
        failures = test_result.get("failures", [])
        if not failures:

            result = {
                "status": "FAILED",
                "message": "No detectable failures",
                "history": history
            }

            save_results(result)
            return result

        # 🔧 apply fixes
        for failure in failures:
            apply_fix(repo_path, failure)

    # 🚨 max retries reached
    result = {
        "status": "FAILED",
        "message": "Max retries reached",
        "iterations": max_retries,
        "history": history
    }

    save_results(result)
    return result
