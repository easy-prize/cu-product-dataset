from bs4 import BeautifulSoup
import requests

def get_html(payload):
  res = requests.post('https://cu.bgfretail.com/product/productAjax.do', data=payload)
  return res.text

def get_products(html):
  soup = BeautifulSoup(html, 'html.parser')

  product_htmls = soup.find_all('li')

  products = []

  for product_html in product_htmls:
    try:

      def get_span_text_of_class(class_):
        return product_html.find('p', class_=class_).find('span').string,

      price = get_span_text_of_class('prodPrice')[0]
      price = int(price.replace(',', ''))

      products.append({
        'image': product_html.find('img').get('src'),
        'name': get_span_text_of_class('prodName'),
        'price': price,
      })
    except:
      # print(product_html)
      pass # dummy fragments

  return products
