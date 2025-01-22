from flask import Flask, redirect, request
import os
import time
import random
from cloudevents.http import from_http

app = Flask(__name__)

# Store job status (in a real service, this would be in a database)
jobs = {}

@app.route("/", methods=["POST"])
def event():
    # create a CloudEvent
    event = from_http(request.headers, request.get_data())

    # you can access cloudevent fields as seen below
    print(
        f"Received {event['id']} from {event['source']} with type "
        f"{event['type']} and specversion {event['specversion']}"
    )

    jobs[event['id']] = {
        'job_id': event['id'],
        'status': 'complete',
        'completion_time': time.time(),
    }

    return "", 200

@app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    if job_id not in jobs:
        return "", 404
    
    return redirect(f"{os.getenv('SERVICE_HOST')}/resource/{job_id}", code=301)


@app.route('/resource/<job_id>', methods=['GET'])
def get_resource(job_id):
    # Simulate resource response
    if job_id not in jobs:
        return "", 404

    return jobs[job_id], 200

@app.route('/status/health', methods=['GET'])
def health():
    return "", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
