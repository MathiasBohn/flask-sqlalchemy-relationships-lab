#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/events")
def get_events():
    events = Event.query.all()
    
    events_list = []
    for event in events:
        event_dict = {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        events_list.append(event_dict)
    
    return jsonify(events_list), 200


@app.route("/events/<int:id>/sessions")
def get_event_sessions(id):
    event = Event.query.get(id)
    
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    sessions = event.sessions
    
    sessions_list = []
    for session in sessions:
        session_dict = {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
        }
        sessions_list.append(session_dict)
    
    return jsonify(sessions_list), 200


@app.route("/speakers")
def get_speakers():
    speakers = Speaker.query.all()
    
    speakers_list = []
    for speaker in speakers:
        speaker_dict = {
            "id": speaker.id,
            "name": speaker.name
        }
        speakers_list.append(speaker_dict)
    
    return jsonify(speakers_list), 200


@app.route("/speakers/<int:id>")
def get_speaker(id):
    speaker = Speaker.query.get(id)
    
    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404
    
    if speaker.bio:
        bio_text = speaker.bio.bio_text
    else:
        bio_text = "No bio available"
    
    speaker_dict = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text
    }
    
    return jsonify(speaker_dict), 200

@app.route("/sessions/<int:id>/speakers")
def get_session_speakers(id):
    session = Session.query.get(id)
    
    if session is None:
        return jsonify({"error": "Session not found"}), 404
    
    speakers = session.speakers
    
    speakers_list = []
    for speaker in speakers:
        if speaker.bio:
            bio_text = speaker.bio.bio_text
        else:
            bio_text = "No bio available"
        
        speaker_dict = {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": bio_text
        }
        speakers_list.append(speaker_dict)
    
    return jsonify(speakers_list), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)