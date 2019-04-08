from selenium import webdriver
import pytest


@pytest.mark.order1
def test_index_successful_login():
    """
    Tests a successful login.

    :return:
    """
    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("ronWeasley")

    password = driver.find_element_by_name("password")
    password.send_keys("ualberta123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    header = driver.find_element_by_xpath('//*[@id="accordionSidebar"]/a/div')
    assert header is not None


@pytest.mark.order2
def test_unsuccessful_login():
    """
    Tests an unsuccessful login

    :return:
    """
    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("yar")

    password = driver.find_element_by_name("password")
    password.send_keys("jessica123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    exists = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[4]/ul/li')
    assert "Sorry, the username and password could not be found." == exists.text


@pytest.mark.order3
def test_edit_profile():
    """
    Tests editing a profile - username

    :return:
    """
    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("ronWeasley")

    password = driver.find_element_by_name("password")
    password.send_keys("ualberta123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    driver.find_element_by_xpath('//*[@id="userDropdown"]').click()
    driver.find_element_by_xpath('//*[@id="content"]/nav/ul/li[3]/div/a[1]').click()

    displayName = driver.find_element_by_xpath('//*[@id="content"]/div/div/div').text
    assert "ronWeasley" == displayName

    driver.find_element_by_xpath('//*[@id="userDropdown"]').click()
    driver.find_element_by_xpath('//*[@id="content"]/nav/ul/li[3]/div/a[2]').click()

    username = driver.find_element_by_id("id_username")
    username.clear()
    username.send_keys("hermioneGranger")

    driver.find_element_by_xpath('//*[@id="content"]/div/form/button').click()

    displayName = driver.find_element_by_xpath('//*[@id="content"]/div/div/div').text
    assert "hermioneGranger" == displayName

    driver.find_element_by_xpath('//*[@id="userDropdown"]').click()
    driver.find_element_by_xpath('//*[@id="content"]/nav/ul/li[3]/div/a[2]').click()

    username = driver.find_element_by_id("id_username")
    username.clear()
    username.send_keys("ronWeasley")

    driver.find_element_by_xpath('//*[@id="content"]/div/form/button').click()

    displayName = driver.find_element_by_xpath('//*[@id="content"]/div/div/div').text
    assert "ronWeasley" == displayName


@pytest.mark.order4
def test_create_post():
    """
    Tests post can be created - private
    :return:
    """
    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("ronWeasley")

    password = driver.find_element_by_name("password")
    password.send_keys("ualberta123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    driver.find_element_by_xpath('//*[@id="content"]/nav/a[1]').click()

    title = driver.find_element_by_xpath('//*[@id="id_title"]')
    title.send_keys("Selenium Test")

    desc = driver.find_element_by_xpath('//*[@id="id_description"]')
    desc.send_keys("Selenium Description")

    content = driver.find_element_by_xpath('//*[@id="id_text"]')
    content.send_keys("Selenium Test Content")

    driver.find_element_by_xpath('//*[@id="content"]/div/div/form/button').click()

    assert driver.page_source.__contains__("Selenium Test")

    driver.find_element_by_xpath('//*[@id="accordionSidebar"]/li[2]/a').click()

    assert driver.page_source.__contains__("Selenium Test")


@pytest.mark.order5
def test_edit_post():
    """
    Tests editing a post.

    :return:
    """
    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("ronWeasley")

    password = driver.find_element_by_name("password")
    password.send_keys("ualberta123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    driver.find_element_by_xpath('//*[@id="accordionSidebar"]/li[2]/a').click()

    assert driver.page_source.__contains__("Selenium Test")
    assert not driver.page_source.__contains__("Selenium Edit Post")

    driver.find_element_by_link_text('Edit').click()

    title = driver.find_element_by_xpath('//*[@id="id_title"]')
    title.clear()
    title.send_keys("Selenium Edit Post")

    driver.find_element_by_xpath('//*[@id="content"]/div/div/form/button').click()
    assert driver.page_source.__contains__("Selenium Edit Post")


@pytest.mark.order6
def test_comment_post():
    """
    Tests commenting on a post

    :return:
    """

    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("ronWeasley")

    password = driver.find_element_by_name("password")
    password.send_keys("ualberta123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    elements = driver.find_elements_by_link_text('View Comments / Comment')
    elements[0].click()

    comment = driver.find_element_by_xpath('//*[@id="id_comment"]')
    comment.send_keys("Test Comment")

    driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/form/button').click()

    assert driver.page_source.__contains__("Test Comment")


@pytest.mark.order7
def test_delete_post():
    """
    Tests deleting a post

    :return:
    """

    driver = webdriver.Chrome()
    driver.get('https://cmput404group10.herokuapp.com')

    username = driver.find_element_by_id("username")
    username.send_keys("ronWeasley")

    password = driver.find_element_by_name("password")
    password.send_keys("ualberta123")

    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/button').click()

    driver.find_element_by_xpath('//*[@id="accordionSidebar"]/li[2]/a').click()
    assert driver.page_source.__contains__("Selenium Test Content")

    driver.find_element_by_link_text('Delete').click()

    driver.find_element_by_xpath('//*[@id="content"]/div/form/input[2]').click()

    assert not driver.page_source.__contains__("Selenium Test Content")
