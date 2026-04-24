from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load synthetic datasets
with open("incidents.json") as f:
    incidents = json.load(f)

with open("resources.json") as f:
    resources = json.load(f)

@app.route("/api/incidents", methods=["GET"])
def get_incidents():
    return jsonify(incidents)

@app.route("/api/resources", methods=["GET"])
def get_resources():
    return jsonify(resources)

@app.route("/api/allocate", methods=["POST"])
def allocate_resource():
    data = request.json
    incident_type = data.get("type")
    location = data.get("location")

    # Find first available matching resource
    for r in resources:
        if r["type"] == incident_type and r["status"] == "available":
            r["status"] = "dispatched"
            allocation = {
                "incident": data,
                "allocated_resource": r
            }
            return jsonify(allocation)

    return jsonify({"error": "No available resource"}), 404

if __name__ == "__main__":
    app.run(debug=True)
