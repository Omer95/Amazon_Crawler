#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:50:23 2018

@author: omer farooq ahmed
"""
import random
import bs4
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as soup

links=set()
USER_AGENT_LIST = [
    #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
CONST_URL='https://www.amazon.com/s/ref=nb_sb_ss_c_2_6?url=search-alias%3Dcomputers&field-keywords=laptops&sprefix=laptop%2Caps%2C355&crid=3DC6JC79BTUXG'

def main():
    
    user_agent=gen_user_agent()
    data=scrape_page(url, user_agent)
    #store all links in a set. These links are the next page links at n number of pages
    page_limit=20
    links=fill_links(url, page_limit)
#end main

def scrape_page(url, user_agent):
    html=''
    try:
        headers={'User-Agent':user_agent}
        response=requests.get(url, headers=headers)
        html=response.text
    except:
        print('could not connect to website')
        exit()
    #parse html using beautiful soup
    html_soup=soup(html, 'html.parser')
    laptops=html_soup.findAll("li", {'class':"s-result-item celwidget "})
    #for each laptop, gather its data
    print(str(len(laptops)))
    titles=[]
    for laptop in laptops:
        title=laptop.find('h2', {"class":"a-size-medium s-inline s-access-title a-text-normal"})
        if title is not None:
            title=title.text
            print(title+'\n')
            titles.append(title)
        #end if
    #end for
    print(html_soup)
    return titles

#end scrape_page

#This function fills links to the first n search result pages recursively
def fill_links(url, page_limit):
    page_limit=page_limit-1
    if page_limit<=0:
        return 
    else:
        html=''
        user_agent=gen_user_agent()
        try:
            headers={'User-Agent':user_agent}
            response=requests.get(url, headers=headers)
            html=response.text
        except:
            print('fill links failed. No Connection')
            exit()
        html_soup=soup(html, 'html.parser')
        links_container=html_soup.findAll('span', {'class':'pagnLink'})
        link_container=links_container[0]
        link=link_container.a['href']
        new_url='https://www.'+get_domain(CONST_URL)+link
        links.add(new_url)
        #call function recursively
        fill_links(new_url, page_limit)
    #end if else
#end fill_links
        
# return a random user agent
def gen_user_agent():
    return random.choice(USER_AGENT_LIST)

#get domain
def get_domain(url):
    try:
        results=get_sub_domain(url).split('.')
        return results[-2]+'.'+results[-1]
    except:
        return ''

#get sub domain name
def get_sub_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
    
main()