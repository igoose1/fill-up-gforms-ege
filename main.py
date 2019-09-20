# Copyright 2019 Oskar Sharipov
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.


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

driver.get(FORM_URL)
problem_set_number = input('Задание: ')
start_with = input('Начинать с номера: ')
wait = True
while wait:
    wait = 'y' not in input('Вы залогинились в Google [y/n]? ')

ind = int(start_with)

while True:
    try:
        driver.get(FORM_URL)
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
    ind += 1
