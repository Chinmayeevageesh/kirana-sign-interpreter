import sys
import requests

BASE_URL = "http://127.0.0.1:8000"


def check(condition, message):
    if condition:
        print(f"PASS: {message}")
        return True

    print(f"FAIL: {message}")
    return False


def main():
    results = []

    print("\n=== Kirana Sign Interpreter API Smoke Test ===\n")

    # 1. Check whether backend is running
    try:
        response = requests.get(
            f"{BASE_URL}/api/health",
            timeout=5
        )
    except requests.RequestException as exc:
        print("FAIL: Backend is unreachable.")
        print(f"Details: {exc}")
        print("\nStart the backend using:")
        print("python -m uvicorn main:app --reload")
        sys.exit(1)

    results.append(
        check(
            response.status_code == 200,
            "Health endpoint responds with HTTP 200"
        )
    )

    try:
        health_data = response.json()
    except ValueError:
        health_data = {}

    results.append(
        check(
            health_data.get("status") == "ok",
            "Health response contains status=ok"
        )
    )

    # 2. Test dummy recognition
    landmarks = [
        [0.1, 0.2, 0.0] for _ in range(21)
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/api/recognize",
            json={
                "landmarks": landmarks,
                "test_label": "rice"
            },
            timeout=5
        )

        results.append(
            check(
                response.status_code == 200,
                "Recognition endpoint responds with HTTP 200"
            )
        )

        try:
            data = response.json()
        except ValueError:
            data = {}

        results.append(
            check(
                data.get("recognized") is True
                and data.get("label") == "rice",
                "Dummy rice recognition returns expected label"
            )
        )

        results.append(
            check(
                data.get("kannada") == "ಅಕ್ಕಿ",
                "Rice response contains the Kannada translation"
            )
        )

        results.append(
            check(
                data.get("status") == "recognized",
                "Recognition response has the expected status"
            )
        )

    except requests.RequestException as exc:
        results.append(False)
        print(f"FAIL: Recognition request failed: {exc}")

    # 3. Test invalid landmark count
    try:
        response = requests.post(
            f"{BASE_URL}/api/recognize",
            json={
                "landmarks": landmarks[:20],
                "test_label": "rice"
            },
            timeout=5
        )

        results.append(
            check(
                response.status_code == 422,
                "Invalid landmark count is rejected with HTTP 422"
            )
        )

    except requests.RequestException as exc:
        results.append(False)
        print(f"FAIL: Validation request failed: {exc}")

    # 4. Final summary
    passed = sum(results)
    total = len(results)

    print(f"\n=== Result: {passed}/{total} checks passed ===")

    if passed == total:
        print("Smoke test completed successfully!")
    else:
        print("Some checks failed. Review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()