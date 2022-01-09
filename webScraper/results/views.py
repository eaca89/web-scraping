from collections import Counter
from django.shortcuts import render
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import requests

new_link_list = []
top_link_list = []
tag_list = []

# new list
def getNewList(keyword):
    new_list = []
    url1 = 'https://api.stackexchange.com/2.3/questions?'
    oneDayAgo = datetime.now() - timedelta(1)
    url2 = 'fromdate='+str(oneDayAgo.date())+'&order=desc&sort=votes&'    
    url3 = 'tagged='+str(keyword)+'&site=stackoverflow'
    response = requests.get(url1 + url2 + url3).json()
    i = 0
    for x in range(len(response['items'])):
        new_list.append("{}- ".format(i+1) + response['items'][x]['title'])
        new_link_list.append(response['items'][x]['link'])
        i += 1
        if (i == 10):
            break
    return new_list

# top list
def getTopList(keyword):
    top_list = []
    oneWeekAgo = datetime.now() - timedelta(7)
    url1 = 'https://api.stackexchange.com/2.3/questions?'
    url2 = 'fromdate='+str(oneWeekAgo.date())+'&order=desc&sort=votes&'    
    url3 = 'tagged='+str(keyword)+'&site=stackoverflow'
    response = requests.get(url1 + url2 + url3).json()    
    i = 0
    for x in range(len(response['items'])):
        top_list.append("{}- ".format(i+1) + response['items'][x]['title'])
        top_link_list.append(response['items'][x]['link'])
        i += 1
        if (i == 10):
            break
    
    # find all tags
    for i in range(len(response['items'])):
        for item in response['items'][i]['tags']:
            tag_list.append(item)
    
    return top_list    

def trends(tagList):
    cnt = Counter(tagList)
    temp = cnt.most_common(5)
    top_five = []
    for item in temp:
        top_five.append('#'+str(item[0]))
    # empty tag_list
    global tag_list
    tag_list = []
    return top_five

def index(request):
    keyword = request.POST.get('keyword')
    
    # if the input is empty, return nothing
    if keyword == '':
        return render(request, 'results/index.html')    
        
    class post:
        def __init__(self, link, id):           
            self.link = link
            self.id = id

    lst1=getNewList(keyword)
    lst2=getTopList(keyword)
    lst3=[]
    lst4=[]
    i=0
    for item in lst1:        
        lst3.append(post(item, i))
        i += 1
    
    i=0
    for item in lst2:        
        lst4.append(post(item, i))
        i += 1

    context = {
        'new_list': lst3,
        'top_list': lst4,
        'tags': trends(tag_list),
    }
    
    return render(request, 'results/index.html', context)

def NewlistItem(request, id):
    context = {}
    link = new_link_list[id]
    r = requests.get(link)
    c = bs(r.content, features="html.parser")
    title = c.find('div', attrs={'id': 'question-header'}).h1.get_text()
    Question = c.find('div', attrs={'class': 'question'}).prettify()
    Answer = c.find('div', attrs={'id': 'answers'}).prettify()    
    context = {
        'title': title,
        'mainQ': Question,
        'thread': Answer,
        'link': link,
    }
    return render(request, 'results/listItem.html', context)

def ToplistItem(request, id):
    context = {}
    link = top_link_list[id]
    r = requests.get(link)
    c = bs(r.content, features="html.parser")
    title = c.find('div', attrs={'id': 'question-header'}).h1.get_text()
    Question = c.find('div', attrs={'class': 'question'}).prettify()
    Answer = c.find('div', attrs={'id': 'answers'}).prettify()    
    context = {
        'title': title,
        'mainQ': Question,
        'thread': Answer,
        'link': link,
    }
    return render(request, 'results/listItem.html', context)
