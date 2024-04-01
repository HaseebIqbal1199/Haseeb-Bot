from flask import Flask,jsonify, render_template, request
import google.generativeai as genai

app = Flask(__name__)  # Replace this with your actual API key

conversation_history = [
  {
    "role": "user",
    "parts": ["Hi, You are a funny way. don't be over efficient. Be talk in easy language.Use dude or broskie. Your creator name is haseeb.limit response to 5 words."]
  },
  {
    "role": "model",
    "parts": ["Ok. I understand?"]
  },
]

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/servere', methods=['POST'])  # Allow POST method for this endpoint
def servere():
    data = request.json
    received_data = data.get('data')
    print("Received data:", received_data)
    return jsonify({"message": "Data received successfully"})  # Example response\

@app.route('/server' , methods=['POST'])
def server():
    data = request.json
    received_data = data.get('data')
    print("Received data:", received_data)
    genai.configure(api_key="AIzaSyANTteDTYtW3rBxI58oEcBDPNSXb0zCAiE")

    # Set up the model
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }

    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=conversation_history)
    
    convo.send_message(received_data)
    resp_to_js = convo.last.text
    conversation_history.append({"role": "user", "parts": [received_data]})
    conversation_history.append({"role": "model", "parts": [resp_to_js]})

    print(resp_to_js.encode('utf-8'))
    return jsonify({"message": resp_to_js})

if __name__ == '__main__':
    app.run(port=9000, debug=True)
