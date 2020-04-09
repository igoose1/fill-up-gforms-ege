#!/usr/bin/env python

# Copyright 2019-2020 Oskar Sharipov
# Copyright 2019 Timur Garaev
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

"""Script for filling up Google Forms by studying in litsey7 ege ICT
lessons."""

import threading
import queue
import time
from selenium import webdriver


# ----------------------------
# Edit lines below.


FORM_URL = (
    'https://docs.google.com/forms/d/e/'
    '1FAIpQLScyrlhh0IGxev3S9CKrO8vyX_MkhfLSKCl_2Ux3QZRDo2_DaA/viewform'
)
DRIVER = webdriver.WebKitGTK

# New design xpaths.
INPUT_FIELD_XPATH_LAYOUT = (
    '/html/body/div/div[2]/form/div/div/div[2]/'
    'div[{index}]/div/div[2]/div/div[1]/div/div[1]/input'
)
SEND_BUTTON_XPATH = '/html/body/div/div[2]/form/div/div/div[3]/div[1]/div/div/span/span'

# Old design xpaths.
# INPUT_FIELD_XPATH_LAYOUT = (
#   '/html/body/div/div[2]/form/div/div[2]/'
#   'div[2]/div[{index}]/div/div[2]/div/div[1]/div/div[1]/input'
# )
# SEND_BUTTON_XPATH = '/html/body/div/div[2]/form/div/div[2]/div[3]/div[1]/div/div/span'

# Stop editing lines.
# ----------------------------

HELP_MESSAGE = '''Скрипт для заполнения Google форм на уроках IT в
Лицее-интернате №7.

При запуске спросит задание и будет ждать входа в аккаунт, проверяя, когда
наконец скрипт сможет оказаться перед формой. Если что-то с этой проверкой
пошло не так (например, с браузера пошли делать что-то другое), перезапустите
скрипт.

Возможные команды:
`@N` -- сменит индекс на N (должно быть целым числом!).
`$ABC` -- сменит задание на ABC.
`?` -- выведет это сообщение.

Также есть стрелочки (`<` или `>`), которые дикрементируют или инкрементируют
индекс.
'''

solutions_queue = queue.Queue()
filling_thread = None


def is_command(string):
    """Check if `string` is the command.

    Parameters
    ----------
    string : str
        The string which should be checked
    """

    return len(string) and string[0] in ('<', '>', '@', '$', '?')


def process_command(string, previous_index, previous_problem_set):
    """Try to execute command if it's possible. If it's not, do nothing.

    Parameters
    ----------
    string : str
        The string of the command which should be executed
    previous_index : int
        Index which was before execution
    previous_problem_set : str
        Problem set which was before execution
    """

    # if command is '?' which means 'show help and do nothing'
    if string[0] == '?':
        print(HELP_MESSAGE)
        return previous_index, previous_problem_set

    # if command is < which means 'decrease index'
    if all(char == '<' for char in string):
        return previous_index - len(string), previous_problem_set

    # if command is > which means 'increase index'
    if all(char == '>' for char in string):
        return previous_index + len(string), previous_problem_set

    # if command is @N which means 'goto N'
    if string[0] == '@' and string[1:].isdigit():
        return int(string[1:]), previous_problem_set

    # if command is $N which means 'goto N problem set and reset index'
    if string[0] == '$' and len(string[1:]):
        return 1, string[1:]

    # if command syntax is wrong
    return previous_index, previous_problem_set


def preload(driver):
    """Load webdriver and ask user of preparameters.

    Parameters
    ----------
    driver
        Selenium webdriver
    """

    driver.get(FORM_URL)
    print(HELP_MESSAGE)
    problem_set_number = input('Задание: ')
    print('Ждем входа в аккаунт Google с доступом к форме...')
    while driver.current_url != FORM_URL:
        time.sleep(.5)
    print('Дождались!')

    return problem_set_number


def fill(driver):
    """Fill up fields to send answer.

    Get new answers in queue to process them in webdriver

    Parameters
    ----------
    driver
        Selenium webdriver
    """

    while True:
        solution = solutions_queue.get()
        if solution is None:
            break

        ANSWER_FIELDS = 3
        fill_xpaths = [
            INPUT_FIELD_XPATH_LAYOUT.format(
                index=index+1
            )
            for index in range(ANSWER_FIELDS)
        ]

        if driver.current_url != FORM_URL:
            driver.get(FORM_URL)
        for i in range(ANSWER_FIELDS):
            element = driver.find_element_by_xpath(fill_xpaths[i])
            element.send_keys(solution[i])
        send_button_element = driver.find_element_by_xpath(SEND_BUTTON_XPATH)
        send_button_element.click()


def rolling(problem_set_number, start_with=1):
    """Ask user of answers.

    Parameters
    ----------

    problem_set_number : str
        Problem set
    start_with : int
        Index at starting of rolling
    """

    index = start_with

    while True:
        answer = input('№{}: '.format(index))
        if is_command(answer):
            index, problem_set_number = process_command(
                answer,
                index,
                problem_set_number
            )
            continue
        if answer == '':
            continue

        solution = [
            problem_set_number,
            index,
            answer
        ]
        solutions_queue.put(solution)
        index += 1


def main():
    """Main function which starts new thread and executes preloading."""
    global filling_thread
    # execute webdriver
    driver = DRIVER()
    problem_set_number = preload(driver)
    filling_thread = threading.Thread(target=fill, args=(driver,))
    filling_thread.start()
    rolling(problem_set_number)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Завершение работы...')
        solutions_queue.put(None)
        filling_thread.join()
        print('Пока <3')
