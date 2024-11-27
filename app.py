from flask import Flask, render_template, request, jsonify
import pickle
from features import FeatureExtraction
from features import Urlcheck
import numpy as np
app = Flask(__name__)

# Load the model
with open('model/pickle/model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-link', methods=['POST'])
def check_link():
    data = request.json
    url = data.get('url')
    
       # Call the PageRank method
    obj1 = Urlcheck(url)
    validity = obj1.getValidity()
    print("validity", validity)
    if validity==0:
        result= "Suspicious"
        print("validity", result)
        return jsonify({'result': result})
    else:
       obj = FeatureExtraction(url)
       x = np.array(obj.getFeaturesList())
       # Predict using the model
       prediction = model.predict([x])[0]
       print(prediction)
       result = "Phishing Link" if prediction == -1 else "Safe Link"

       return jsonify({'result': result})

@app.route('/phishing-details')
def phishing_details():
    return render_template('phishing.html')

@app.route('/block-email', methods=['POST'])
def block_email():
    # Simulate the process of blocking the sender's email
    try:
        # Perform blocking logic here (e.g., call an API, update a database)
        print("Sender blocked.")
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error blocking sender: {e}")
        return jsonify({'success': False})
@app.route('/block-sender', methods=['POST'])
def block_sender():
    data = request.json
    sender_email = data.get('email')

    # Block the sender (mock implementation)
    # Integrate with an email provider API to actually block the sender
    response = f"Sender {sender_email} has been blocked."

    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)
