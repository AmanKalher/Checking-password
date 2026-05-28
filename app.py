from flask import Flask, render_template, request, jsonify
import os
import time

# This trick forces Flask to use the absolute path of the folder it is currently running in
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# --- YOUR BACKEND CODE PLACEHOLDER ---
def your_cracking_function(target_password):
    start_time = time.time()
    
    # Place your actual Python cracking logic here!
    attempts = len(target_password) * 150 
    guessed_password = target_password    
    
    time_taken = round(time.time() - start_time, 4)
    return guessed_password, attempts, time_taken
# -------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    data = request.json
    user_password = data.get('password')

    guessed, attempts, duration = your_cracking_function(user_password)

    return jsonify({
        "guessed_password": guessed,
        "attempts": attempts,
        "time_taken": duration
    })

if __name__ == '__main__':
    # Using port 5001 in case port 5000 is blocked by your system
    app.run(debug=True, port=5001)
