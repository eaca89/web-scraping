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
    # store the response in the dictionary format
    response = requests.get(url1 + url2 + url3).json()
    return response

def get_top_response(keyword):
    oneWeekAgo = datetime.now() - timedelta(7)
    url1 = 'https://api.stackexchange.com/2.3/questions?'
    url2 = 'fromdate='+str(oneWeekAgo.date())+'&order=desc&sort=votes&'    
    url3 = 'tagged='+str(keyword)+'&site=stackoverflow'
    # store the response in the dictionary format
    response = requests.get(url1 + url2 + url3).json()    
    return response

def get_new_list(keyword):
    # reset the list
    global new_link_list, new_title_list
    new_title_list = []
    new_link_list = []
    response = get_new_response(keyword)

    # if the response is empty, return an empty list
    if 'error_id' in response:
         return []
   
    for x in range(len(response['items'])):
        new_title_list.append("{}- ".format(x+1) + response['items'][x]['title'])
        new_link_list.append(response['items'][x]['link'])
        if (x == 9):
            break

    return new_title_list

def get_top_list(keyword):
    global top_title_list, top_link_list, top_vote_list
    top_title_list = []
    top_link_list = []
    top_vote_list = []

    response = get_top_response(keyword)   
    # if the response is empty, return an empty list
    if 'error_id' in response:
         return []

    for x in range(len(response['items'])):
        top_title_list.append("{}- ".format(x+1) + response['items'][x]['title'])
        top_link_list.append(response['items'][x]['link'])
        top_vote_list.append(response['items'][x]['score'])
        if ( x == 9):
            break
    
    # find all tags
    for i in range(len(response['items'])):
        for item in response['items'][i]['tags']:
            top_tag_list.append(item)
    
    return top_title_list    

def get_trends(tags):
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
    
    new_list = []
    for index, item in enumerate(get_new_list(keyword)):        
        new_list.append(newPost(item, index))

    class topPost:
        def __init__(self, link, id, vote):           
            self.link = link
            self.id = id
            self.vote = vote
        
    top_list = []
    for index, item in enumerate(get_top_list(keyword)):        
        top_list.append(topPost(item, index, top_vote_list[index]))  

    context = {
        'new_list': new_list,
        'top_list': top_list,
        'tags': get_trends(top_tag_list),
    }
    
    return render(request, 'results/index.html', context)

def show_items(request, ch, id):
    context = {}
    
    if ch == 'N':
        link = new_link_list[id]
    elif ch == 'T':
        link = top_link_list[id]

    r = requests.get(link)
    # beautiful soup
    c = bs(r.content, features="html.parser")
    title = c.find('div', attrs={'id': 'question-header'}).h1.get_text()
    Question = c.find('div', attrs={'class': 'question'}).prettify()
    Answers = c.find('div', attrs={'id': 'answers'}).prettify()    
    
    context = {
        'title': title,
        'Question': Question,
        'Answers': Answers,
        'link': link,
    }
    return render(request, 'results/listItem.html', context)