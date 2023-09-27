from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)  # Dodali ste ovo polje
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.party_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Party(db.Model):
    __tablename__ = 'party'

    party_id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

class Session(db.Model):
    __tablename__ = 'session'

    session_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False)

class AgendaItem(db.Model):
    __tablename__ = 'agenda_item'

    agenda_item_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    pdf_path = db.Column(db.String(200), nullable=True)

class Vote(db.Model):
    __tablename__ = 'vote'

    vote_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    agenda_item_id = db.Column(db.Integer, db.ForeignKey('agenda_item.agenda_item_id'), nullable=False)
    decision = db.Column(db.String(50), nullable=False)
    vote_time = db.Column(db.DateTime, default=datetime.utcnow)

class QuorumVote(db.Model):
    __tablename__ = 'quorum_vote'

    quorum_vote_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)

class UserQuorumVote(db.Model):
    __tablename__ = 'user_quorum_vote'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    quorum_vote_id = db.Column(db.Integer, db.ForeignKey('quorum_vote.quorum_vote_id'), primary_key=True)
    decision = db.Column(db.String(50), nullable=False)
    vote_time = db.Column(db.DateTime, default=datetime.utcnow)
