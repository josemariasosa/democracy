#!/usr/bin/env python
# coding=utf-8

# Movement Admin | Democracy.
# ------------------------------------------------------------------------------
# josemariasosa 🕺

"""
movement = {
    - type:         deposit or withdrawal
    - account:      user account
    - user:         user name
    - currency:     transaction currency
    - total:        transaction total
    - created_at*:   transaction datetime
}
* optional
"""

import json
from datetime import datetime as dt

def insert_movement(movement):
    with open('data/api_db/Movement.json', 'r') as f:
        movements = json.load(f)
    movements.append(movement)
    with open('data/api_db/Movement.json', 'w') as f:
        json.dump(movements, f)

def is_valid_movement(movement):
    required_keys = [
        'type', 
        'account',
        'user',
        'currency',
        'total'
    ]
    return all([x in movement.keys() for x in required_keys])

def formatting_movement(movement):
    if is_valid_movement(movement):
        if 'created_at' not in movement.keys():
            movement['created_at'] = dt.now().__str__()
        return movement
    msg = 'Invalid movement format!'
    raise ValueError(msg)

def create_movement(user, movement):
    movement = formatting_movement(movement)
    insert_movement(movement)

