from parliament import Context, event
from pymongo import MongoClient, UpdateOne
import os
from bson import ObjectId
from cloudevents.conversion import to_structured
from cloudevents.http import CloudEvent
from flask import jsonify

def get_mongo_uri():
    # Get the value of the environment variable or use the default value
    return os.getenv('MONGO_URI', 'mongodb://localhost:27017')

def update_db(reminder_data_list):
    mongo_uri = get_mongo_uri()
    print(mongo_uri)
    client = MongoClient(mongo_uri)
    db = client['notes-db']
    reminders_collection = db['reminders']
    print('db connect',reminders_collection)
    print("reminder_data_list", reminder_data_list)
    update_operations = []
    for reminder_data in reminder_data_list:
        # print ("Each Record: ",ObjectId(reminder_data['_id']))
        query = {'_id': ObjectId(reminder_data['_id'])}
        update_operations.append(UpdateOne(query, {'$set': {'expired': True}}))

    print("update records", update_operations)
    result = reminders_collection.bulk_write(update_operations)

    print(f'{result.modified_count} reminders updated as expired')

    for reminder in reminder_data_list:
        reminder['expired'] = True
    return reminder_data_list

@event
def main(context: Context):
    """
    Function template
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """
    print(context.request,"asdasdas")
    print(context.cloud_event.data)
    # Add your business logic here
    # The return value here will be applied as the data attribute
    # of a CloudEvent returned to the function invoker
    if context.cloud_event.data is None or not context.cloud_event.data:
         return jsonify({})
    reminder_data= update_db(context.cloud_event.data)
    attributes = {
    "type": "services-res",
    "source": "emitter-ce",
    }

    # Set the content type to application/json
    attributes["datacontenttype"] = "application/json"

    event = CloudEvent(attributes, reminder_data)
    print("event:",event)
    # Creates the HTTP request representation of the CloudEvent in structured content mode
    # headers, event_data = to_structured(event)
    # print("event:",event_data)
    return event
