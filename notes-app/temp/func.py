from parliament import Context
from flask import Request,jsonify
import json
from pymongo import MongoClient, UpdateOne
import os
from bson import ObjectId
import requests


def get_mongo_uri():
    # Get the value of the environment variable or use the default value
    return os.getenv('MONGO_URI', 'mongodb://localhost:27017')
def get_server_url():
    # Get the value of the environment variable or use the default value
    return os.getenv('SERVER_URL', 'http://localhost:3001')


def payload_print(req: Request) -> str:
    if req.method == "POST":
        if req.is_json:

            # open db connection 
            mongo_uri = get_mongo_uri()
            print(mongo_uri)
            client = MongoClient(mongo_uri)
            db = client['notes-db']
            reminders_collection = db['reminders']
            print('db connect',reminders_collection)

            print("REQUEST JSON:- ",req.json)
            # itrating and setting or reminders to expired
            reminder_data_list = req.json
            print("reminder_data_list", reminder_data_list)
            update_operations = []
            for reminder_data in reminder_data_list['reminder']:
                # print ("Each Record: ",ObjectId(reminder_data['_id']))
                query = {'_id': ObjectId(reminder_data['_id'])}
                update_operations.append(UpdateOne(query, {'$set': {'expired': True}}))

            print("update records", update_operations)
            result = reminders_collection.bulk_write(update_operations)

            print(f'{result.modified_count} reminders updated as expired')

            # API CALL
            api_url = get_server_url()+'/emitter'
            for reminder in reminders:
                reminder['expired'] = True
            response = requests.post(api_url, json={'reminder': reminders})
            if response.status_code == 200:
                print('Reminders processed successfully')
                return 'success'
            else:
                print(f'Error processing reminders. Status code: {response.status_code}')
                return 'Internal Server Error'
            return json.dumps(req.json) + "\n"
        else:
            # MultiDict needs some iteration
            ret = "{"

            for key in req.form.keys():
                ret += '"' + key + '": "'+ req.form[key] + '", '

            return ret[:-2] + "}\n" if len(ret) > 2 else "{}"

    elif req.method == "GET":
        # MultiDict needs some iteration
        ret = "{"

        for key in req.args.keys():
            ret += '"' + key + '": "' + req.args[key] + '", '

        return ret[:-2] + "}\n" if len(ret) > 2 else "{}"


def update_reminders_as_expired(reminder_data_list):
    try:
        mongo_uri = get_mongo_uri()
        print(mongo_uri)
        client = MongoClient(mongo_uri)
        db = client['notes-db']
        reminders_collection = db['reminders']
        print('db connect',reminders_collection)
        update_operations = []
        for reminder_data in reminder_data_list:
            print ("iddddd",ObjectId(reminder_data['_id']))
            query = {'_id': ObjectId(reminder_data['_id'])}
            # update_operations.append(UpdateOne(query, {'$set': {'expired': True}}))

        # result = reminders_collection.bulk_write(update_operations)

        # print(f'{result.modified_count} reminders updated as expired')

    except Exception as e:
        print('Error updating reminders as expired:', str(e))

def process_reminder(req: Request):
    if req.method == "POST":
        if req.is_json:
                try:
                    reminders = req.json.get('reminder', [])
                    print(reminders)
                    mongo_uri=get_mongo_uri()
                    print(mongo_uri,"mongouri")
                    # update_reminders_as_expired(reminders)

        #             for reminder in reminders:
        #                 reminder['expired'] = True
        #             api_url = get_server_url()+'/emitter'
        # # api_url = 'http://localhost:3001/emitter'
        #             response = requests.post(api_url, json={'reminder': reminders})

        #             if response.status_code == 200:
        #                 print('Reminders processed successfully')
        #                 return 'success'
        #             else:
        #                 print(f'Error processing reminders. Status code: {response.status_code}')
        #                 return 'Internal Server Error'

                except Exception as e:
                    print('Error processing reminders:', str(e))
                    return  'Internal Server Error'
        else:
            # MultiDict needs some iteration
            ret = "{"

            for key in req.form.keys():
                ret += '"' + key + '": "'+ req.form[key] + '", '

            return ret[:-2] + "}\n" if len(ret) > 2 else "{}"

    elif req.method == "GET":
        # MultiDict needs some iteration

        return "hello world"


# pretty print the request to stdout instantaneously
def pretty_print(req: Request) -> str:
    ret = str(req.method) + ' ' + str(req.url) + ' ' + str(req.host) + '\n'
    for (header, values) in req.headers:
        ret += "  " + str(header) + ": " + values + '\n'

    if req.method == "POST":
        ret += "Request body:\n"
        ret += "  " + payload_print(req) + '\n'

    elif req.method == "GET":
        ret += "URL Query String:\n"
        ret += "  " + payload_print(req) + '\n'

    return ret

 
def main(context: Context):
    """ 
    Function template
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """

    # Add your business logic here
    print("Received request")

    if 'request' in context.keys():
        ret = pretty_print(context.request)
        print(ret, flush=True)
        return  "{}", 200
    else:
        print("Empty request", flush=True)
        return "{}", 200
