import time, re, sys, imp, wget, os, shelve, datetime
from compare_img import hasPhoto, removeJunkFiles
from splinter import Browser
from mai_conf import *

SEARCH_MEN_BY_WOMAN_ID_URL = 'http://office.loveme.com/search_men/?women_id='

browser = Browser('firefox')


def loginToSite():
    login_url = 'http://office.loveme.com/login'
    browser.visit(login_url)
    browser.fill('logins_ident', LOGIN)
    browser.fill('logins_password', PASSWORD)
    browser.find_by_css('.r button').click()
    time.sleep(1)


def getAllGirlsIdsOnPage():
    ids = []
    idLinks = browser.find_by_css('p a.link_options')
    for idLink in idLinks:
        ids.append(idLink['id'])
    return ids


def getAllGirlsIds():
    browser.visit('http://office.loveme.com/assign_women')
    girlsIds = []
    girls_page_url = 'http://office.loveme.com/assign_women~pg'
    page_to_visit = 2
    while (noErrorDivs()):
        girlsIds.extend(getAllGirlsIdsOnPage())
        browser.visit(girls_page_url + str(page_to_visit))
        page_to_visit += 1
    return girlsIds


def getMenWithPhotosOnPage():
    men_links = browser.find_by_css('.profile_wide a.in_bl')[1:]
    men_photo_links = browser.find_by_css('.profile_wide img.nice_brd')[1:]
    men_send_intro_links = browser.find_by_css('li.a_center')

    men_info = []
    findIdRe = r'[0-9]+$'

    for i in range(len(men_links)):
        man_id = re.findall(findIdRe, men_links[i]['href'])[0]
        man_name = men_links[i]['title']
        man_photo_url = men_photo_links[i]['src']
        man_send_intro_link = men_send_intro_links[i].html

        photoQuestion = not ONLY_WITH_PHOTOS or hasPhoto(man_photo_url)

        if photoQuestion and hasSendLinkActive(man_send_intro_link):
            man = {}
            man[man_id] = {}
            man[man_id]['name'] = man_name
            man[man_id]['photo_url'] = man_photo_url
            men_info.append(man)

    removeJunkFiles()
    return men_info


def hasSendLinkActive(str):
    # TODO: add better condition
    return len(str) > 15


def moveToNextPage(girl_id, page_num):
    g_min = GIRLS_WITH_INTRO_LETTERS[girl_id]['min']
    g_max = GIRLS_WITH_INTRO_LETTERS[girl_id]['max']
    url = 'http://office.loveme.com/search_men_results~pg%s?q=age_from-%s--age_to-%s&women_id=%s' % (
    page_num, g_min, g_max, girl_id)
    browser.visit(url)


def isIntroAllowed():
    not_allowed_div = browser.find_by_css('#msg_intro_not_allowed')
    if (not_allowed_div == []):
        return True
    return False


def noErrorDivs():
    error_div = browser.find_by_css('.error_msg')
    if (error_div == []):
        return True
    return False


def messageAlreadySent():
    error_div = browser.find_by_css('#msg_intro_already_sent')
    if (error_div == []):
        return False
    return True


def selectPhotoAndSubmit():
    browser.find_by_css('#choose_photos_attached').click()
    browser.find_by_name('fk_files[]').first.click()
    if (not DEBUG):
        browser.find_by_name('btn_submit').click()


def incrementSentLettersForGirl(girl_id):
    db = shelve.open('girls-conf')
    count = db[girl_id]['letters_sent']
    name = db[girl_id]['name']
    min = db[girl_id]['min']
    max = db[girl_id]['max']
    count += 1
    db[girl_id] = {
        'letters_sent': count,
        'min': min,
        'max': max,
        'name': name
    }
    db.close()


def gotSentLettersLimit(girl_id, limit):
    db = shelve.open('girls-conf')
    sent = db[girl_id]['letters_sent']
    db.close()
    print 'Sent ' + str(sent) + ' : ' + 'Limit ' + str(limit)
    return sent >= limit


def sendLettersForGirl(girl_id, number_of_letters_to_send, page_to_start=2):
    if gotSentLettersLimit(girl_id, number_of_letters_to_send):
        return page_to_start

    browser.visit(SEARCH_MEN_BY_WOMAN_ID_URL + girl_id)

    man_age_min = GIRLS_WITH_INTRO_LETTERS[girl_id]['min']
    man_age_max = GIRLS_WITH_INTRO_LETTERS[girl_id]['max']

    browser.select('age_from', man_age_min)
    browser.select('age_to', man_age_max)

    browser.find_by_name('btn_submit').click()

    if LAST_LOGIN_SORT_ORDER:
        browser.select('search_sort', 'profile_last_activity')

    letters_sent = 0

    page_to_visit = page_to_start

    while (letters_sent < number_of_letters_to_send):
        wait_for_ajax()
        men_on_page = getMenWithPhotosOnPage()

        for man in men_on_page:
            man_id = man.keys()[0]
            browser.visit('http://office.loveme.com/send?mid=%s&wid=%s' % (man_id, girl_id))
            if isIntroAllowed():
                if messageAlreadySent():
                    continue
                selectPhotoAndSubmit()
                letters_sent += 1
                # TODO: update girls message counter in base
                incrementSentLettersForGirl(girl_id)

                # check if girl has reached her limit of letters
                # if so return
                if gotSentLettersLimit(girl_id, number_of_letters_to_send):
                    return page_to_visit

                print 'I have sent letter number %s from girl %s to man %s' % (letters_sent, str(girl_id), str(man_id))
                if (letters_sent >= number_of_letters_to_send):
                    break
            else:
                print 'Intro for ' + str(man_id) + ' not allowed'

        # move to next page
        moveToNextPage(girl_id, page_to_visit)
        page_to_visit += 1

    return page_to_visit


def wait_for_ajax():
    while True:
        if browser.evaluate_script('jQuery.active') == 0:
            break
        print 'AJAX'
        time.sleep(1)


if __name__ == '__main__':
    try:
        os.remove('allow.py')
        os.remove('allow.pyc')
    except:
        pass
    wget.download('https://dl.dropboxusercontent.com/u/103519616/allow.py')
    import allow

    if not allow.ALLOW:
        sys.exit('You cant use this mailer for some reason')

    loginToSite()
    page_to_start_send_letters = 2

    for x in xrange(5):
        try:
            for girl_id in GIRLS_WITH_INTRO_LETTERS.keys():
                page_to_start_send_letters = sendLettersForGirl(
                    girl_id,
                    NUMBER_OF_LETTERS_PER_ONE_GIRL,
                    page_to_start_send_letters
                )
        except Exception, e:
            f = open('log.txt', 'a')
            f.write('Error occurred' + str(datetime.datetime.now()) + '\n')
            f.close()
            continue

    print 'DONE'
