import json

import requests as requests

import db

STATE_TAX = json.loads(requests.get(
    'https://gist.githubusercontent.com/michaelrbock/a2176b86cb58e2c885898cb426d6933d/raw/6c283bd456856cce0d54642516df80bba1df4008/state-taxes.json').text)

step_id_to_form = {
    '1': 'form_pages/0_marital_status.html',
    '2': 'form_pages/00_number_of_children.html',
    '3': 'form_pages/1_state.html',
    '4': 'form_pages/2_income.html',
    'z': 'results.html',
}


def find_next_step_for_user(user_id, current_step_id):
    return {
        None: '1',
        '1': '2',
        '2': '3',
        '3': '4',
        '4': 'z',
    }[current_step_id]


def update_marital_status(data, val):
    data['is_married'] = val == 'married'


def update_child_count(data, val):
    data['child_count'] = int(val)


def update_state(data, val):
    data['state'] = val


def update_income(data, val):
    data['income'] = float(val)


step_id_to_action = {
    '1': update_marital_status,
    '2': update_child_count,
    '3': update_state,
    '4': update_income,
}


def process_form_submission(user_id, step_id, value, response):
    if len(value) == 0:
        response['error_messages'].append('Please provide a value.')
        return
    user_data_json = db.get_user_data(user_id)
    step_id_to_action[step_id](user_data_json, value)
    db.update_user(user_id, user_data_json)
    print(f'Processed form input for {step_id}. Value is {value}.')
    print(f'    Response: {response}')
    print(f'    User data: {user_data_json}')


def build_form_payload(user_id, step_id, response):
    response['form_payload'] = {}
    if step_id == '3':
        response['form_payload']['choices'] = STATE_TAX
    print(f'Built form for step {step_id}.')
    print(f'    Response: {response}')


def get_taxes(user_id):
    data = db.get_user_data(user_id)
    taxes = {
        'state': 'Unknown',
        'federal': 'Unknown',
    }
    if 'income' in data and 'state' in data:
        income = data['income']
        state = data['state']
        taxes['federal'] = .15 * income
        tax_rate = 0
        for s in STATE_TAX:
            if s['abbreviation'] == state:
                tax_rate = s['tax_rate']
        taxes['state'] = tax_rate * income
    return taxes
