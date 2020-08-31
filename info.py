import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'https://www.letuin.com/login.php'
LOGIN_DATA = {
    'action':'Login',
    'url':'aHR0cHM6Ly93d3cubGV0dWluLmNvbS9sb2dpbi5waHA%3D',
    'code':'',
    'userid':'',
    'passwd':''
}

ADMIN_URL = 'https://www.letuin.com/admin/'
LECTURE_URL = 'lecture.php?action=LectureDate&lec_no='
USERINFO_URL = 'userinfo.php?user_id='

print("아이디와 비밀번호를 입력해주세요")
userid = input()
passwd = input()

LOGIN_DATA['userid'] = userid
LOGIN_DATA['passwd'] = passwd

with requests.session() as session:
    res = session.post(LOGIN_URL, data=LOGIN_DATA)

    flag = 1
    f = open("user.txt", "w")
    while flag != 0:

        if flag == 1:
            print("스크랩을 원하는 아이디를 입력해주세요")
            user_id = input()

        user_url = ADMIN_URL + USERINFO_URL + user_id + '&s='

        user_res = session.get(user_url)
        soup = BeautifulSoup(user_res.text, 'html.parser')

        user_name = soup.select('table.tbl-table-style > tr.ht > td > input[name=name1]')[0]['value']
        user_id = soup.select('table.tbl-table-style > tr.ht > td > input[name=id]')[0]['value']
        user_hp = soup.select('table.tbl-table-style > tr.ht > td > input[name=hp]')[0]['value']
        user_email = soup.select('table.tbl-table-style > tr.ht > td > input[name=email]')[0]['value']
        user_birth1 = soup.select('table.tbl-table-style > tr.ht > td > input[name=birth1]')[0]['value']
        user_birth2 = soup.select('table.tbl-table-style > tr.ht > td > input[name=birth2]')[0]['value']
        user_birth3 = soup.select('table.tbl-table-style > tr.ht > td > input[name=birth3]')[0]['value']

        line = user_name + "\t" + user_birth1 + ". " + user_birth2 + ". " + user_birth3 + "\t" + user_id + "\t" + user_hp + "\t" + user_email + "\n"

        f.write(line)

        print("계속하시겠습니까(Y/N)")
        flag = input()

        if flag == 'N':
            flag = 0
            f.close()
        else:
            user_id = flag