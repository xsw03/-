
# 页面设置
from selenium import webdriver
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from lxml import etree
# 设置浏览器驱动路径
driver_path = r'C:\Program Files\Google\Chrome Dev\Application\chromedriver.exe'        # 这个路径建议改
# 创建浏览器选项对象
chrome_options = Options()

# chrome_options.add_argument('--headless')  # 启用无头模式
chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 禁用图像加载

# 创建浏览器驱动实例
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)



#函数设置
def get_main_url(url_in,start_data,end_data):
    # 根据输入的时间，返回一个列表，列表内包含所有可以爬取的值
    list_out = []
    flag = 1
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url_in)

    while(flag):

        time.sleep(5)                   # 留有加载时间
        page_body = driver.page_source

        # print("打开网页成功\n\n\n")
        # print(page_body)

        tree = etree.HTML(page_body)
        # 获取当前页的元素信息并存储到临时列表中
        # 只要当前页 发布日期 晚于截止日期就继续下一个或翻页，晚于开始日期就加入列表，当发布日期 早于开始日期就停止程序


        tr_elements = tree.xpath("""//*[@id="postList"]/table/tbody/tr""")

        # 创建一个大列表
        result_list = []

        # 遍历每个 <tr> 元素
        for tr_element in tr_elements:
            # 创建一个内部列表
            inner_list = []

            # 在 <tr> 元素下使用 XPath 定位到第一个 <td> 元素，并提取其 <a> 标签的 href 属性
            first_td_element = tr_element.xpath(".//td[1]")[0]
            href = first_td_element.xpath(".//a/@href")[0]
            inner_list.append(href)

            # 在 <tr> 元素下使用 XPath 定位到第二个 <td> 元素，并提取其文本内容
            second_td_element = tr_element.xpath(".//td[2]")[0]
            text = second_td_element.text
            inner_list.append(text)

            # 将内部列表添加到大列表中
            result_list.append(inner_list)
        # print(result_list)


        for data in result_list:
            i = data[1].replace("-","")
            if int(end_data) < int(i):
                continue
            elif int(start_data) < int(i):
                list_out.append(data[0])
                print(data)
            else:
                flag = 0
                break
        if flag:
            driver.find_element(by=By.XPATH,value="""//*[@id="postList"]/div/a[contains(text(), '下一页')]""").click()     # 下一页的位置并不固定，采用查找的方式进行点击


    # time.sleep(1000)
    driver.close()
    return list_out



def get_list(url_in):
    # 遍历输入的列表，将其中的内容进行解析后输出
    list_out = []
    for url_i in url_in:
        # print("进入循环")
        url_ = "https:" + url_i
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url_)
        time.sleep(3)           # 依然根据网速留时间
        page_body = driver.page_source
        tree = etree.HTML(page_body)

        attachment_links = tree.xpath('//a[contains(text(), "附件")]/@href')

        # 将附件链接添加到列表中
        attachment_list = []
        for link in attachment_links:
            attachment_list.append(link)

        # 使用XPath定位<div>元素
        div_elements = tree.xpath("""/html/body/div[2]/div[4]/div[3]/div[3]/div[2]""")
        # 使用XPath定位<div>元素下所有<p>标签，并获取其文字内容
        p_texts = []
        for div_element in div_elements:
            p_tags = div_element.xpath('.//p')  # 获取所有的<p>标签，不仅限于直接子节点
            # 存储<p>标签的文字内容的列表
            for p in p_tags:
                p_texts.append(p.text)  # 去除文字内容的前后空白字符


        dict_use = {
            '索引号': tree.xpath("""/html/body/div[2]/div[4]/div[3]/div[1]/table/tbody/tr[1]/td[2]/span/text()"""),
            '发布机构': tree.xpath("""/html/body/div[2]/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[2]/span/text()"""),
            '发布日期': tree.xpath("""/html/body/div[2]/div[4]/div[3]/div[1]/table/tbody/tr[4]/td[4]/span/text()"""),
            '政策标题': tree.xpath("""/html/body/div[2]/div[4]/div[3]/div[3]/h1/text()"""),
            '政策正文文本': p_texts,
            '政策正文附件链接': attachment_list
        }
        list_out.append(dict_use)
        print(dict_use)

        driver.close()
    return list_out




# 主函数
if __name__ == "__main__":
    start_data,end_data = input().split("-")    # 20220101-20230601           20240401-20240510

    # start_data = 20240401
    # end_data = 20240510
    # print(start_data)
    # print(end_data)
    list_urls = get_main_url("https://www.gd.gov.cn/gkmlpt/policy",start_data,end_data)
    print(list_urls)
    list_ans = get_list(list_urls)
    print(list_ans)

    # list_ans = get_list(['//www.gd.gov.cn/gkmlpt/content/4/4419/post_4419971.html','//www.gd.gov.cn/gkmlpt/content/4/4412/post_4412010.html'])
    # print(list_ans)