from flask import Flask, request, jsonify, render_template
from node_manager import add_node, list_nodes, delete_node, schedule_pod, list_pods, delete_pod, start_node, stop_node
import subprocess
from datetime import datetime
from node_manager import update_heartbeat
import threading
import time
from node_manager import check_node_health

app = Flask(__name__)
global node

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_node', methods=['POST'])
def add_node_api():
    try:
        data = request.get_json()
        cpu_cores = data.get('cpu_cores', 1)
        
        if not isinstance(cpu_cores, int) or cpu_cores <= 0:
            return jsonify({'error': 'CPU cores must be a positive whole number'}), 400
            
        node = add_node(cpu_cores)
        
        # Launch Docker container simulating the node
        try:
            subprocess.run([
                "docker", "run", "-d",
                "--name", f"node_{node['id'][:8]}",
                "--env", f"NODE_ID={node['id']}",
                "--env", f"API_SERVER_URL=http://host.docker.internal:5000",
                "node-sim"
            ], check=True)
        except subprocess.CalledProcessError as e:
            delete_node(node['id'])  # Cleanup if container fails to start
            return jsonify({'error': 'Failed to start node container'}), 500

        return jsonify({'message': 'Node added', 'node_id': node['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_nodes', methods=['GET'])
def list_nodes_api():
    return jsonify(list_nodes())

@app.route('/delete_node', methods=['POST'])
def delete_node_api():
    data = request.get_json()
    node_id = data.get('id')
    delete_node(node_id)
    return jsonify({'message': f'Node {node_id} deleted'})

@app.route('/heartbeat', methods=['POST'])
def receive_heartbeat():
    data = request.get_json()
    node_id = data.get('node_id')
    
    if not node_id:
        return jsonify({'error': 'Missing node_id'}), 400

    success = update_heartbeat(node_id)
    if not success:
        return jsonify({'error': 'Node not found'}), 404

    return jsonify({'message': 'Heartbeat received'}), 200

def start_health_monitor():
    def monitor():
        while True:
            check_node_health()
            time.sleep(5)  # check every 5 seconds
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()

start_health_monitor()

@app.route('/schedule_pod', methods=['POST'])
def schedule_pod_api():
    data = request.get_json()
    pod_id = data.get('pod_id')
    cpu_request = data.get('cpu_request')
    strategy = data.get('strategy', 'best_fit')  # default is best_fit now

    if not pod_id or cpu_request is None:
        return jsonify({'error': 'Missing pod_id or cpu_request'}), 400
    
    if not isinstance(cpu_request, int) or cpu_request <= 0:
        return jsonify({'error': 'CPU request must be a positive whole number'}), 400

    result = schedule_pod(pod_id, cpu_request, strategy)

    if result == "duplicate":
        return jsonify({'error': f'Pod with ID {pod_id} already exists'}), 409
    if result is None:
        return jsonify({'error': 'No suitable node found'}), 404

    return jsonify({
        'message': f'Pod scheduled on node {result["id"]}',
        'strategy_used': strategy
    }), 200

@app.route('/list_pods', methods=['GET'])
def list_pods_api():
    return jsonify(list_pods())

@app.route('/delete_pod', methods=['POST'])
def delete_pod_api():
    data = request.get_json()
    pod_id = data.get('pod_id')

    if not pod_id:
        return jsonify({'error': 'Missing pod_id'}), 400

    if delete_pod(pod_id):
        return jsonify({'message': f'Pod {pod_id} deleted successfully'}), 200
    else:
        return jsonify({'error': 'Pod not found'}), 404
    
@app.route('/stop_node', methods=['POST'])
def stop_node_api():
    node_id = request.get_json().get('node_id')
    if stop_node(node_id):
        return jsonify({'message': f'Node {node_id} stopped'}), 200
    return jsonify({'error': 'Node not found'}), 404

@app.route('/start_node', methods=['POST'])
def start_node_api():
    node_id = request.get_json().get('node_id')
    if start_node(node_id):
        return jsonify({'message': f'Node {node_id} started'}), 200
    return jsonify({'error': 'Node not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)