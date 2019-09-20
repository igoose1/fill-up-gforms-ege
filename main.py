from selenium import webdriver
import os


'''
    Edit lines below.
'''

FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLScyrlhh0IGxev3S9CKrO8vyX_MkhfLSKCl_2Ux3QZRDo2_DaA/viewform'
driver = webdriver.WebKitGTK()

'''
    Stop editing lines.
'''


xpaths = [
    '/html/body/div/div[2]/form/div/div[2]/div[2]/div[{ind}]/div/div[2]/div/div[1]/div/div[1]/input'.format(
        ind=ind+1
    )
    for ind in range(3)
]

introduction_url = 'file://' + os.path.join(os.getcwd(), 'intro.html')
driver.get(introduction_url)

