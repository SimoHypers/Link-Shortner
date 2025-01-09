import requests


def shorten_link(original_url, url_name):
    API_KEY = '87b15d971ffa5ced2664ddba7caf46e9d8b57'
    BASE_URL = 'https://cutt.ly/api/api.php'

    payload = {
        'key': API_KEY,
        'short': original_url,
        'name': url_name
    }
    request = requests.get(BASE_URL, params=payload)
    data = request.json()
    print('')
    try:
        title = data['url']['title']
        short_link = data['url']['shortLink']

        print(f"Title: {title}")
        print(f"Link: {short_link}")
    except:
        status = data['url']['status']
        print('Error Status', status)

link = input("Enter a link: >> ")
link_name = input("Enter a link name: >> ")

shorten_link(link, link_name)