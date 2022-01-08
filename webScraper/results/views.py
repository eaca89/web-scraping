from django.shortcuts import render
from typing import Counter
import requests
from bs4 import BeautifulSoup as bs
from requests.api import head
from collections import Counter

new_link_list = []
top_link_list = []
tag_list = []
# new list
def getNewList(keyword):
    new_list = []
    myurl = 'https://stackoverflow.com/questions/tagged/'+str(keyword)+'?tab=Newest'+str(keyword)
    r = requests.get(myurl)
    new = bs(r.content, features="html.parser")
    summary = new.find_all('div', attrs={'class': 'summary'})
    i = 0
    # new_link_list = []
    for item in summary:
        new_list.append("{}- ".format(i+1) + item.h3.a.string)
        new_link_list.append(item.a['href'])
        i += 1
        if (i == 10):
            break
    return new_list

# top list
def getTopList(keyword):
    top_list = []    
    myurl = 'https://stackoverflow.com/questions/tagged/'+str(keyword)+'?tab=Votes'
    r = requests.get(myurl)
    top = bs(r.content, features="html.parser")
    summary = top.find_all('div', attrs={'class': 'summary'})    
    i = 0
    # top_link_list = []
    for item in summary:
        top_list.append("{}- ".format(i+1) + item.h3.string)
        top_link_list.append(item.a['href'])
        # print(top_link_list[i])
        i += 1
        if (i == 10):
            break
    # find all tags
    tags = top.find_all('div', attrs={'class': 'tags'})
    for tag in tags:
        tag_list.append(tag.a.string)
        
    return top_list    

def trends(tagList):

    cnt = Counter(tagList)
    temp = cnt.most_common(4)
    top_four = []
    for item in temp:
        top_four.append('#'+str(item[0]))
    # empty tag_list
    global tag_list
    tag_list = []
    return top_four

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
    print(tag_list)
    context = {
        'new_list': lst3,
        'top_list': lst4,
        'tags': trends(tag_list),
    }
    
    return render(request, 'results/index.html', context)

def NewlistItem(request, id):
    context = {}
    link = 'https://stackoverflow.com'+new_link_list[id]
    r = requests.get(link)
    c = bs(r.content, features="html.parser")
    Question = c.find('div', attrs={'class': 'question'}).prettify()
    Answer = c.find('div', attrs={'id': 'answers'}).prettify()    
    context = {
        'mainQ': Question,
        'thread': Answer,
        'link': link,
    }
    return render(request, 'results/listItem.html', context)

def ToplistItem(request, id):
    context = {}
    link = 'https://stackoverflow.com'+top_link_list[id]
    r = requests.get(link)
    c = bs(r.content, features="html.parser")
    Question = c.find('div', attrs={'class': 'question'}).prettify()
    Answer = c.find('div', attrs={'id': 'answers'}).prettify()    
    context = {
        'mainQ': Question,
        'thread': Answer,
        'link': link,
    }
    return render(request, 'results/listItem.html', context)