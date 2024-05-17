from flask import jsonify
from app.park import bp
from app.park.algorithm import park_algorithm

@bp.route('/api/park/hello', methods=['GET'])
def hello_park():
    return jsonify({"message": "Hello from park"})

@bp.route('/api/park/recommend', methods=['GET'])
def recommend_park():
    recommendations = park_algorithm()
    return jsonify(recommendations)
