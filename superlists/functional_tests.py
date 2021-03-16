from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("user-data-dir=C:\\Users\\poku.flacko\\AppData\\Local\Google\\Chrome\\User Data\\Default")

browser = webdriver.Chrome(executable_path="C:\\Users\\poku.flacko\\Downloads\\Applications\\chromedriver_win32\\chromedriver.exe", options=options)
browser.get('http://localhost:8000')

assert 'Django' in browser.title
