import requests
import json

# Test the new agent endpoints
BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/agent/health")
        print(f"Health status: {response.status_code}")
        print(f"Health response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_retrieval():
    print("\nTesting retrieval endpoint...")
    try:
        payload = {
            "query": "What is ROS2?",
            "top_k": 3
        }
        response = requests.post(f"{BASE_URL}/retrieval/query", json=payload)
        print(f"Retrieval status: {response.status_code}")
        if response.status_code == 200:
            print("Retrieval test passed")
            return True
        else:
            print(f"Retrieval response: {response.text}")
            return False
    except Exception as e:
        print(f"Retrieval test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    health_ok = test_health()
    retrieval_ok = test_retrieval()

    if health_ok:
        print("\n✓ Health endpoint is working")
    else:
        print("\n✗ Health endpoint failed")

    if retrieval_ok:
        print("✓ Retrieval endpoint is working")
    else:
        print("✗ Retrieval endpoint failed")