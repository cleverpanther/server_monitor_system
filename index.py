from flask import Flask, request, jsonify
import psutil
import requests

app = Flask(__name__)

PROMETHEUS_URL = "http://localhost:9090"

def query_prometheus(query, start, end, step):
    url = f"{PROMETHEUS_URL}/api/v1/query_range"
    params = {
        'query': query,
        'start': start,
        'end': end,
        'step': step
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

@app.route('/api/historical/cpu', methods = ['GET'])
def get_cpu_usage():
    start = request.args.get('start')
    end = request.args.get('end')
    step = request.args.get('step', '60s')
    data = query_prometheus('server_cpu_usage', start, end, step)
    return jsonify(data)

@app.route('/api/historical/ram', methods = ['GET'])
def get_ram_usage():
    start = request.args.get('start')
    end = request.args.get('end')
    step = request.args.get('step', '60s')
    data = query_prometheus('server_memory_usage', start, end, step)
    return jsonify(data)

@app.route('/api/historical/disk', methods = ['GET'])
def get_disk_usage():
    start = request.args.get('start')
    end = request.args.get('end')
    step = request.args.get('step', '60s')
    data = query_prometheus('server_disk_usage', start, end, step)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)