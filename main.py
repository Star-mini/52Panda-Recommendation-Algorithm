from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def run_algorithm():
    user = request.args.get('user')
    algorithm = request.args.get('algorithm')

    if user and algorithm:
        file_path = f"./{user}/{algorithm}.py"
        try:
            result = subprocess.run(["python", file_path], capture_output=True, text=True)
            return jsonify({"output": result.stdout, "error": result.stderr}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Missing 'user' or 'algorithm' parameter"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
