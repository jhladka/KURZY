#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError
import argparse
import json
import sys


def get_input():

    """
    Parse and validate input line.
    """

    # Parse input line:
    parser = argparse.ArgumentParser(description='Currency converter using daily ECB rates.')
    parser.add_argument("--amount", help="amount which you want to convert - float")
    parser.add_argument("--input_currency", help="input currency - 3 letters name or currency symbol")
    parser.add_argument("--output_currency", help="requested/output currency - 3 letters name or currency symbol")
    args = parser.parse_args()

    # Convert a sign to currency code:
    symbols = {
                '$': 'USD',
                '£': 'GBP',
                '€': 'EUR',
                '¥': 'CNY',
                }

    if args.input_currency in symbols:
        args.input_currency = symbols[args.input_currency]
    if args.output_currency in symbols:
        args.output_currency = symbols[args.output_currency]

    # Check if amount is float:
    try:
        amount = float(args.amount)
    except ValueError:
        sys.stderr.write('Amount must be a number!\n')
        sys.exit(1)

    return amount, args.input_currency, args.output_currency


def download_exchange_rates(amount, input_currency, output_currency):

    """
    Download exchange rates from fixer.io
    """

    # Get json response from webpage:
    http = '{0}{1}'.format('http://api.fixer.io/latest?base=', input_currency)
    try:
        r = requests.get(http)
    except ConnectionError:
        sys.stderr.write('Failed to established HTTP connection!\n')
        sys.exit(1)
    rates = r.json()

    # Check if input currency is valid:
    if 'error' in rates:
        if rates['error'] == 'Invalid base':
            sys.stderr.write('Invalid format of input currency!\n')
            sys.exit(1)

    # Setting format of output json:
    conversion = {
            'input': {'amount': amount, 'currency': input_currency},
            'output': {}
            }

    # Output currency is specified:
    if output_currency:

        # Check if output currency is valid:
        if output_currency not in rates['rates']:
            sys.stderr.write('Invalid format of output currency!\n')
            sys.exit(1)

        # Save conversion for specified output currency:
        rate = rates['rates'][output_currency]
        conversion['output'] = {output_currency: amount*rate}
        #conversion['output'] = {output_currency: float('{:.2f}'.format(amount*rate))}


    # Output currency is missing -> conversion to all known currencies:
    else:
        for currency in rates['rates']:
            rate = rates['rates'][currency]
            conversion['output'][currency] = float('{:.2f}'.format(amount*rate))

    # Output:
    sys.stdout.write(json.dumps(conversion, indent=4, sort_keys=True) + '\n')


if __name__ == "__main__":

    amount, input_currency, output_currency = get_input()
    download_exchange_rates(amount, input_currency, output_currency)
