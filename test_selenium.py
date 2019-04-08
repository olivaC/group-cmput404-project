from selenium import webdriver


def test_home():
    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("ronWeasley")

    password = driver.find_element_by_name("password")
    password.send_keys("ualberta123")





