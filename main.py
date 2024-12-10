import re
import os
from datetime import datetime
from typing import Union, Tuple, Any, List, Dict

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from tinydb import TinyDB, Query


app = FastAPI()

db_filepath = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'forms.json')


def validate_email(email: str) -> bool:
    pattern = r'\w+@\w+\.\w+'
    match = re.fullmatch(pattern, email)
    return match is not None


def validate_phone(phone: str) -> bool:
    pattern = r'\+7 \d\d\d \d\d\d \d\d \d\d'
    match = re.fullmatch(pattern, phone)
    return match is not None


def validate_date(date: str) -> bool:  
    try:
        # check if date match DD.MM.YYYY
        datetime.strptime(date, '%d.%m.%Y') 
        return True
    except ValueError as error:
        pass

    try:
        # check if date match YYYY-MM-DD 
        datetime.strptime(date, '%Y-%m-%d') 
        return True
    except ValueError:
        pass

    return False


def validate_text(text: str) -> bool:
    return True


validate_type_funcs = {
        'email': validate_email,
        'date': validate_date,
        'phone': validate_phone,
        'text': validate_text
}


def check_form(form: Dict[str, str], user_input: Dict[str, str]) -> bool:
    fields = {key: value for key, value in form.items() if key != 'name'}
    
    for field_name, field_type in fields.items():
        is_field_in_user_form = False

        for key, value in user_input.items():
            if field_name != key:
                continue
            validate_value = validate_type_funcs[field_type] 
            if not validate_value(value):
                continue
            is_field_in_user_form = True

        if not is_field_in_user_form:
            return False
    
    return True 


def get_field_type(field: str):
    for field_type, validate_func in validate_type_funcs.items():
        if validate_func(field):
            return field_type


@app.post("/get_form/")
async def read_form(request: Request) -> Union[str, Dict[str, str]]:
    ''' Получение имени формы из базы '''

    user_form = dict(request.query_params)
    with TinyDB(db_filepath) as db: 
        for template in db:
            if check_form(template, user_form):
                return template['name']
    
    response = {}
    for key, value in user_form.items():
        response[key] = get_field_type(value)

    return response 
