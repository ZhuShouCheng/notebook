# -*- coding = utf-8 -*-
# @Time : 2021/4/5 15:41
# @Author :
# @File : qingjia.py
# @Software: PyCharm

# from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
import time

# url:
from selenium.webdriver.support.wait import WebDriverWait


class qingjia:
    def __init__(self):
        url = 'http://ehall.seu.edu.cn/new/index.html'
        self.url = url

        chromedriver_path = "D:\Repositories\python_working\chromedriver.exe"  # 改成你的chromedriver的完整路径地址

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # 不加载图片,加快访问速度
        options.add_experimental_option("excludeSwitches", ["enable - logging"])
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 20)

    def hover(self, value):
        element = self.browser.find_element_by_xpath(value)
        ActionChains(self.browser).move_to_element(element).perform()

    def login(self, info):

        print("in login")
        self.browser.get(self.url)
        time.sleep(3)
        in_button = self.wait.until(lambda x: x.find_element_by_class_name("amp-no-login-zh"))
        in_button.click()

        # find_element_by_name("username")
        user_login = self.wait.until(lambda x: x.find_element_by_name("username"))
        user_login.send_keys(info["学号"])

        passwd = self.browser.find_element_by_id("password")
        passwd.send_keys(info["密码"])

        login_button = self.wait.until(lambda x: x.find_element_by_id("xsfw"))
        login_button.send_keys(Keys.ENTER)
        ActionChains(self.browser).move_to_element(login_button).perform()
        login_button.click()
        print("out login")
        # # self.browser.find_elements_by_class_name("App-name")
        # in_button = self.wait.until(lambda x:x.find_element_by_xpath('//*[contains(text(), "研究生出校登记审核")]'))
        #
        # # in_button = buttons.find_element_by_xpath('//*[contains(text(), "研究生出校登记审核")]')
        # in_button.click()

    def health_declaration(self):
        in_button = self.wait.until(lambda x: x.find_element_by_xpath(
            '//*[contains(@href, "http://ehall.seu.edu.cn/appShow?appId=5821102911870447")]'))

        # in_button = buttons.find_element_by_xpath('//*[contains(text(), "研究生出校登记审核")]')
        in_button.click()

        main_handle = self.browser.current_window_handle

        # 获取当前窗口句柄集合（列表类型）
        handles = self.browser.window_handles

        reg_handle = None
        for handle in handles:
            if handle != main_handle:
                reg_handle = handle

        self.browser.switch_to.window(reg_handle)

        # ------------进入申报系统界面--------------

        registration_button = self.wait.until(lambda x: x.find_element_by_xpath('//*[contains(text(), "新增")]'))
        registration_button.click()

        button = self.wait.until(lambda x: x.find_element_by_xpath('//*[contains(@data-name, "DZ_JSDTCJTW")]'))
        button.send_keys("36")

        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        buttons = self.wait.until(lambda x: x.find_elements_by_xpath('//*[contains(@data-action, "save")]'))
        for button in buttons:
            button.click()

        button = self.wait.until(lambda x: x.find_element_by_xpath('//*[contains(text(), "提示")]'))
        # button_find = self.browser.find_element_by_class_name("bh-dialog-btn bh-bg-primary bh-color-primary-5")
        # print(button_find)

        yes_buttons = self.browser.find_elements_by_xpath('//*[text()="确认"]')

        for button in yes_buttons:
            # print(button.get_attribute("class"))
            if button.get_attribute("class") == "bh-dialog-btn bh-bg-primary bh-color-primary-5":
                button.click()
        # print(self.browser.page_source)
        self.browser.close()

    def out_registration(self, info):

        dict = {
            "辅导员姓名": "唐佳琦",
            "辅导员电话": "18552075730",
            "请假详情": "实习",
            "详细地址": "国金大厦",
        }
        # -----------进入审核界面----------------
        in_button = self.wait.until(lambda x: x.find_element_by_xpath('//*[contains(text(), "研究生出校登记审核")]'))

        # in_button = buttons.find_element_by_xpath('//*[contains(text(), "研究生出校登记审核")]')
        in_button.click()

        main_handle = self.browser.current_window_handle

        # 获取当前窗口句柄集合（列表类型）
        handles = self.browser.window_handles

        reg_handle = None
        for handle in handles:
            if handle != main_handle:
                reg_handle = handle

        self.browser.switch_to.window(reg_handle)

        # time.sleep(5)
        #
        # text = self.browser.page_source
        # print(text)

        registration_button = self.wait.until(lambda x: x.find_element_by_xpath('//*[contains(text(), "我要请假")]'))
        # registration_button = self.browser.find_element_by_xpath('//*[contains(string(), "我要请假")]')

        button = self.wait.until(lambda x: x.find_element_by_xpath('//*[contains(text(), "详情")]'))
        # registration_button.click()
        # button = self.browser.find_element_by_xpath('//*[contains(text(), "销假")]')
        # print(button)
        # ---------销假操作-------------
        try:
            button = self.browser.find_element_by_xpath('//*[text()="销假"]')
            button.click()
            button = self.wait.until(lambda x: x.find_element_by_xpath('//*[contains(text(), "提示")]'))
            # button_find = self.browser.find_element_by_class_name("bh-dialog-btn bh-bg-primary bh-color-primary-5")
            # print(button_find)

            yes_buttons = self.browser.find_elements_by_xpath('//*[text()="确定"]')

            for button in yes_buttons:
                print(button.get_attribute("class"))
                if button.get_attribute("class") == "bh-dialog-btn bh-bg-primary bh-color-primary-5":
                    button.click()

        except:
            pass

        registration_button.click()
        button = self.browser.find_element_by_id("CheckCns")
        button.click()

        yes_buttons = self.browser.find_elements_by_xpath('//*[text()="确定"]')

        for button in yes_buttons:
            # print(button.get_attribute("class"))
            if button.get_attribute("class") == "bh-btn bh-btn-primary bh-pull-right":
                button.click()

        # -----------请假信息录入页面--------------

        # -----------------基本信息--------------------

        button = self.wait.until(lambda x: x.find_element_by_xpath('//*[contains(text(), "家长姓名")]'))
        button = self.browser.find_element_by_name("JZXM")
        button.clear()
        button.send_keys(info["家长姓名"])

        button = self.browser.find_element_by_name("JZLXDH")
        button.clear()
        button.send_keys(info["家长联系电话"])

        button = self.browser.find_element_by_name("FDYXM")
        button.clear()
        button.send_keys(dict["辅导员姓名"])

        button = self.browser.find_element_by_name("FDYDH")
        button.clear()
        button.send_keys(dict["辅导员电话"])

        # ----------------请假信息----------------------

        # ------------------请假下拉框选择---------------------

        all = self.wait.until(
            lambda x: x.find_element_by_xpath(
                '//*[contains(@class, "add-form-container bh-mt-24")]'))

        button_1 = all.find_element_by_xpath(
            '//*[contains(@data-name, "DZQJSY")]')

        button_1.click()

        ActionChains(self.browser).move_to_element(button_1).perform()

        buttons = self.browser.find_elements_by_xpath(
            '//*[contains(@class, "jqx-listitem-state-normal jqx-item jqx-rc-all")]')

        for button in buttons:
            # print(button.text)
            if button.text == "因事出校（当天往返）":
                button.click()

        # ---------------------------------

        button_1 = self.browser.find_element_by_xpath(
            '//*[contains(@data-name, "QJXZ")]')

        button_1.click()

        ActionChains(self.browser).move_to_element(button_1).perform()

        buttons = self.browser.find_elements_by_xpath(
            '//*[contains(@class, "jqx-listitem-state-normal jqx-item jqx-rc-all")]')

        for button in buttons:
            # print(button.text)
            if button.text == "因公":
                button.click()

        # -----------------------------------
        button_1 = self.wait.until(
            lambda x: x.find_element_by_xpath(
                '//*[contains(@data-name, "YGLX")]'))

        button_1.click()

        ActionChains(self.browser).move_to_element(button_1).perform()

        buttons = self.browser.find_elements_by_xpath(
            '//*[contains(@class, "jqx-listitem-state-normal jqx-item jqx-rc-all")]')

        for button in buttons:
            # print(button.text)
            if button.text == "其他":
                button.click()

        # print(self.browser.page_source)

        # ------------请假日期------------------
        time_tool = time.localtime()
        begin = time.struct_time((
            time_tool.tm_year, time_tool.tm_mon, time_tool.tm_mday, 7, time_tool.tm_min, time_tool.tm_sec,
            time_tool.tm_wday, time_tool.tm_yday, time_tool.tm_isdst
        ))
        begin_time = time.strftime("%Y-%m-%d %H:%M:%S", begin)
        end = time.struct_time((
            time_tool.tm_year, time_tool.tm_mon, time_tool.tm_mday, 20, time_tool.tm_min, time_tool.tm_sec,
            time_tool.tm_wday, time_tool.tm_yday, time_tool.tm_isdst
        ))
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", end)

        button = self.browser.find_element_by_xpath('//*[contains(@data-name, "QJKSRQ")]')
        button_1 = button.find_element_by_xpath('//*[contains(@bh-form-role, "dateTimeInput")]')
        button_1.send_keys(begin_time)

        button_td = self.browser.find_element_by_xpath('//*[contains(@data-name, "QJJSRQ")]')
        buttons = button_td.find_elements_by_xpath('//*[contains(@bh-form-role, "dateTimeInput")]')
        for button in buttons:
            if button is not button_1:
                button.send_keys(end_time)

        button = self.browser.find_element_by_xpath('//*[contains(@class, "bh-txt-input__txtarea")]')
        button.send_keys("实习")

        # --------------出校信息---------------------
        # 界面下拉到底端
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        button_1 = self.wait.until(
            lambda x: x.find_element_by_xpath(
                '//*[contains(@data-name, "HDXQ")]'))

        button_1.click()

        ActionChains(self.browser).move_to_element(button_1).perform()

        buttons = self.browser.find_elements_by_xpath(
            '//*[contains(@class, "jqx-listitem-state-normal jqx-item jqx-rc-all")]')

        for button in buttons:
            # print(button.text)
            if button.text == "无锡校区":
                button.click()

        button_1.click()

        # ---------------------------
        button_1 = self.wait.until(
            lambda x: x.find_element_by_xpath(
                '//*[contains(@data-name, "DZSFLN")]'))

        button_1.click()

        ActionChains(self.browser).move_to_element(button_1).perform()

        buttons = self.browser.find_elements_by_xpath(
            '//*[contains(@class, "jqx-listitem-state-normal jqx-item jqx-rc-all")]')

        for button in buttons:
            # print(button.text)
            if button.text == "否":
                button.click()

        button = self.browser.find_element_by_xpath('//*[contains(@data-name, "XXDZ")]')
        button.send_keys("国金大厦")

        # 测试时可以改成 请假取消
        button = self.browser.find_element_by_xpath('//*[contains(@data-action, "请假保存")]')
        button.click()

        time.sleep(4)
        self.browser.close()

        self.browser.switch_to.window(main_handle)
        self.browser.close()


def run_registration():
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
    # a.login(zhu)

    # a.health_declaration()
    try:
        a.out_registration(zhu)
    except:
        a.browser.close()
    finally:
        a.browser.quit()


if __name__ == "__main__":
    # chromedriver_path = "D:\Repositories\python_working\chromedriver.exe"  # 改成你的chromedriver的完整路径地址

    zhu = {
        "学号": "220205356",
        "密码": "zsc19971121",
        "家长姓名": "朱信福",
        "家长联系电话": "15190670581",
    }

    currentTime = time.localtime()
    if currentTime.tm_wday == 0 or currentTime.tm_wday == 2 or currentTime.tm_wday == 3:
        run_registration()
