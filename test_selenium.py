from selenium import webdriver


def test_index_successful_login():
    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("ronWeasley")

    password = driver.find_element_by_name("password")
    password.send_keys("ualberta123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    header = driver.find_element_by_xpath('//*[@id="accordionSidebar"]/a/div')
    assert header is not None


def test_unsuccessful_login():
    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("yar")

    password = driver.find_element_by_name("password")
    password.send_keys("jessica123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    exists = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[4]/ul/li')
    assert "Sorry, the username and password could not be found." == exists.text

    

