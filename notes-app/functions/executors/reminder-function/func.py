from flask import Flask, Request, jsonify
from pymongo import MongoClient, UpdateOne
from bson import ObjectId
import requests
from parliament import Context
import os

def get_mongo_uri():
    # Get the value of the environment variable or use the default value
    return os.getenv('MONGO_URI', 'mongodb://localhost:27017')
def get_server_url():
    # Get the value of the environment variable or use the default value
    return os.getenv('SERVER_URL', 'http://localhost:3001')

def update_reminders_as_expired(reminder_data_list, client):
    try:
        db = client['notes-db']
        reminders_collection = db['reminders']

        update_operations = []
        for reminder_data in reminder_data_list:
            print ("iddddd",ObjectId(reminder_data['_id']['$oid']))
            query = {'_id': ObjectId(reminder_data['_id']['$oid'])}
            update_operations.append(UpdateOne(query, {'$set': {'expired': True}}))

        result = reminders_collection.bulk_write(update_operations)

        print(f'{result.modified_count} reminders updated as expired')

    except Exception as e:
        print('Error updating reminders as expired:', str(e))

def process_reminder(request: Request):
    try:
        reminders = request.json.get('reminder', [])
        print(reminders)
        mongo_uri=get_mongo_uri()
        update_reminders_as_expired(reminders, MongoClient(mongo_uri))

        for reminder in reminders:
            reminder['expired'] = True
        api_url = get_server_url()+'/emitter'
        # api_url = 'http://localhost:3001/emitter'
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

def main(context: Context):
    print(context.request.method,context.request.path)
    if context.request.method == "GET":
        return "hello world", 200
    elif context.request.method == "POST":
        return process_reminder(context.request)
    else:
        return "Invalid endpoint or method", 400
