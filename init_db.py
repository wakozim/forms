from tinydb import TinyDB, Query


Form = Query()
db = TinyDB('./forms.json')


if not db.search(Form.name == 'user'):
    db.insert({
        'name': 'user',
        'login': 'email',
        'phone': 'phone',
        'registration': 'date',
        'username': 'text'
    })

if not db.search(Form.name == 'event'):
    db.insert({
        'name': 'event',
        'type': 'text',
        'data': 'text',
        'timestamp': 'date'
    })

if not db.search(Form.name == 'state'):
    db.insert({
        'name': 'state',
        'id': 'text'
    })
