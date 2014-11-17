from selenium import webdriver

b = webdriver.Firefox()
b.get('localhost:8888')

assert 'Django' in b.title
