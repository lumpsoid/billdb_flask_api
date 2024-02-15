from flask import Blueprint, request, jsonify, current_app
from billdb import Bill
from utils import get_logger

base_path = '/api/flutter'

flutter_app = Blueprint('flutter_app', __name__)

logger = get_logger(__name__)

def bill_as_dict(bill):
    return {
        'timestamp': str(bill.timestamp), 
        'name': bill.name, 
        'date': bill.date, 
        'price': str(bill.price), 
        'currency': bill.currency, 
        'exchange_rate': bill.exchange_rate, 
        'country': bill.country, 
        'items': str(len(bill.items)),
        'link': bill.link,
        'duplicates': len(bill.dup_list)
    }

def parse_error_respons(data, message='parse_error'):
    response = {
        'success': 'parse_error',
        'message': message,
        'force': data['force'],
        'bill': []
    }
    return jsonify(response)

def insert_error_respons(data, message='insert_error'):
    logger.info(message)
    response = {
        'success': 'insert_error',
        'message': message,
        'force': data['force'],
        'bill': []
    }
    return jsonify(response)

def duplicates_respons(data, bill, message='duplicates'):
    response = {
        'success': 'duplicates',
        'message': message,
        'force': data['force'],
        'bill': [bill_as_dict(bill)]
    }
    return jsonify(response)

def success_respons(data, bill, message='success'):
    response = {
        'success': 'success',
        'message': message,
        'force': data['force'],
        'bill': [bill_as_dict(bill)],
    }
    return jsonify(response)


@flutter_app.route(f'{base_path}/qr', methods=['POST'])
def post_qr():
    data = request.get_json()

    qr_link = data.get('link')
    forcefully = True if data.get('force') == 'true' else False

    Bill.connect_to_sqlite(current_app.config['DATABASE_PATH'])
    try:
        bill = Bill().from_qr(qr_link)
    except:
        Bill.close_sqlite()
        return parse_error_respons(data)
    print(bill)
    bill.update_info(
        currency = "rsd",
        country = "serbia",
        exchange_rate = "1",
    )
    try:
        bill.insert(force_dup=forcefully)
    except ValueError as ve:
        Bill.close_sqlite()
        logger.info(ve)
        return insert_error_respons(data, message=f"{ve}")
    Bill.close_sqlite()

    if len(bill.dup_list) > 0 and not forcefully:
        # bill.dup_list
        logger.info('Duplicates found.')
        return duplicates_respons(data, bill)
    logger.info('Successfully added.')
    return success_respons(data, bill)

@flutter_app.route(f'{base_path}/form', methods=['POST'])
def post_form():
    data = request.get_json()

    name = data.get('name')
    date = data.get('date')
    price = data.get('price')
    currency = data.get('currency')
    exchange_rate = data.get('exchange_rate')
    country = data.get('country')
    tags = data.get('tags')
    forcefully = True if data.get('force') == 'true' else False

    if None in (name, date, price, currency, exchange_rate, country, tags,):
        return 'You need to provide: name, date, price, currency, exchange-rate, country, tags'

    Bill.connect_to_sqlite(current_app.config['DATABASE_PATH'])
     
    bill = Bill(
        name=name,
        date=date,
        price=float(price),
        currency=currency,
        exchange_rate=exchange_rate,
        country=country,
        tags=tags
    )
    try:
        bill.insert(force_dup=forcefully)
    except:
        Bill.close_sqlite()
        return insert_error_respons(data)
    Bill.close_sqlite()

    if len(bill.dup_list) > 0 and not forcefully:
        # bill.dup_list
        return duplicates_respons(data, bill)
    
    return success_respons(data, bill)
