from flask import Blueprint, request, jsonify
from models import Vote, User, AgendaItem, QuorumVote, UserQuorumVote, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit
from datetime import datetime

votes_blueprint = Blueprint('votes', __name__)

@votes_blueprint.route('/agenda/<int:agenda_item_id>/vote', methods=['POST'])
@jwt_required()
def cast_vote(agenda_item_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found!"), 404

    agenda_item = AgendaItem.query.get(agenda_item_id)
    if not agenda_item:
        return jsonify(message="Agenda item not found!"), 404

    data = request.json
    decision = data.get('decision')

    # Check if the user has already voted on this agenda item
    existing_vote = Vote.query.filter_by(user_id=user_id, agenda_item_id=agenda_item_id).first()
    if existing_vote:
        existing_vote.decision = decision
    else:
        vote = Vote(user_id=user_id, agenda_item_id=agenda_item_id, decision=decision)
        db.session.add(vote)

    db.session.commit()

    # Emit WebSocket event to all clients
    emit('vote_casted', {'agenda_item_id': agenda_item_id, 'decision': decision}, broadcast=True)

    return jsonify(message="Vote casted successfully!")

@votes_blueprint.route('/agenda/<int:agenda_item_id>/results', methods=['GET'])
def get_voting_results(agenda_item_id):
    votes = Vote.query.filter_by(agenda_item_id=agenda_item_id).all()

    results = {
        "yes": 0,
        "no": 0,
        "maybe": 0
    }

    for vote in votes:
        if vote.decision == 'yes':
            results["yes"] += 1
        elif vote.decision == 'no':
            results["no"] += 1
        elif vote.decision == 'maybe':
            results["maybe"] += 1

    return jsonify(results)

@votes_blueprint.route('/session/<int:session_id>/start-quorum', methods=['POST'])
@jwt_required()
def start_quorum(session_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Provjerite je li korisnik administrator (predsjednik vijeća)
    if user.role != 'administrator':
        return jsonify(message="Only administrators can start a quorum vote."), 403

    quorum_vote = QuorumVote(session_id=session_id, start_time=datetime.utcnow())
    db.session.add(quorum_vote)
    db.session.commit()
    return jsonify(message="Quorum vote started!")

@votes_blueprint.route('/session/<int:session_id>/vote-quorum', methods=['POST'])
@jwt_required()
def vote_quorum(session_id):
    user_id = get_jwt_identity()
    decision = request.json.get('decision')

    quorum_vote = QuorumVote.query.filter_by(session_id=session_id).order_by(QuorumVote.start_time.desc()).first()
    if not quorum_vote:
        return jsonify(message="No quorum vote in progress."), 400

    vote = UserQuorumVote(user_id=user_id, quorum_vote_id=quorum_vote.quorum_vote_id, decision=decision)
    db.session.add(vote)
    db.session.commit()
    return jsonify(message="Voted for quorum!")

@votes_blueprint.route('/session/<int:session_id>/quorum-results', methods=['GET'])
def get_quorum_results(session_id):
    quorum_vote = QuorumVote.query.filter_by(session_id=session_id).order_by(QuorumVote.start_time.desc()).first()
    if not quorum_vote:
        return jsonify(message="No quorum vote found for this session."), 400

    votes = UserQuorumVote.query.filter_by(quorum_vote_id=quorum_vote.quorum_vote_id).all()

    results = {
        "present": 0,
        "absent": 0
    }

    for vote in votes:
        if vote.decision == 'present':
            results["present"] += 1
        elif vote.decision == 'absent':
            results["absent"] += 1

    return jsonify(results)
