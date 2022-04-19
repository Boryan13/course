from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from flask import Flask, request, render_template

import os, time

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("window-size=1000,600")
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

def open_mathpix():
    try:
        driver.get("https://snip.mathpix.com/")
        inp = driver.find_elements(By.TAG_NAME, "input")
        inp[0].send_keys(os.environ["login"])
        inp[1].send_keys(os.environ["password"])
        driver.find_element(By.TAG_NAME, "button").click()
    except:
        open_mathpix()

def delete_note():
	driver.find_elements(By.TAG_NAME, "svg")[9].click()
	[i for i in driver.find_elements(By.TAG_NAME, "li") if i.text == "Delete Note"][0].click()
	time.sleep(1)
	driver.find_element(By.CLASS_NAME, "button-container").find_elements(By.TAG_NAME, "button")[0].click()

def create_note(flag):
    time.sleep(2)
    driver.find_elements(By.TAG_NAME, "svg")[9].click()
    driver.find_element(By.XPATH, "//input[@id = 'note-name']").send_keys(Keys.ENTER)
    time.sleep(3)
    if flag:
        driver.find_element(By.XPATH, "//input[@name = 'image']").send_keys(os.getcwd() + "/test.png")
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "CodeMirror-code").click()
        base = driver.find_element(By.CLASS_NAME, "CodeMirror-code")
        base.click()
        driver.get(base.text.split("(")[1][:-1])
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL, "C")
        driver.get("https://snip.mathpix.com/")
    else:
        elem = driver.find_element(By.CLASS_NAME, "CodeMirror-code")
        actions = ActionChains(driver)
        actions.move_to_element(elem)
        actions.click(elem) 
        actions.key_down(Keys.CONTROL)
        actions.send_keys('v')
        actions.key_up(Keys.CONTROL)
        actions.perform() 
        time.sleep(5)
        return elem.text

def get_text():
    time.sleep(3)
    delete_note()
    return create_note(False)
	
app = Flask(__name__)
@app.route("/")
def index():
	return render_template("upload.html")

@app.route("/upload", methods = ["POST"])
def upload():
    for file in request.files["file"]:
        with open("test.png", "ab") as photo:
            photo.write(file)
    delete_note()
    create_note(True)	
    os.remove("test.png")
    return render_template("result.html", url_for = get_text())


def main():
	open_mathpix()
	app.run(host = "0.0.0.0", port = 5000)

if __name__ == "__main__":
	main()