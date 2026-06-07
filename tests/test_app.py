from fastapi import status


def test_get_activities_returns_all_activities(client):
    # Arrange / Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert "Science Club" in payload


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Science Club"
    email = "test.signup@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in client.get("/activities").json()[activity_name]["participants"]

    # Cleanup
    client.delete(f"/activities/{activity_name}/participants", params={"email": email})


def test_signup_for_activity_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_removes_student(client):
    # Arrange
    activity_name = "Programming Class"
    email = "remove.test@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"
    remove_url = f"/activities/{activity_name}/participants"

    client.post(signup_url, params={"email": email})

    # Act
    response = client.delete(remove_url, params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Gym Class"
    email = "not.registered@mergington.edu"
    remove_url = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(remove_url, params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Participant not found in this activity"
