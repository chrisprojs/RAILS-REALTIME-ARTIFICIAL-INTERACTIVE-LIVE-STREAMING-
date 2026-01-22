from flask import Flask, request, jsonify
from flask_cors import CORS
from loader import load_model_and_tokenizer, classify_text_with_loaded_model
from obs_set_input import change_video
import random
import threading
import time

app = Flask(__name__)
CORS(app)

model, tokenizer = load_model_and_tokenizer()
lock = threading.Lock()

global previous_video
previous_video = {"label": None, "video_number": None}

global last_request_time
last_request_time = time.time()

monitor_thread = None
monitor_thread_running = False

def random_label():
    global previous_video
    random_label = 'random'
    video_number = change_video(random_label, previous_video)
    previous_video = {"label": random_label, "video_number": video_number}

def monitor_timeout():
    global last_request_time, monitor_thread_running
    print("monitor timeout is active")
    monitor_thread_running = True
    while True:
        time.sleep(1)  # Check every 2 seconds
        if last_request_time and (time.time() - last_request_time >= 3):  # No requests in the last 10 seconds
            acquired = lock.acquire(timeout=1)
            if acquired:
                try:
                    random_label()
                    last_request_time = time.time()
                finally:
                    lock.release()

@app.route('/classify', methods=['POST'])
def classify_text():
    global previous_video, last_request_time
    
    data = request.json
    input_text = data.get("text")
    acquired = lock.acquire(timeout=50)
    if not acquired:
        return jsonify({"error": "Server is busy. Please try again later."}), 503
    
    try:
        print(f"Received input: {input_text}")

        if input_text:
            label_result = classify_text_with_loaded_model(input_text, model, tokenizer)
            if label_result != previous_video.label:
                video_number = change_video(label_result, previous_video)
                previous_video = {"label": label_result, "video_number": video_number}
                last_request_time = time.time()
                return jsonify({"label": label_result})
            else:
                return jsonify({"error": "Cannot Accept Same Label"}), 502
        else:
            return jsonify({"error": "Invalid input"}), 400  # Ensure response if input_text is empty or None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500  # Generic error handling
    
    finally:
        print("Releasing lock")
        last_request_time = time.time() 
        lock.release()

if __name__ == '__main__':
    if not monitor_thread_running:
        monitor_thread = threading.Thread(target=monitor_timeout, daemon=True)
        monitor_thread.start()
    app.run(debug=True, use_reloader=False)
