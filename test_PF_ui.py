# python -m pytest -v --driver Chrome --driver-path chromedriver.exe
# python -m pytest -v --driver Chrome --driver-path C:/Users/tatik/chromedriver_win32/chromedriver.exe test_PF_ui.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.set_headless(True)
    chrome_options.add_argument('--headless')
    return chrome_options
@pytest.fixture
def driver_pets_chrome(request):
    drivpets = webdriver.Chrome()
    drivpets.get('https://petfriends.skillfactory.ru/login')
    WebDriverWait(drivpets, 10).until(EC.presence_of_element_located((By.ID, "email")))
    drivpets.find_element_by_id("email").send_keys('Vasilisa@mail.ru')
    drivpets.find_element_by_id("pass").send_keys('12345')
    WebDriverWait(drivpets, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                           'button[type="submit"]')))
    drivpets.find_element_by_css_selector('button[type="submit"]').submit()

    return drivpets

    drivpets.quit()


def test_my_pets_info(driver_pets_chrome):
   # Проверяю, что зашла на страницу "Мои питомцы"
   driver_pets_chrome.implicitly_wait(10)
   driver_pets_chrome.find_element_by_xpath('//*[@id="navbarNav"]/ul/li[1]/a').click()
   WebDriverWait(driver_pets_chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   assert driver_pets_chrome.find_element_by_xpath('//body/div[1]/div/div[1]/h2').text == "Vasilisa"

def test_my_pets_stat(driver_pets_chrome):

    # Проверяю, что количество питомцев соответствует указанному в статистике.
    driver_pets_chrome.implicitly_wait(10)
    driver_pets_chrome.find_element_by_xpath('//body/nav/div[1]/ul/li[1]/a').click()
    WebDriverWait(driver_pets_chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
    pets = 'Питомцев: 7'
    pets_text = driver_pets_chrome.find_element_by_xpath('//div[@class=".col-sm-4 left"]')
    assert pets in pets_text.text

def test_my_pets_name_age_animal_type(driver_pets_chrome):

    # Проверяю, что у всех питомцев есть имя, возраст и порода.
    driver_pets_chrome.implicitly_wait(10)
    driver_pets_chrome.find_element_by_xpath('//body/nav/div[1]/ul/li[1]/a').click()
    WebDriverWait(driver_pets_chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
    string = driver_pets_chrome.find_elements_by_xpath('//table[@class ="table table-hover"]/tbody/tr')
    images = driver_pets_chrome.find_elements_by_css_selector('div#all_my_pets>table>tbody>tr>th>img')
    names = driver_pets_chrome.find_elements_by_xpath("//tr/td[1]")
    animal_type = driver_pets_chrome.find_elements_by_xpath('//tr/td[2]')
    age = driver_pets_chrome.find_elements_by_xpath('//tr/td[3]')
    table_pet = driver_pets_chrome.find_elements_by_xpath('//*[@id="all_my_pets"]/table')
    for i in range(len(string)):
        assert names[i].text and animal_type[i].text and age[i].text != ''
        count_nam = len(names)
        count_type = len(animal_type)
        count_age = len(age)
        assert count_type == count_nam
        assert count_nam == count_age

def test_different_names(driver_pets_chrome):

    # Проверяю, что у питомцев разные имена.
    pet_data = driver_pets_chrome.find_elements_by_css_selector('.table.table-hover tbody tr')
    pets_name = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        pets_name.append(split_data_pet[0])
    r = 0
    for i in range(len(pets_name)):
        if pets_name.count(pets_name[i]) > 1:
            r += 1
        assert r == 0

def test_one_pet(driver_pets_chrome):

    # Проверяю, что питомцы не повторяются.
    pet_data = driver_pets_chrome.find_elements_by_css_selector('.table.table-hover tbody tr')
    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '
    list_line = line.split(' ')
    set_list_line = set(list_line)
    a = len(list_line)
    b = len(set_list_line)
    result = a - b
    assert result == 0

def test_photo_more_then_half(driver_pets_chrome):

    # Проверяю, что фото есть больше, чем у половины питомцев.
    driver_pets_chrome.implicitly_wait(10)
    driver_pets_chrome.find_element_by_xpath('//body/nav/div[1]/ul/li[1]/a').click()
    statistic = driver_pets_chrome.find_elements_by_css_selector(".\\.col-sm-4.left")
    images = driver_pets_chrome.find_elements_by_css_selector('.table.table-hover img')
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    half = number // 2
    number_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_photos += 1
    assert number_photos >= half

