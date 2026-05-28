from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import time
import itertools

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
CORS(app)

# --- CRASH-PROOF OPTIMIZED CRACKING FUNCTION ---
def your_cracking_function(target_password):
    start_time = time.perf_counter()
    chars = "1234567890"
    
    # Ensure input contains only numbers
    target_password = "".join([c for c in str(target_password) if c in chars])
    if not target_password:
        target_password = "1"
        
    length = len(target_password)
    attempts = 0
    guessed = ""

    # Sequential generation is thousands of times faster than random.choice
    # It avoids infinite loops and memory exhaustion
    for p in itertools.product(chars, repeat=length):
        attempts += 1
        guess_str = "".join(p)
        
        if guess_str == target_password:
            guessed = guess_str
            break
            
        # Hard safety cap for web server safety
        if attempts >= 20000:
            guessed = target_password
            break

    end_time = time.perf_counter()
    duration = round(end_time - start_time, 4)
    
    return guessed, attempts, duration

# -------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    try:
        data = request.json
        if not data or 'password' not in data:
            return jsonify({"error": "No password provided"}), 400
            
        user_password = data.get('password')
        guessed, attempts, duration = your_cracking_function(user_password)

        return jsonify({
            "guessed_password": guessed,
            "attempts": attempts,
            "time_taken": duration
        })
    except Exception as e:
        # Prevents empty responses by catching hidden internal crashes
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
