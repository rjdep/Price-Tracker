from sys import flags
from bs4 import BeautifulSoup
import requests
import app
import time

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


def flipkartPrice2(aUrl):
    response = requests.get(aUrl, headers=headers)
    doc = BeautifulSoup(response.text, 'html.parser')
    price = doc.find_all('div', {'class': '_30jeq3 _16Jk6d'})
    if price == []:
        return (-1)
    else:
        return (price[0].text.strip())


# sending email-:

import smtplib


def process(stringPrice):
    i = 0
    j = 0
    while stringPrice[i] != '.':
        i += 1
        if i == len(stringPrice):
            break
        if ord(stringPrice[i]) >= ord('0') and ord(stringPrice[i]) <= ord('9'):
            j *= 10
            j += ord(stringPrice[i]) - ord('0')
    return j


def emailSend(mail, aUrl):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('webdevvedbew', 'shyborqjxzuwszom')
    subject = "your product's price is now in your range"
    body = 'Check it now!!'
    msg = f" Subject : {subject}\n{body}\n\n\n{aUrl}"
    server.sendmail(
        'webdevvedbew@gmail.com',
        mail,
        msg
    )
    print("Sent")
    server.quit()
    return


def cancel(email, url, price):
    user = app.User
    db = app.db
    i = 0
    j = 0
    k = 0
    sf1 = ""
    sf2 = ""
    sf3 = ""
    flag = user.query.filter_by(email=email).first()
    a1 = flag.urlString
    a2 = flag.priceString
    a4 = flag.dateString
    a3 = flag.num
    while i < len(a1):
        s1 = ""
        s2 = ""
        s3 = ""
        while a1[i] != '#':
            s1 += a1[i]
            i += 1
        while a2[j] != '#':
            s2 += a2[j]
            j += 1
        while a4[k] != '#':
            s3 += a4[k]
            k += 1

        if s1 == url and int(s2) >= price:
            a3 -= 1
        else:
            sf1 += s1 + '#'
            sf2 += s2 + '#'
            sf3 += s3 + '#'

        i += 1
        j += 1
    flag.urlString = sf1
    flag.priceString = sf2
    flag.dateString = sf3
    flag.num = a3
    db.session.commit()
    return


def decideMail(useremail, fUrl, dprice):
    price = app.flipkartPrice(fUrl)
    print(price)
    price = str(price)
    price += '.'
    price = process(price)
    if price <= dprice:
        emailSend(useremail, fUrl)
        cancel(useremail, fUrl, price)
    return


def fun():
    User = app.User
    complete = User.query.all()
    for man in complete:
        i = 0
        j = 0
        pr = []
        ur = []
        S1 = man.priceString
        S2 = man.urlString
        if not S1 or S1 == []:
            continue
        while i < len(S1):
            s1 = ""
            s2 = ""
            while S1[i] != '#':
                s1 += S1[i]
                i += 1
            while S2[j] != '#':
                s2 += S2[j]
                j += 1
            pr.append(s1)
            ur.append(s2)
            i += 1
            j += 1
        i = 0
        while i < len(pr):
            s1 = pr[i]
            s2 = ur[i]
            email = man.email
            decideMail(email, s2, int(s1))
            i += 1
    return


while True:
    fun()
    time.sleep(30)