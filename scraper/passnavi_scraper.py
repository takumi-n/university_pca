# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import json

# google API KEY
API_KEY = "xxxxx"
CX = 'xxxxx'


def get_passnavi_url(university_name):
    query = u"site:https://passnavi.evidus.com/search_univ/ %s 大学トップ" %(university_name)
    url = 'https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s' %(API_KEY, CX, urllib.quote(query.encode('utf-8')))
    opener = urllib2.build_opener()
    res = opener.open(url).read()
    res_dict = json.loads(opener.open(url).read())
    for res_items in res_dict.get('items'):
        res_url = res_items.get('formattedUrl')
        if re.search('https://passnavi.evidus.com/search_univ/(\d+)/campus.html', res_url):
            return res_url
    return None


# 100 * 女子数 / 全体数
def get_student_num(passnavi_url):
    html = urllib2.urlopen(passnavi_url)
    soup = BeautifulSoup(html, "html.parser")
    h5_tags = soup.find_all('h5')
    for h5t in h5_tags:
        if h5t.text == u'学生総数':
            student_num_str = h5t.find_next_sibling('p').text
            # 4,079（女子のみ）
            student_num_obj = re.match(u'(\d+)（女子のみ）', student_num_str.replace(',', ''))
            if student_num_obj:
                total_num = int(student_num_obj.group(1))
                return {'total_num':total_num, 'gender_ratio': 100}
            # 男11,383・女2,664、計14,047（2016年）
            student_num_obj = re.match(u'男(\d+)・女(\d+)、計(\d+)', student_num_str.replace(',', ''))
            if student_num_obj:
                female_num = int(student_num_obj.group(2))
                total_num = int(student_num_obj.group(3))
                gender_ratio = 100 * female_num / total_num
                return {'total_num':total_num, 'gender_ratio': gender_ratio}
    return None


def get_expense(passnavi_url):
    html = urllib2.urlopen(passnavi_url.replace('campus', 'expense'))
    soup = BeautifulSoup(html, "html.parser")
    th_tags = soup.find_all('th', class_='cell-color-default')
    expense_list = []
    for tht in th_tags:
        if tht.text == u'初年度納入金額':
            expense_str = tht.find_next_sibling('td').text
            expense_list.append(int(expense_str.replace(',','').replace(u'※', '')))
    avg_expense = sum(expense_list) / len(expense_list)
    return avg_expense


def main():
    master_file = '../data/university_name_master.csv'
    f = open(master_file, 'r')
    lines = f.readlines()
    lines = map(lambda x: x.rstrip(), lines)
    f.close()
    for l in lines:
        university_name = l.split(',')[0]
        university_name = unicode(university_name, 'utf-8')
        passnavi_url = get_passnavi_url(university_name)
        student_num = get_student_num(passnavi_url)
        expense = get_expense(passnavi_url)
        if not student_num:
            print '--'
            print expense
            exit()
        new_line = str(student_num.get('total_num')) + ',' + str(student_num.get('gender_ratio')) + ',' + str(expense)
        print new_line


if __name__ == '__main__':
    main()
