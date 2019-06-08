from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils2 import fetch_reply
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    #Store in database
    connectDB(msg, sender)

    # Create reply
    resp = MessagingResponse()
    resp.message(fetch_reply(msg, sender))

    return str(resp)

def connectDB(msg, sender):
    client = MongoClient("mongodb+srv://test:test@cluster0-kmp6d.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('bot_db')
    records = db.bot_records
    new_item = {
        'msg': msg,
        'sender': sender
    }
    records.insert_one(new_item)


if __name__ == "__main__":
    app.run(debug=True)