import traceback
from flask import Flask, request, jsonify, abort, Response
from flask_cors import CORS
import traceback
import litellm
import threading
import os, dotenv, time 
import json
dotenv.load_dotenv()

# TODO: set your keys in .env or here:
# os.environ["OPENAI_API_KEY"] = "" # set your openai key here
# see supported models / keys here: https://litellm.readthedocs.io/en/latest/supported/

############ HELPER FUNCTIONS ###################################

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'received!', 200

def data_generator(response):
    for chunk in response:
        yield f"data: {json.dumps(chunk)}\n\n"

@app.route('/chat/completions', methods=["POST"])
def api_completion():
    data = request.json
    start_time = time.time() 
    if data.get('stream') == "True":
        data['stream'] = True # convert to boolean
    try:
        # COMPLETION CALL
        print(f"data: {data}")
        response = litellm.completion(**data)
        print(f"Got Response: {response}")
        if 'stream' in data and data['stream'] == True: # use generate_responses to stream responses
            return Response(data_generator(response), mimetype='text/event-stream')
    except Exception as e:
        # call handle_error function
        print(f"Got Error api_completion(): {traceback.format_exc()}")
        ## LOG FAILURE
        end_time = time.time() 
        # raise e
    return response

"""
expects json data to have the following params:
data = {
    'litellm_request_id': 1234-8801-2222,
    'feedback': 'good'
}
"""
@app.route('/feedback', methods=["POST"])
def store_feedback():
    data = request.json
    try:
        # COMPLETION CALL
        print(f"data: {data}")
        litellm_request_id = data.get("litellm_request_id")
        feedback = data.get("feedback")
        # store_user_feedback 
        

    except Exception as e:
        # call handle_error function
        print(f"Got Error api_completion(): {traceback.format_exc()}")
        ## LOG FAILURE
        end_time = time.time() 
        # raise e
    return {
        "status": "success"
    }

@app.route('/get_models', methods=["POST"])
def get_models():
    try:
        return litellm.model_list
    except Exception as e:
        traceback.print_exc()
        response = {"error": str(e)}
    return response, 200

if __name__ == "__main__":
  from waitress import serve
  serve(app, host="0.0.0.0", port=4000, threads=500)
