from __future__ import unicode_literals, absolute_import, print_function, division
import configparser
import json
import mwclient
from mwclient import errors
import requests
import re
import time
from sopel.module import rule, commands, example


pages = ''


def save_wrap(site, requester, status):
    page = site.Pages['User:' + requester + '/Status']
    content = status
    save_edit(page, content)


def save_edit(page, content):
    time.sleep(5)
    edit_summary = """BOT: Settings status per request """
    times = 0
    while True:
        if times > 1:
            break
        try:
            page.save(content, summary=edit_summary, bot=True, minor=True)
            print('Line 27')
        except errors.ProtectedPageError:
            print('Could not edit ' + page + ' due to protection')
            times += 1
        except errors.EditError:
            print("Error")
            times += 1
            time.sleep(5)  # sleep for 5 seconds before trying again
            continue
        break


def main(wiki, requester, status):
    wikiurl = 'example.org'
    file = open('/data/project/zppixbot/.sopel/modules/config/statuswikis.csv', 'r')
    for line in file:
        data = line.split(',')
        if data[1] == wiki:
            wikiurl = data[0]
    site = mwclient.Site(('https', wikiurl), '/w/')
    config = configparser.RawConfigParser()
    config.read('/data/project/zppixbot/.sopel/credentials.txt')
    try:
        site.login(config.get('zppixbot_status', 'username'), config.get('zppixbot_status', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")
    save_wrap(site, requester, status)


@commands('status')
@example('.status mhtest offline')
def status(bot, trigger):
    try:
        options = trigger.group(2).split(" ")
        if len(options) == 2:
            wiki = options[0]
            status = options[1]
            host = trigger.host
            host = host.split('/')
            if host[0] == 'miraheze':
                requester = host[1]
                main(wiki, requester, status)
    except AttributeError:
        bot.say('Syntax: .mh wiki page', trigger.sender)