from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:8080'}})

TEST = [
    {
    'ID': uuid.uuid4().hex,
    'Name': 'Presidential',
    'Description': 'National',
    'Quantity': '3',
    'StartDate': '07/03/2023', 
    'StartTime': '08:00',
    'EndDate': '07/03/2023',
    'EndTime': '17:00',
    'Fingerprint': '1ej829u&a'
    },
    {
    'ID': uuid.uuid4().hex,
    'Name': 'Congress',
    'Description': 'National',
    'Quantity': '594',
    'StartDate': '26/03/2023', 
    'StartTime': '12:00',
    'EndDate': '28/03/2023',
    'EndTime': '12:00',
    'Fingerprint': '(*!XMe21)'
    },
    {
    'ID': uuid.uuid4().hex,
    'Name': 'Academic Center',
    'Description': 'Small',
    'Quantity': '1',
    'StartDate': '14/04/2023',
    'StartTime': '08:00',
    'EndDate': '14/04/2023',
    'EndTime': '09:00',
    'Fingerprint': '@*Ye9*@Uecm)'
    }
]


@app.route('/', methods=['GET', 'POST'])
def all_elections():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        TEST.append({
            'ID': uuid.uuid1().hex,
            'Name': post_data.get('Name'),
            'Description': post_data.get('Description'),
            'Quantity': post_data.get('Quantity'),
            'StartDate': post_data.get('StartDate'),
            'StartTime': post_data.get('StartTime'),
            'EndDate': post_data.get('EndDate'),
            'EndTime': post_data.get('EndTime')})
        response_object['message'] = 'Election Created!'
    else:
        response_object['elections'] = TEST
    return jsonify(response_object)


@app.route('/<election_id>', methods=['PUT', 'DELETE'])
def single_election(election_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        put_data = request.get_json()
        remove_election(election_id)

        TEST.append({
            'ID': uuid.uuid1().hex,
            'Name': put_data.get('Name'),
            'Description': put_data.get('Description'),
            'Quantity': put_data.get('Quantity'),
            'StartDate': put_data.get('StartDate'),
            'StartTime': put_data.get('StartTime'),
            'EndDate': put_data.get('EndDate'),
            'EndTime': put_data.get('EndTime')})
        
        response_object['message'] = 'Election Updated!'

    if request.method == 'DELETE':
        remove_election(election_id)
        response_object['message'] = 'Election Removed!'

    return jsonify(response_object)


def remove_election(election_id):
    for election in TEST:
        if election['ID'] == election_id:
            TEST.remove(election)
            return True


if __name__ == '__main__':
    app.run(debug=True)
    