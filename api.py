from flask import Flask, jsonify, request
from program_manager import ClientManager, ProgramManager
from werkzeug.exceptions import BadRequest
import re

app = Flask(__name__)

program_manager = ProgramManager()
client_manager = ClientManager()

API_PREFIX = '/api/v1'

_cached_programs = [
    {"id": 1, "name": "Nutrition Program"},
    {"id": 2, "name": "Mental Health Support"},
    {"id": 3, "name": "Physical Fitness Program"}
]

def is_valid_client_id(client_id):
    return bool(re.match(r"^[a-zA-Z0-9\-]+$", client_id))

@app.route('/')
def home():
    return jsonify({"success": True, "message": "Health Program Management API v1 is running."})

@app.route(f'{API_PREFIX}/client/<client_id>', methods=['GET'])
def get_client_profile(client_id):
    # SECURITY: Validate input
    if not is_valid_client_id(client_id):
        raise BadRequest("Invalid client ID format.")
    
    client = client_manager.get_client_by_id(client_id)
    if client:
        program_dict = {p.program_id: p.name for p in program_manager.programs}
        enrolled_programs = [program_dict.get(pid, "Unknown Program") for pid in client.program_ids]
        
        client_data = {
            "full_name": client.full_name,
            "age": client.age,
            "gender": client.gender,
            "registered_at": client.registered_at.strftime('%Y-%m-%d %H:%M:%S'),
            "enrolled_programs": enrolled_programs,
            "client_id": client.client_id
        }
        return jsonify({"success": True, "data": client_data}), 200
    else:
        return jsonify({"success": False, "message": "Client not found"}), 404

@app.route(f'{API_PREFIX}/clients', methods=['GET'])
def get_all_clients():
    program_dict = {p.program_id: p.name for p in program_manager.programs}


    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    clients_data = []
    clients = client_manager.clients[offset:offset + limit]
    
    for client in clients:
        enrolled_programs = [program_dict.get(pid, "Unknown Program") for pid in client.program_ids]
        clients_data.append({
            "full_name": client.full_name,
            "age": client.age,
            "gender": client.gender,
            "registered_at": client.registered_at.strftime('%Y-%m-%d %H:%M:%S'),
            "enrolled_programs": enrolled_programs,
            "client_id": client.client_id
        })
    return jsonify({"success": True, "data": clients_data}), 200

@app.route(f'{API_PREFIX}/health-programs', methods=['GET'])
def get_health_programs():
    return jsonify({"success": True, "data": _cached_programs}), 200


@app.errorhandler(404)
def handle_404(error):
    return jsonify({"success": False, "message": "Resource not found"}), 404

@app.errorhandler(400)
def handle_400(error):
    return jsonify({"success": False, "message": str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True)
