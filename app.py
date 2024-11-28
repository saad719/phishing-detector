from flask import Flask, render_template, request, jsonify
import pickle
from features import FeatureExtraction
from features import Urlcheck
import numpy as np
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
app = Flask(__name__)

# Load the model
with open('model/pickle/model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/searchlink')
def index1():
    return render_template('index.html')

@app.route('/searchemail')
def index2():
    return render_template('index2.html')

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

@app.route('/check-email', methods=['POST'])
def extract_links():
    print("check-email endpoint was called")
    """
    Extracts all links (URLs) from the given email text and analyzes each link.
    
    Args:
        - email_text (str): The full email text, received in the POST request.
    
    Returns:
        - JSON response with extracted URLs and analysis result.
    """
    data = request.get_json()
    email = data.get('email')  # Get the email address
    email_text = data.get('emailText')  # Get the email content
    print(email)
    print(email_text)
    if not email or not email_text:
        return jsonify({"error": "Email and email text are required!"}), 400

    # Regular expression for identifying URLs in the email text
    url_pattern = re.compile(
        r'(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))'
    )
    
    # Extract all URLs from the email text
    url_list = list(url_pattern.findall(email_text))
    
    if not url_list:
        return jsonify({"result": "No links found in the email text."})

    # Placeholder logic to analyze each URL (you can replace this with actual link analysis)
    for url in url_list:
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


    
@app.route('/block-sender', methods=['POST'])
def block_sender():
    data = request.json
    sender_email = data.get('email')
    service = authenticate_gmail()
    print("blocking working")
    # Sender email address to block
     # Replace with the email address to block

    # Move existing emails to Trash
    move_existing_emails_to_trash(service, sender_email)

    # Create the filter to move future emails to Trash
    create_filter(service, sender_email)

def authenticate_gmail():
    """Authenticate and create a Gmail API client."""
    SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.modify']
    flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\Dell\Downloads\client_secret_61948592137-vp3t8qksetsfquuc3eros1hh9oakt5he.apps.googleusercontent.com.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def move_existing_emails_to_trash(service, sender_email):
    """Move existing emails from the specified sender to Trash."""
    try:
        # Search for all emails from the sender
        results = service.users().messages().list(userId='me', q=f'from:{sender_email}').execute()
        
        if 'messages' in results:
            for message in results['messages']:
                # Move each email to Trash
                service.users().messages().modify(
                    userId='me', 
                    id=message['id'], 
                    body={'removeLabelIds': ['INBOX'], 'addLabelIds': ['TRASH']}
                ).execute()
            print(f"All existing emails from {sender_email} have been moved to Trash.")
        else:
            print(f"No existing emails found from {sender_email}.")
    
    except Exception as e:
        print(f"An error occurred while moving existing emails to Trash: {e}")

def create_filter(service, sender_email):
    """Create a Gmail filter to send future emails to Trash."""
    filter_settings = {
        'criteria': {
            'from': sender_email  # Specify the sender email address
        },
        'action': {
            'addLabelIds': ['TRASH'],  # Send to Trash
            'removeLabelIds': ['INBOX']  # Remove from Inbox
        }
    }

    try:
        service.users().settings().filters().create(
            userId='me', body=filter_settings
        ).execute()
        print(f"Filter created to send emails from {sender_email} to Trash.")
    except Exception as e:
        print(f"An error occurred while creating the filter: {e}")


    # Block the sender (mock implementation)
    # Integrate with an email provider API to actually block the sender
    response = f"Sender {sender_email} has been blocked."

    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)
