import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

# Create your views here.
BASE_CRAIGSLIST_URL = 'https://sfbay.craigslist.org/search/?query={}'
BASE_CRAIGSLIST_IMAGES = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listing = soup.find_all('li', class_='result-row')

    final_posting_list = []
    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_CRAIGSLIST_IMAGES.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_posting_list.append((post_title, post_url, post_price, post_image_url))

    context = {
        'search': search,
        'final_posting_list': final_posting_list,
    }
    return render(request, 'first_app/new_search.html', context)
