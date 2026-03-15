from fastapi.testclient import TestClient
from main import app
from database import Base, engine

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def run_tests():
    print("--- Starting Verification ---")
    
    # 1. Create User
    resp = client.post("/users/", json={"name": "Test User", "email": "test@example.com"})
    print("Create User:", resp.status_code, resp.json() if resp.status_code != 500 else "Internal Error")
    if resp.status_code != 200 and resp.status_code != 400:
        return
    user_id = resp.json().get("id", 1)
    
    # 2. Create Habit
    resp = client.post(f"/habits/", params={"user_id": user_id}, json={
        "habit_name": "Read Book", 
        "category": "Education", 
        "target_frequency": "daily"
    })
    print("Create Habit:", resp.status_code, resp.json() if resp.status_code != 500 else "Internal Error")
    habit_id = resp.json().get("id", 1)
    
    # 3. Mark completed
    from datetime import date, timedelta
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    resp = client.post(f"/habits/{habit_id}/mark", json={"date": today, "completed": True})
    print("Mark Habit Today:", resp.status_code, resp.json())
    resp = client.post(f"/habits/{habit_id}/mark", json={"date": yesterday, "completed": True})
    print("Mark Habit Yesterday:", resp.status_code, resp.json())
    
    resp = client.post(f"/habits/{habit_id}/mark", json={"date": today, "completed": True})
    print("Mark Habit Duplicate (Expected 400):", resp.status_code, resp.json())
    
    # 4. Check Analytics
    resp = client.get(f"/analytics/streak/{habit_id}")
    print("Streak Info:", resp.status_code, resp.json())
    
    resp = client.get(f"/analytics/weekly/{habit_id}")
    print("Weekly Analytics:", resp.status_code, len(resp.json()), "records")
    
    resp = client.get(f"/analytics/heatmap/{user_id}")
    print("Heatmap Data:", resp.status_code, resp.json())
    
    print("--- Verification Complete ---")

if __name__ == "__main__":
    run_tests()
