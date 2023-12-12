from flask import Flask, request, jsonify
from pymongo import MongoClient, UpdateOne
from bson import ObjectId
import requests
import os

app = Flask(__name__)

def get_mongo_uri():
    # Get the value of the environment variable or use the default value
    return os.getenv('MONGO_URI', 'mongodb://localhost:27017')
def get_server_url():
    # Get the value of the environment variable or use the default value
    return os.getenv('SERVER_URL', 'http://localhost:3001')

def update_reminders_as_expired(reminder_data_list):
    try:
        mongo_uri = get_mongo_uri()
        client = MongoClient(mongo_uri)
        db = client['notes-db']
        reminders_collection = db['reminders']

        update_operations = []
        for reminder_data in reminder_data_list:
            query = {'_id': ObjectId(reminder_data['_id'])}
            update_operations.append(UpdateOne(query, {'$set': {'expired': True}}))

        result = reminders_collection.bulk_write(update_operations)

        print(f'{result.modified_count} reminders updated as expired')

    except Exception as e:
        print('Error updating reminders as expired:', str(e))
    finally:
        client.close()

@app.route('/',methods=['GET'])
def hello():
    return "hello world"

@app.route('/process', methods=['POST'])
def process_reminder():
    try:
        reminders = request.json.get('reminder', [])
        update_reminders_as_expired(reminders)

        for reminder in reminders:
            reminder['expired'] = True

        server_url = get_server_url()
        api_url = server_url +' /emitter'
        response = requests.post(api_url, json={'reminder': reminders})

        if response.status_code == 200:
            print('Reminders processed successfully')
            return jsonify(reminders), 200
        else:
            print(f'Error processing reminders. Status code: {response.status_code}')
            return jsonify({'error': 'Internal Server Error'}), 500

    except Exception as e:
        print('Error processing reminders:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
