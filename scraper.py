import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from time import sleep

def get_order_data(order):
    order_title = order.find('div', {'class': 'p_title'}).find('a', {'class': 'ptitle'}).text.strip()
    order_task = order.find('a', {'class': 'descr'}).find_all('span')[1].text.strip()
    order_cost = order.find('a', {'class': 'descr'}).find('b').text[8:].strip()
    order_date = order.find('ul', {'class': 'list-inline'}).find('li').text[8:].strip()
    order_views = int(order.find('ul', {'class': 'list-inline'}).find('li', {'class': 'proj-inf views pull-left'}).text[11:].strip())
    order_answers = int(order.find('ul', {'class': 'list-inline'}).find('li', {'class': 'proj-inf messages pull-left'}).find('i').text.strip())
    order_status = order.find('ul', {'class': 'list-inline'}).find('li', {'class': 'proj-inf status pull-left'}).text.strip()
    
    result = {
        'title': order_title,
        'task': order_task,
        'cost': order_cost,
        'date': order_date,
        'views': order_views,
        'answers': order_answers,
        'status': order_status
    }
    
    return result

url = 'https://freelance.ru/projects/filter/'
proxies = {
    'http': 'http://10.10.0.0.0000',
    'https': 'http://120.10.0.0.0000'
}
headers = {
    'User-agent': generate_user_agent(device_type='desktop', os=('mac', 'linux'))
}

orders = []
page = 1

for i in tqdm(range(50)):
    params = {
        'page': page
    }
    try: 
        response = requests.get(url, params=params, headers=headers, timeout=50)
        if (response.status_code==200):
            bs = BeautifulSoup(response.content)
            page_orders = bs.find('div', {'class': 'projects'}).find_all('div', {'class': 'proj'}, recursive=False)
    
            page_orders = [get_order_data(order) for order in page_orders]
            orders.extend(page_orders)
            page += 1
        else:
            print('It is time to timeout')
            
    except requests.Timeout as e:
        print('It is time to timeout')
        print(str(e))

    except Exception:
        print('Something goes wrong!')

    sleep(20)

df = pd.DataFrame(orders)
df.to_csv('freelanceOrders.csv', index=False)
    