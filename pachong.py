__author__ = 'wuhailong 2016-12-16'
import requests
from bs4 import BeautifulSoup
import os
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
all_url = 'http://pubmedcentralcanada.ca/pmcc/articles/PMC3128069/;jsessionid=0CC6B01018E52C5C995F585DBE299DAE.eider?lang=en-ca'
start_html=requests.get(all_url,headers = headers)
#print(start_html.text)
Soup=BeautifulSoup(start_html.text,'lxml')
#li_list=Soup.find_all()
HomeJobTopicString=Soup.find(id="HomeJobTopicPanel")
print(HomeJobTopicString)
#HomeJobTopicElements=BeautifulSoup(str(HomeJobTopicString),'lxml')
#a_list =HomeJobTopicElements.find_all("a",class_="thread_type_1")
#for element in a_list:
#    title=element.get_text()
#    author=BeautifulSoup(str(element.find_next_sibling('span')),'lxml').get_text()
#    href = element['href']
#    print(title.ljust(40,'.')+author.replace('\n','',-1).replace(' ','-').ljust(60,'.')+href)
#    contentt_html=requests.get(href,headers = headers)
#    Content=BeautifulSoup(start_html.text,'lxml')
#    print(contentt_html)
#    print(Content.find_all("div",class_="detail"))