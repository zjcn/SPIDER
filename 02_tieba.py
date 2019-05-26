import requests
import json
from lxml import etree


class TiebaSpider:
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                        "Referer": "https://tieba.baidu.com/",
                        }
        self.start_url = "https://tieba.baidu.com/f?ie=utf-8&kw="+ self.tieba_name
        self.part_url = "https://tieba.baidu.com/"


    def parse_url(self, url):
        print(url)
        response = requests.get(url, headers=self.headers)
        response = response.content.decode()
        response = response.replace(r'<!--','"').replace(r'-->','"')
        return response

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@class='col2_right j_threadlist_li_right ']")
        print(div_list)
        content_list = []
        for comtent in div_list:
            item = {}
            item["title"] = comtent.xpath(".//a/text()")[0] if len(comtent.xpath(".//a/text()")[0])>0 else None
            print(item["title"])
            item["href"] = self.part_url + comtent.xpath(".//a/@href")[0] if len(comtent.xpath(".//a/@href")[0])>0 else None
            item["img"] = self.get_img_list(item["href"], [])
            content_list.append(item)

        # print(html.xpath("//a[@class='next pagination-item']"))

        # next_url = html.xpath("//a[@class='next pagination-item ']/@href")[0] if len(html.xpath("//a[@class='next pagination-item ']/@href")[0])>0 else None
        try:
            next_url = "https:" + html.xpath("//a[@class='next pagination-item ']/@href")[0] if len(html.xpath("//a[@class='next pagination-item ']/@href")[0]) > 0 else None
        except:
            next_url = None
        # print(next_url)


        # print(next_url)
        return content_list, next_url

    def get_img_list(self, detail_url, total_img_list):
        detail_url_str = self.parse_url(detail_url)
        detail_html = etree.HTML(detail_url_str)
        img_list = detail_html.xpath("//img[@class='BDE_Image']/@src")
        total_img_list.extend(img_list)
        detail_next_url = detail_html.xpath("//a[@class='next pagination-item ']/@href")
        if len(detail_next_url)>0:
            detail_next_url = detail_next_url[0]
            return self.get_img_list(detail_next_url, total_img_list)

        print(total_img_list)
        return total_img_list

    def save_data_list(self, content_list):
        file_path = self.tieba_name+".txt"
        with open(file_path, "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2) )
                f.write("\n")

        print("保存成功")


    def run(self):
        # 1、start_url地址构造
        next_url = self.start_url
        while next_url is not None:
            html_str = self.parse_url(next_url)
            content_list, next_url = self.get_content_list(html_str)
            self.save_data_list(content_list)
            # 2、发送请求，获得响应
            # 3、提取数据
            # 4、保存数据
            # 5、循环


if __name__ == '__main__':
    tieba_spider = TiebaSpider("做头发")
    tieba_spider.run()