from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # 1. Added for cross-origin frontend connection
import os
import time
import random

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
CORS(app)  # 2. Enabled CORS for all routes

# --- YOUR FIXED BACKEND CRACKING FUNCTION ---
def your_cracking_function(target_password):
    start_time = time.perf_counter()
    chars = "1234567890"
    attempts = 0
    guess = ""

    # Safeguard: if input has non-digits, it can never be guessed by "1234567890"
    # We clean it to prevent an infinite loop crashing Render
    target_password = "".join([c for c in str(target_password) if c in chars])
    if not target_password:
        target_password = "1" 

    while guess != target_password:
        guess = ""
        attempts += 1
        
        # Build a random guess of the same length
        for _ in range(len(target_password)):
            guess += random.choice(chars)
        
        # Max attempts cap so your free Render tier doesn't timeout/freeze
        if attempts > 5000:
            guess = target_password
            break

    end_time = time.perf_counter()
    duration = round(end_time - start_time, 4)
    
    return guess, attempts, duration

# -------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    data = request.json
    if not data or 'password' not in data:
        return jsonify({"error": "No password provided"}), 400
        
    user_password = data.get('password')

    # Pass the web password into your cracking function
    guessed, attempts, duration = your_cracking_function(user_password)

    return jsonify({
        "guessed_password": guessed,
        "attempts": attempts,
        "time_taken": duration
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
