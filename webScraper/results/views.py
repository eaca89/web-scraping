from collections import Counter
from django.shortcuts import render
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import requests

new_title_list =[]
new_link_list = []
top_title_list = []
top_link_list = []
top_vote_list = []
top_tag_list = []

def get_new_response(keyword):
    url1 = 'https://api.stackexchange.com/2.3/questions?'
    oneDayAgo = datetime.now() - timedelta(1)
    url2 = 'fromdate='+str(oneDayAgo.date())+'&order=desc&sort=creation&'    
    url3 = 'tagged='+str(keyword)+'&site=stackoverflow'
    response = requests.get(url1 + url2 + url3).json()
    return response

def get_top_response(keyword):
    oneWeekAgo = datetime.now() - timedelta(7)
    url1 = 'https://api.stackexchange.com/2.3/questions?'
    url2 = 'fromdate='+str(oneWeekAgo.date())+'&order=desc&sort=votes&'    
    url3 = 'tagged='+str(keyword)+'&site=stackoverflow'
    response = requests.get(url1 + url2 + url3).json()
    return response

def get_new_list(keyword):
    # reset the list
    global new_link_list, new_title_list
    new_title_list = []
    new_link_list = []
    response = get_new_response(keyword)
    # print('%%%%%%%%%%%%%%%%%%%%%%')
    # print(response)
    # if the response is empty, return an empty list
    if 'error_id' in response:
         return []

    i = 0    
    for x in range(len(response['items'])):
        new_title_list.append("{}- ".format(i+1) + response['items'][x]['title'])
        new_link_list.append(response['items'][x]['link'])
        i += 1
        if (i == 10):
            break

    return new_title_list

def get_top_list(keyword):
    global top_title_list, top_link_list, top_vote_list
    top_title_list = []
    top_link_list = []
    top_vote_list = []

    response = get_top_response(keyword)
    # print('%%%%%%%%%%%%%%%%%%%%%%')
    # print(response)
    # if the response is empty, return an empty list
    if 'error_id' in response:
         return []

    i = 0
    for x in range(len(response['items'])):
        top_title_list.append("{}- ".format(i+1) + response['items'][x]['title'])
        top_link_list.append(response['items'][x]['link'])
        top_vote_list.append(response['items'][x]['score'])
        i += 1
        if (i == 10):
            break
    
    # find all tags
    for i in range(len(response['items'])):
        for item in response['items'][i]['tags']:
            top_tag_list.append(item)
    
    return top_title_list    

def trends(tags):
    cnt = Counter(tags)
    temp = cnt.most_common(5)
    top_five = []
    for item in temp:
        top_five.append('#'+str(item[0]))
    # empty tag_list
    global top_tag_list
    top_tag_list = []
    return top_five

def index(request):
    keyword = request.POST.get('keyword')
    
    # if the input is empty, return nothing
    if keyword == '':
        return render(request, 'results/index.html')    

    class newPost:
        def __init__(self, link, id):           
            self.link = link
            self.id = id
    lst1=get_new_list(keyword)
    lst2=[]
    i=0
    for item in lst1:        
        lst2.append(newPost(item, i))
        i += 1

    class topPost:
        def __init__(self, link, id, vote):           
            self.link = link
            self.id = id
            self.vote = vote

    
    lst3=get_top_list(keyword)    
    lst4=[]
        
    i=0
    for item in lst3:        
        lst4.append(topPost(item, i, top_vote_list[i]))
        i += 1   

    context = {
        'new_list': lst2,
        'top_list': lst4,
        'tags': trends(top_tag_list),
    }
    
    return render(request, 'results/index.html', context)

def new_list_item(request, id):
    context = {}
    link = new_link_list[id]
    r = requests.get(link)
    # beautiful soup
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

def top_list_item(request, id):
    context = {}
    link = top_link_list[id]
    r = requests.get(link)
    # beautiful soup
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
