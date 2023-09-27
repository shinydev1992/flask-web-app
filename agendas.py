from flask import Blueprint, request, jsonify, send_from_directory
from models import AgendaItem, db
from flask_jwt_extended import jwt_required

agendas_blueprint = Blueprint('agendas', __name__)

@agendas_blueprint.route('/session/<int:session_id>/agendas', methods=['GET'])
def get_agendas(session_id):
    # Prikaz svih dnevnih redova za određenu sesiju
    agenda_items = AgendaItem.query.filter_by(session_id=session_id).all()
    return jsonify([item.serialize() for item in agenda_items])

@agendas_blueprint.route('/session/<int:session_id>/agenda/<int:agenda_id>', methods=['GET'])
def get_agenda_detail(session_id, agenda_id):
    # Prikaz detalja dnevnog reda
    agenda_item = AgendaItem.query.get(agenda_id)
    if not agenda_item:
        return jsonify(message="Agenda item not found!"), 404
    return jsonify(agenda_item.serialize())

@agendas_blueprint.route('/session/<int:session_id>/agenda/<int:agenda_id>/pdf', methods=['GET'])
def get_agenda_pdf(session_id, agenda_id):
    # Prikaz PDF-a za određeni dnevni red
    agenda_item = AgendaItem.query.get(agenda_id)
    if not agenda_item or not agenda_item.pdf_path:
        return jsonify(message="PDF not found!"), 404
    # Pretpostavimo da su PDF-ovi pohranjeni u mapi 'pdfs' unutar vaše aplikacije
    return send_from_directory('pdfs', agenda_item.pdf_path)
