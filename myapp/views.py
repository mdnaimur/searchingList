from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models
# Create your views here.

#https://bangladesh.craigslist.org/d/books-magazines/search/bka
BASE_CRAIGSLIST_URL = 'https://bangladesh.craigslist.org/search/?query={}'


def home(request):

    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    #print(quote_plus(search))
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    #print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listing = soup.find_all('li', {'class': 'result-row'})

    #post_title = post_listing[0].find(class_='result-title').text
    #post_url = post_listing[0].find('a').get('href')
    #post_price = post_listing[0].find(class_='result-price').text



    final_posting = []

    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price').text
        final_posting.append((post_title, post_url, post_price))

    stuff_for_frontend = {
        'search': search,
        'final_posting': final_posting
    }
    return render(request,'my_app/new_search.html', stuff_for_frontend)
