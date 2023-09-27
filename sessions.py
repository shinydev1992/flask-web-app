from flask import Blueprint, request, jsonify
from models import Session, db
from auth import requires_roles  # Ako je dekorator u drugoj datoteci, prilagodite ovo uvoz
from flask_jwt_extended import jwt_required

sessions_blueprint = Blueprint('sessions', __name__)

@sessions_blueprint.route('/sessions', methods=['GET'])
def get_sessions():
    # Prikaz svih sesija
    sessions = Session.query.all()
    return jsonify([session.serialize() for session in sessions])

@sessions_blueprint.route('/session', methods=['POST'])
def create_session():
    # Kreiranje nove sesije
    data = request.json
    session = Session(start_time=data['start_time'], status="pending")
    db.session.add(session)
    db.session.commit()
    return jsonify(session.serialize()), 201

@sessions_blueprint.route('/session/<int:session_id>', methods=['GET'])
def get_session(session_id):
    # Prikaz pojedine sesije
    session = Session.query.get(session_id)
    if not session:
        return jsonify(message="Session not found!"), 404
    return jsonify(session.serialize())

@sessions_blueprint.route('/session/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    # Ažuriranje sesije
    session = Session.query.get(session_id)
    if not session:
        return jsonify(message="Session not found!"), 404
    data = request.json
    if 'start_time' in data:
        session.start_time = data['start_time']
    if 'status' in data:
        session.status = data['status']
    db.session.commit()
    return jsonify(session.serialize())

@sessions_blueprint.route('/start-voting/<int:session_id>', methods=['POST'])
@jwt_required()
@requires_roles('predsjednik')
def start_voting(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify(message="Session not found!"), 404

    # Logika za pokretanje glasovanja, npr. postavljanje statusa sesije na "active"
    session.status = "active"
    db.session.commit()

    return jsonify(message="Voting started successfully!")

@sessions_blueprint.route('/stop-voting/<int:session_id>', methods=['POST'])
@jwt_required()
@requires_roles('predsjednik')
def stop_voting(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify(message="Session not found!"), 404

    # Logika za zaustavljanje glasovanja, npr. postavljanje statusa sesije na "stopped"
    session.status = "stopped"
    db.session.commit()

    return jsonify(message="Voting stopped successfully!")

@sessions_blueprint.route('/restart-voting/<int:session_id>', methods=['POST'])
@jwt_required()
@requires_roles('predsjednik')
def restart_voting(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify(message="Session not found!"), 404

    # Logika za ponovno pokretanje glasovanja, npr. ponovno postavljanje statusa sesije na "active"
    session.status = "active"
    db.session.commit()

    return jsonify(message="Voting restarted successfully!")
