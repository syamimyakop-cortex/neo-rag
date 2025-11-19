import requests
import os

BASE_URL = "http://localhost:8000"
TEST_PDF = "windows-whats-new (1).pdf"

def test_health():
    print("Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        print("[PASS] Health Check Passed")
    except Exception as e:
        print(f"[FAIL] Health Check Failed: {e}")

def test_upload():
    print("Testing Upload...")
    if not os.path.exists(TEST_PDF):
        print(f"[WARN] Test PDF '{TEST_PDF}' not found. Skipping upload test.")
        return False

    try:
        with open(TEST_PDF, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            assert response.status_code == 200
            data = response.json()
            assert "chunks" in data
            print(f"[PASS] Upload Passed (Chunks: {data['chunks']})")
            return True
    except Exception as e:
        print(f"[FAIL] Upload Failed: {e}")
        return False

def test_query():
    print("Testing Query...")
    try:
        payload = {"question": "What is new in Windows?"}
        response = requests.post(f"{BASE_URL}/query", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        print(f"[PASS] Query Passed")
        print(f"   Answer Preview: {data['answer'][:100]}...")
    except Exception as e:
        print(f"[FAIL] Query Failed: {e}")

if __name__ == "__main__":
    print("--- Starting Backend Tests ---")
    test_health()
    if test_upload():
        test_query()
    print("--- Tests Completed ---")
