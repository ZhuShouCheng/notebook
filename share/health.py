# -*- coding = utf-8 -*-
# @Time : 2021/4/9 12:47
# @Author :
# @File : health.py
# @Software: PyCharm
from qingjia import qingjia



if __name__ == "__main__":
    # chromedriver_path = "D:\Repositories\python_working\chromedriver.exe"  # 改成你的chromedriver的完整路径地址

    # 人多后可以考虑开启多线程

    zhu = {
        "学号": "220205356",
        "密码": "zsc19971121",
    }

    han = {
        "学号": "220205268",
        "密码": "hanzhen123",
    }


    flag = True
    while flag:
        try:
            a = qingjia()
            a.login(zhu)  # 登录
        except:
            a.browser.close()
            continue
        else:
            flag = False

    try:
        a.health_declaration()
    except:
        a.browser.close()
    finally:
        a.browser.quit()

    flag = True
    while flag:
        try:
            b = qingjia()
            b.login(han)  # 登录
        except:
            b.browser.close()
            continue
        else:
            flag = False

    for i in range(0,10):
        try:
            b.health_declaration()
        except:
            b.browser.close()
            continue

    b.browser.quit()