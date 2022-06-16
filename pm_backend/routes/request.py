#!/usr/bin/python3
"""route for request"""
from database import tables
from models.request import Request
from models.request_event import RequestEvent
from routes import app_views
from flask import jsonify, abort, request, make_response
from database.db_procedure import DBProcedures
from datetime import datetime

time = '%Y-%m-%dT%H:%M:%S.%f'
dt_date = '%Y-%m-%d'


@app_views.route('/request/all', methods=['GET'],
                 strict_slashes=False)
def all_request():
    """returns list of all projects"""
    date_begin = datetime.strptime(
        request.args.get('date_begin', None), dt_date)
    date_end = datetime.strptime(
        request.args.get('date_end', None), dt_date)
    if date_end is None or date_begin is None:
        return make_response(jsonify({'request': 'failure'}), 204)
    company_id = request.args.get('company_id', None)
    department = request.args.get('department', None)
    # Necesito una lista de diccionarios de todos los proyectos con
    # todos sus datos en ese rango de fecha
    res = DBProcedures.requests_all(
        date_begin, date_end, company_id, department)
    if res is None:
        return make_response(jsonify({'request': 'empty'}), 204)
    return make_response(jsonify(res), 200)


@app_views.route('/request', methods=['GET'],
                 strict_slashes=False)
def get_request():
    """returns a list of specific projects"""
    id = request.args.get('id', None)
    # Necesito un diccionario de el proyectos con todos sus datos
    res = DBProcedures.requests_one(id)
    if res is None:
        return make_response(jsonify({'request': 'empty'}), 204)
    return make_response(jsonify(res.to_dict()), 200)


@app_views.route('/request', methods=['POST'],
                 strict_slashes=False)
def insert_request():
    """inserts a new requirement/project"""
    item = Request()
    data = request.get_json()
    item.date_issue = datetime.strptime(
        data.get('date_issue', None), time)
    item.user_id = data.get('user_id', None)
    item.reason = data.get('reason', None)
    item.subject = data.get('subject', None)
    item.table_pri = tables.get('PRI')
    item.code_pri = data.get('code_pri', None)
    item.code = ''
    item.percentage = 0
    # Data is sent to procedures and is returned on success or failure.
    res = DBProcedures.requests_insert(item)
    print(res)
    if not res:
        return make_response(jsonify({'request': 'failure'}), 204)
    return make_response(jsonify({'request': 'success'}), 201)


@app_views.route('/request', methods=['PUT'],
                 strict_slashes=False)
def update_request():
    """updates a new requirement/project"""
    data = request.get_json()
    item = Request()
    item.id = data.get('id', None)
    item.date_tentative = datetime.strptime(
        data.get('date_tentative', None), time)
    item.date_issue = datetime.strptime(data.get(
        'date_issue', None), time)
    item.user_id = data.get('user_id', None)
    item.name = data.get('name', None)
    item.description = data.get('description', None)
    item.table_typ = tables.get('TYP')
    item.table_pri = tables.get('PRI')
    item.code_typ = data.get('code_typ', None)
    item.code_pri = data.get('code_pri', None)
    res = DBProcedures.requests_update(item)
    if not res:
        return make_response(jsonify({'request': 'failure'}), 204)
    return make_response(jsonify({'request': 'success'}), 201)


@app_views.route('/event', methods=['POST'],
                 strict_slashes=False)
def update_event():
    """changes state"""
    data = request.get_json()
    item = RequestEvent()
    item.project_id = data.get('project_id', None)
    item.code_sta = data.get('code_sta', None)
    item.tabe_sta = tables.get('STA')
    item.date_issue = data.get('date_issue', None)
    item.user_id = data.get('user_id', None)
    res = DBProcedures.requests_events_insert(item)
    if res is None:
        return make_response(jsonify({'request': 'failure'}), 204)
    return make_response(jsonify({'request': 'success'}), 201)
