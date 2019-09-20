from selenium import webdriver
from time import sleep


'''

----------------------------
    Edit lines below.

'''

FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLScyrlhh0IGxev3S9CKrO8vyX_MkhfLSKCl_2Ux3QZRDo2_DaA/viewform'
driver = webdriver.WebKitGTK()

'''

    Stop editing lines.
----------------------------

'''


ANSWER_FIELDS = 3

fill_xpaths = [
    '/html/body/div/div[2]/form/div/div[2]/div[2]/div[{ind}]/div/div[2]/div/div[1]/div/div[1]/input'.format(
        ind=ind+1
    )
    for ind in range(ANSWER_FIELDS)
]
send_button_xpath = '/html/body/div/div[2]/form/div/div[2]/div[3]/div[1]/div/div/span'

problem_set_number = input('Задание: ')
start_with = input('Начинать с номера: ')
wait = False
while wait:
    wait = 'y' in input('Вы залогинились в Google [y/n]? ')

driver.get(FORM_URL)
ind = start_with

while True:
    try:
        answer = input('№{}: '.format(ind))
    except KeyboardInterrupt:
        break
    fill_with = [
        problem_set_number,
        ind,
        answer
    ]
    for i in range(ANSWER_FIELDS):
        element = driver.find_element_by_xpath(fill_xpaths[i])
        element.send_keys(fill_with[i])
    send_button_element = driver.find_element_by_xpath(send_button_xpath)
    send_button_element.click()
    driver.get(FORM_URL)
    ind += 1
