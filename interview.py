import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'https://www.letuin.com/login.php'
LOGIN_DATA = {
    'action':'Login',
    'url':'****',
    'code':'',
    'userid':'****',
    'passwd':'****'
}

ADMIN_URL = 'https://www.letuin.com/admin/'
LECTURE_URL = 'lecture.php?action=LectureDate&lec_no='
USERINFO_URL = 'userinfo.php?user_id='

with requests.session() as session:
    res = session.post(LOGIN_URL, data=LOGIN_DATA)

    print("스크랩을 원하는 강의번호를 입력해주세요")
    lecture_num = input()

    lec_url = ADMIN_URL + LECTURE_URL + lecture_num

    res = session.get(lec_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    lec_info = soup.select('table.tbl-table-style > tbody > tr > td > a')

    count = 0
    for i in lec_info:
        if count % 3 == 0:
            count = 0

            #print(i.get('href'))

            info_url = ADMIN_URL + i.get('href')

            info_res = session.get(info_url)
            info_soup = BeautifulSoup(info_res.text, 'html.parser')
            std = info_soup.select('b')

            student = []
            temp_std = {}
            std_count = 0
            for j in std:
                if std_count % 2 == 1:
                    std_count = 0

                    temp_std['name'] = j.text
                    print(temp_std)
                    continue;

                temp_std['id'] = j.text
                std_count = std_count + 1

            print()

        count = count + 1
