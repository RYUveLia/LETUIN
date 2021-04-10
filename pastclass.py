import os
import re
import requests
from bs4 import BeautifulSoup

fileDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(fileDir)

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

    flag = 0

    while flag == 0:
        print("스크랩을 원하는 강의번호를 입력해주세요")
        lecture_num = input()

        lec_url = ADMIN_URL + LECTURE_URL + lecture_num

        res = session.get(lec_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        num_info = soup.select('table.tbl-table-style > tbody > tr > td')

        # pageView = 전체 기수로 새로고침

        lec_url = ADMIN_URL + LECTURE_URL + lecture_num + "&pageView=" + str(re.findall(r'\d+', num_info[0].text)[0])

        res = session.get(lec_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        lec_info = soup.select('table.tbl-table-style > tbody > tr > td > a')
        num_info = soup.select('table.tbl-table-style > tbody > tr > td')

        print("파일명을 입력해주세요")
        filename = input()

        if filename == '':
            f = open("새 파일.txt", "w")
        else:
            f = open(filename + ".txt", "w")

        print("찾으려는 기수를 입력해주세요")
        gisu = int(input())

        # num_info[i % 7]
        # 0: 기수
        # 1: 모집기간
        # 2: 수강기간
        # 3: 강사명
        # 4: 마감여부
        # 5: 수강생
        # 6: 비고 

        for i in reversed(range(0, len(lec_info), 3)):
            # find_gisu = 1기 2기 3기
            newi = i // 3 * 7
            find_gisu = re.findall(r'\d+', num_info[newi].text)
            for k in find_gisu:
                # class_size = 정원
                class_size = int(re.findall(r'\d+', num_info[newi + 5].text)[1])

                if int(k) == gisu:
                    line = k + "기\n"
                    #print(line)
                    f.write(line)

                    # https://www.letuin.com/admin/lecture.php?action=LectureDateRegister&lec_type=&lec_no=강의번호&no=3104[기수번호]&w=update

                    info_url = ADMIN_URL + lec_info[i].get('href') + "&pageView=" + str(class_size)

                    info_res = session.get(info_url)
                    info_soup = BeautifulSoup(info_res.text, 'html.parser')
                    std = info_soup.select('b')

                    #for j in std:
                        #print(j.text)

                    num = 0

                    for j in reversed(range(0, len(std), 2)):
                        user_id = std[j].text

                        #받을때마다 하지말고 전부 받고 가져오기?
                        user_url = ADMIN_URL + USERINFO_URL + user_id + '&s='

                        user_res = session.get(user_url)
                        user_soup = BeautifulSoup(user_res.text, 'html.parser')

                        user_name = user_soup.select('table.tbl-table-style > tr.ht > td > input[name=name1]')[0]['value']
                        user_id = user_soup.select('table.tbl-table-style > tr.ht > td > input[name=id]')[0]['value']
                        user_hp = user_soup.select('table.tbl-table-style > tr.ht > td > input[name=hp]')[0]['value']
                        user_email = user_soup.select('table.tbl-table-style > tr.ht > td > input[name=email]')[0]['value']
                        num = num + 1

                        line = "\t" + str(num) + "\t" + user_name + "\t" + user_id + "\t" + user_hp + "\t" + user_email + "\n"
                        f.write(line)
                        #print(line)

                    # 빈 자리 엔터치기
                    for j in range(len(std)//2, class_size):
                        num = num + 1
                        line = "\t" + str(num) + "\n"
                        f.write(line)

                    f.write("\n")
            

        f.close()

        print("파일이 생성되었습니다. 종료하시겠습니까?(Y/N)")
        flag = input()

        if flag == 'Y':
            flag = 1
        elif flag == 'N':
            flag = 0

