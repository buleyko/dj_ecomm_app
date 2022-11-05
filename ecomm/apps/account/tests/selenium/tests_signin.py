import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def take_screenshot(driver, name):
    time.sleep(1)
    os.makedirs(os.path.join("screenshot", os.path.dirname(name)), exist_ok=True)
    driver.save_screenshot(os.path.join("screenshot", name))


@pytest.mark.selenium
def test_account_signin(live_server, create_admin_user, create_test_fnd, safary_browser_instance):
	browser = safary_browser_instance
	# live_server_url + reverse('fnd:home')
	browser.get(f'{live_server.url}/account/signin/')
	user_email = browser.find_element(By.NAME, 'email')
	user_password = browser.find_element(By.NAME, 'password')
	submit = browser.find_element(By.XPATH, '//button[@type="submit"]')
	time.sleep(1)
	user_email.send_keys('admin@mail.com')
	user_password.send_keys('password')
	submit.send_keys(Keys.RETURN)
	time.sleep(1)
	assert 'Dashboard' in browser.page_source


@pytest.mark.screenshot
def test_screenshot_dashboard_page(live_server, create_admin_user, create_test_fnd, safary_browser_instance):
	browser = safary_browser_instance
	browser.get(f'{live_server.url}/account/signin/')
	user_email = browser.find_element(By.NAME, 'email')
	user_password = browser.find_element(By.NAME, 'password')
	submit = browser.find_element(By.XPATH, '//button[@type="submit"]')
	time.sleep(1)
	user_email.send_keys('admin@mail.com')
	user_password.send_keys('password')
	submit.send_keys(Keys.RETURN)
	time.sleep(1)
	take_screenshot(browser, 'test_screenshot_dashboard_page.png')
	assert 'Dashboard' in browser.page_source