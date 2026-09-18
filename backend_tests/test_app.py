def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_details(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    activities = response.json()
    assert response.status_code == 200
    assert expected_activity in activities
    assert activities[expected_activity]["description"]
    assert activities[expected_activity]["schedule"]
    assert isinstance(activities[expected_activity]["participants"], list)


def test_signup_adds_normalized_email_to_activity(client):
    # Arrange
    activity_name = "Art Club"
    email = "  NewStudent@Mergington.edu "
    normalized_email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == f"Signed up {normalized_email} for {activity_name}"
    assert normalized_email in response_data["participants"]


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_email_case_insensitively(client):
    # Arrange
    activity_name = "Chess Club"
    email = " MICHAEL@MERGINGTON.EDU "

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_normalized_email_from_activity(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "  NewStudent@Mergington.edu "
    normalized_email = "newstudent@mergington.edu"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": normalized_email},
    )

    # Assert
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == f"Unregistered {normalized_email} from {activity_name}"
    assert normalized_email not in response_data["participants"]


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_missing_participant(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
