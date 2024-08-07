from flask import Flask, jsonify, send_from_directory, request
import json
import os

app = Flask(__name__, static_url_path='')

# File to store bin data
DATA_FILE = 'bins_data.json'

# Initialize the JSON file if it doesn't exist
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        initial_data = {
            "statuses": ["empty"] * 11,
            "names": [f"Bin {i+1}" for i in range(11)]
        }
        with open(DATA_FILE, 'w') as file:
            json.dump(initial_data, file)

# Load bin data from the file
def load_bins():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return data['statuses'], data['names']
    else:
        return [], []

# Save bin data to the file
def save_bins(statuses, names):
    with open(DATA_FILE, 'w') as file:
        json.dump({'statuses': statuses, 'names': names}, file)

# Initialize data file if it doesn't exist
initialize_data_file()

# Load bins data initially
bin_statuses, bin_names = load_bins()

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"statuses": bin_statuses, "names": bin_names})

@app.route("/set_status", methods=["POST"])
def set_status():
    index = request.json.get("index")
    status = request.json.get("status")
    if index is not None and 0 <= index < len(bin_statuses) and status in ["full", "empty"]:
        bin_statuses[index] = status
        save_bins(bin_statuses, bin_names)
        return jsonify({"message": f"Bin {bin_names[index]} status set to {status}"})
    else:
        return jsonify({"message": "Invalid status or index"}), 400

@app.route("/add_bin", methods=["POST"])
def add_bin():
    name = request.json.get("name")
    if name:
        bin_statuses.append("empty")
        bin_names.append(name)
        save_bins(bin_statuses, bin_names)
        return jsonify({"message": f"Bin '{name}' added successfully"}), 200
    return jsonify({"message": "Bin name is required"}), 400

@app.route("/delete_bin", methods=["DELETE"])
def delete_bin():
    index = request.json.get("index")
    if index is not None and 0 <= int(index) < len(bin_statuses):
        del bin_statuses[int(index)]
        del bin_names[int(index)]
        save_bins(bin_statuses, bin_names)
        return jsonify({"message": f"Bin {int(index) + 1} deleted successfully"}), 200
    return jsonify({"message": "Invalid bin index"}), 400

@app.route("/delete_all_bins", methods=["DELETE"])
def delete_all_bins():
    global bin_statuses, bin_names  # Ensure you're modifying the global variables
    bin_statuses = []  # Clear the list of statuses
    bin_names = []  # Clear the list of names
    save_bins(bin_statuses, bin_names)  # Save the now empty lists to the file
    return jsonify({"message": "All bins deleted successfully"}), 200

@app.route("/bins", methods=["GET"])
def get_bins():
    bins = [{"index": i, "name": bin_names[i], "status": bin_statuses[i]} for i in range(len(bin_statuses))]
    return jsonify(bins)

@app.route("/")
def home():
    return send_from_directory('.', 'home.html')

@app.route("/status_page")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/allbins_page")
def allbins():
    return send_from_directory('.', 'allbins.html')

@app.route("/manage_bins_page")
def manage_bins():
    return send_from_directory('.', 'manage_bins.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)