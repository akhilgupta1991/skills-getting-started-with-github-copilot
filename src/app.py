"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")


def normalize_email(email: str) -> str:
    return email.strip().lower()


# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice basketball skills and compete in school tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer Club": {
        "description": "Develop soccer skills and play competitive matches",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": []
    },
    "Art Club": {
        "description": "Explore drawing, painting, and other visual arts",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Drama Club": {
        "description": "Act, direct, and produce performances for the school community",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Debate Team": {
        "description": "Build argumentation and public speaking skills through debates",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    normalized_email = normalize_email(email)

    # Validate student is not already signed up (case-insensitive and trims whitespace)
    existing_participants = [normalize_email(participant) for participant in activity["participants"]]
    if normalized_email in existing_participants:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}", "participants": activity["participants"]}


@app.delete("/activities/{activity_name}/unregister")
def unregister_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = normalize_email(email)

    normalized_participants = [normalize_email(participant) for participant in activity["participants"]]
    if normalized_email not in normalized_participants:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")

    for participant in list(activity["participants"]):
        if normalize_email(participant) == normalized_email:
            activity["participants"].remove(participant)
            break

    return {"message": f"Unregistered {normalized_email} from {activity_name}", "participants": activity["participants"]}
