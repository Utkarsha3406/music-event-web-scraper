import time
import requests
import selectorlib as selectorlib
import smtplib, ssl
import os



URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    sender = os.getenv("sender")
    receiver = os.getenv("receiver")
    password = os.getenv("password")

    username = "here_goes_your_gmail"
    password = "here_goes_your_gmail_password"

    receiver = "here_goes_your_gmail"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.ehlo_or_helo_if_needed()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
    print("Email was sent")

def store(extracted):
    with open("data.txt","a") as file:
        file.write(extracted + "\n")

def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


if __name__=="__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="Hey ,new event was found")
        time.sleep(2)