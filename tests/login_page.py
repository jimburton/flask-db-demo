import pytest
 
from selenium import webdriver
from selenium.webdriver.common.by import By
 
class LoginPage():
    USERNAME_FIELD=(By.ID,"username")
    PASSWORD_FIELD=(By.ID,"password")
    LOGIN_BUTTON=(By.ID,"login_button")
     
    def __init__(self, driver):
        self.driver = driver
     
    async def login(self, username, password):
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
 
    async def get_title(self):
        return self.driver.title
