import pytest
from selenium import webdriver

'''
Requires installation of chromedriver and geckodriver for usage

brew install geckodriver
brew install chromedriver
'''

@pytest.fixture(scope="module")
def safary_browser_instance(request):
	browser = webdriver.Safari(executable_path='/usr/bin/safaridriver')
	yield browser
	browser.close()

@pytest.fixture(scope="module")
def firefox_browser_instance(request):
	options = webdriver.Options()
	options.headless = False
	browser = webdriver.Firefox(executable_path='./geckodriver', options=options)
	yield browser
	browser.close()

@pytest.fixture(scope="module")
def chrome_browser_instance(request):
	options = webdriver.Options()
	options.headless = False
	browser = webdriver.Chrome(executable_path='./chromedriver', options=options)
	yield browser
	browser.close()