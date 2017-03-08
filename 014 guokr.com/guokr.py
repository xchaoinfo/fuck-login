# -*- coding: utf-8 -*-

"""
Required
- requests
- bs4
Info
- author: "zhaozhemin"
- email: "zhaozhemyn@gmail.com"
- date: "2017.03.07"
"""

import sys
import os.path
import http.cookiejar

import requests
from bs4 import BeautifulSoup

login_url = ("http://www.guokr.com/sso/"
             "?suppress_prompt=1&lazy=y&success=http%3A%2F%2Fwww.guokr.com%2F")
session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar()
# Opening ``login_url`` will redirect us to the actual page where we
# can retreive some necessary data and make post requests.
resp = session.get(login_url)  # We'll make post requests to ``resp.url``.
soup = BeautifulSoup(resp.text, "html.parser")


def get_csrf_token():
    """
    :rtype: str
    """
    csrf_token = soup.find(id="csrf_token").attrs["value"]
    return csrf_token


def get_captcha_rand():
    """
    :rtype: str
    """
    captcha_rand = soup.find(id="captchaRand").attrs["value"]
    return captcha_rand


def get_captcha_img():
    """
    :rtype: NoneType
    """
    captcha_img_url = soup.find(id="captchaImage").attrs["src"]
    resp = session.get(captcha_img_url, stream=True)
    with open("captcha_img.png", "wb") as f:
        for chunk in resp.iter_content(chunk_size=128):
            f.write(chunk)


def login(url, username, password, csrf_token, captcha, captcha_rand):
    """
    :type url: str
    :type username: str
    :type password: str
    :type csrf_token: str
    :type captcha: str
    :type captcha_rand: str
    :rtype: NoneType
    """
    payload = {
        "username": username,
        "password": password,
        "csrf_token": csrf_token,
        "captcha": captcha,
        "captcha_rand": captcha_rand,
        "permanent": "y"
    }
    try:
        resp = session.post(url, data=payload)
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        soup = BeautifulSoup(resp.text, "html.parser")
        error = soup.find(class_="login-error")
        sys.exit(error.string.strip())


def is_logged_in():
    """
    :rtype: bool
    """
    url = "http://www.guokr.com/settings/profile/"
    resp = session.get(url)
    if "gheaderSettings" in resp.text:
        return True
    else:
        return False


def main():
    """Run the program."""
    csrf_token = get_csrf_token()
    captcha_rand = get_captcha_rand()
    get_captcha_img()
    username = input("Enter username> ")
    password = input("Enter password> ")
    captcha = input("Enter CAPTCHA ({})> "
                    .format(os.path.abspath("captcha_img")))
    login(resp.url, username, password, csrf_token, captcha, captcha_rand)
    if is_logged_in():
        print("You are now logged in.")
    else:
        print("Hmm... Something is wrong.")
    print("Cookies are save in {}".format(os.path.abspath("cookies")))
    session.cookies.save("cookies", ignore_discard=True)


if __name__ == "__main__":
    main()
