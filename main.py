from data import categories
from products import get_products_from_category
import json

if __name__ == '__main__':
  dataset = {}

  for (category_name, category_id) in categories.items():
    print(f'[*] Started parsing {category_name}')

    products = get_products_from_category(category_id)
    dataset[category_name] = products

    print(f'[+] Success parsing {category_name}')

    with open('./result.json', 'w') as result_file:
      json.dump(dataset, result_file, ensure_ascii=False, sort_keys=True, indent=2)

  print('🚀 Success!')
