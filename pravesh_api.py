from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

tokens_db = {}  

# token generation
@app.route('/register_token', methods=['POST'])
def register_token():
    data = request.get_json()
    token = data.get("token")
    
    if not token:
        return jsonify({"error": "Token missing"}), 400
    
    tokens_db[token] = {
        "BTID": data.get("BTID"),
        "mobile": data.get("mobile"),
        "reason": data.get("reason"),
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify({"message": "Token registered", "token": token}), 200


# Camera Verification
@app.route('/validate_token', methods=['POST'])
def validate_token():
    data = request.get_json()
    token = data.get("token")
    
    if not token:
        return jsonify({"error": "Token missing"}), 400
    
    if token not in tokens_db:
        return jsonify({"error": "Invalid or expired token"}), 404
    
    user_data = tokens_db.pop(token)
    
    return jsonify({
        "BTID": user_data["BTID"],
        "mobile": user_data["mobile"],
        "reason": user_data["reason"],
        "token": token,
        "status": "success"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
