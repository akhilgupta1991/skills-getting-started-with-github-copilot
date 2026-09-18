from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == 200
    assert unregister_response.json()["participants"] == []

    remaining = client.get("/activities")
    assert email not in remaining.json()[activity_name]["participants"]


def test_unregister_participant_fails_for_unknown_email():
    activity_name = "Soccer Club"
    email = "missing@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
