#!/usr/bin/python3
# -*- coding: utf-8 -*-

from grab import Grab
import argparse
import json
import sys


def get_input():
    """
    Parse input line.
    """
    parser = argparse.ArgumentParser(description='Currency converter using daily ECB rates.')
    parser.add_argument("--amount", help="amount which you want to convert - float")
    parser.add_argument("--input_currency", help="input currency - 3 letters name or currency symbol")
    parser.add_argument("--output_currency", help="requested/output currency - 3 letters name or currency symbol")
    args = parser.parse_args()
    symbols = {'$': 'USD', '£': 'GBP', '€': 'EUR', '¥': 'CNY'}
    if args.input_currency in symbols:
        args.input_currency = symbols[args.input_currency]
    if args.output_currency in symbols:
        args.output_currency = symbols[args.output_currency]
    try:
        amount = float(args.amount)
    except ValueError:
        print('Amount must be a number!')
        sys.exit(1)
    return amount, args.input_currency, args.output_currency


def goto(amount, input_currency, output_currency):
    """
    Download exchange rate.
    """
    http = 'http://api.fixer.io/latest?base=' + input_currency
    g.go(http)
    rates = g.response.json
    if 'error' in rates:
        print('Invalid format of input currency!')
        sys.exit(1)
    conversion = {'input' : {'amount': amount, 'currency': input_currency}}
    if output_currency != None:
        if output_currency not in rates['rates']:
            print('Invalid format of output currency!')
            sys.exit(1)
        rate = rates['rates'][output_currency]
        conversion['output'] = {output_currency: float('{:.2f}'.format(amount*rate))}
    else:
        conversion['output'] = {}
        for currency in rates['rates']:
            rate = rates['rates'][currency]
            conversion['output'][currency] = float('{:.2f}'.format(amount*rate))
    print(json.dumps(conversion, indent=4, sort_keys=True))


g = Grab()
amount, input_currency, output_currency = get_input()
goto(amount, input_currency, output_currency)
