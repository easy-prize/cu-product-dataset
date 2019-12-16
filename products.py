from parser import get_html, get_products
from itertools import count

def get_products_from_category(category_id):
  products = []
  payload = {
    'pageIndex': 0,
    'searchMainCategory': category_id,
    'searchCondition': 'setA',
    'gdIdx': 0,
    'codeParent': category_id,
  }

  for idx in count(1):
    print(f'[*] Fetching data from Category {category_id}, {idx}th page...')
    payload['pageIndex'] += 1
    html = get_html(payload)

    if '조회된 상품이 없습니다.' in html:
      break

    products += get_products(html)

  return products
