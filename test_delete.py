import requests

BASE_URL = "http://localhost:8000"

def test_clear():
    print("Testing Clear Endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/clear")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"[PASS] Clear Passed: {data['message']}")
        
        # Verify query fails after clear (optional, but good check)
        print("Verifying Query after Clear...")
        payload = {"question": "test"}
        response = requests.post(f"{BASE_URL}/query", json=payload)
        data = response.json()
        # Expecting "Please upload a PDF first."
        if "Please upload a PDF first" in data.get("answer", ""):
             print("[PASS] Query correctly blocked after clear.")
        else:
             print(f"[WARN] Query response after clear: {data}")

    except Exception as e:
        print(f"[FAIL] Clear Failed: {e}")

if __name__ == "__main__":
    test_clear()
