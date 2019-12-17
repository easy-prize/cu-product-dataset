from data import categories
import csv
import re
import json

with open('./result.json', 'r') as result_file:
  dataset = json.load(result_file, encoding='UTF-8')

mfrs = ['GET', 'HEYROO']
units = ['P', 'L', 'T', 'ml']
lasts = ['g', '입']

products = {}

def is_appendable(product, original_name):
  for p in products[category]:
    if p['name'] == product['name']:
      p['original'].append(original_name)
      return False
  return True

for category in categories.keys():
  products[category] = []

  for product in dataset[category]:
    original_name = product['name']

    segments = product['name'].split(')')
    if len(segments) > 1:
      if '(' not in segments[0]:
        product['name'] = segments[1]

    segments = product['name'].split('(')
    product['name'] = segments[0]

    for mfr in mfrs:
      if mfr in product['name']:
        product['name'] = product['name'].replace(mfr, '')

    for unit in units:
      if unit in product['name']:
        # names like 'PB딸기우유' must not be replaced
        if product['name'].find(unit) > 0:
          product['name'] = product['name'].replace(unit, '')

    # to filter names like '의성마늘프랑크2입'
    for last in lasts:
      if last in product['name']:
        if product['name'][-1:] == last:
          product['name'] = product['name'][:len(product['name']) - 1]

    numbers = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', product['name'])
    if numbers:
      last_number = numbers[-1:][0]
      if product['name'].endswith(last_number):
        product['name'] = product['name'].replace(last_number, '')

    product['name'] = product['name'].strip()

    if is_appendable(product, original_name):
      product['original'] = [original_name]
      products[category].append(product)

with open('./preprocessed.json', 'w') as result_file:
  json.dump(products, result_file, ensure_ascii=False, sort_keys=True, indent=2)

print('🎉 Preprocessed!')

keywords = {}
for category in categories.keys():
  keywords[category] = []

  for product in products[category]:
    keywords[category].append(product['name'])

with open('./output.csv', 'w') as csv_file:
  for key in keywords.keys():
    for product in keywords[key]:
      csv_file.write(f'{key},{product}\n')

print('🏪 Generated Output CSV file!')
