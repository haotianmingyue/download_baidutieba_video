# 开发者 haotian
# 开发时间: 2023/8/3 19:01

import requests
import time
from lxml import etree


class Download_by_faviour():
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    # 获取收藏中的项目
    def get_faviour_list(self):
        html = requests.get(url=self.url, headers=self.headers).content.decode("utf-8")
        xpath = '//div[@class="favth_col1"]/span/a/@href'
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath(xpath)
        print(r_list)
        return r_list

    # 根据贴子获得发布人的id
    def get_userid_by_list(self):

        r_list = self.get_faviour_list()
        r_url = 'https://tieba.baidu.com'
        id = list()
        # 获取收藏贴子发布人的id
        for p in r_list:
            html = requests.get(url=r_url + p, headers=self.headers).content.decode("utf-8")
            parse_html = etree.HTML(html)
            xpath_name = '/html/body/div[2]/div/div[2]/div/div[4]/div[1]/div[3]/div[1]/div[1]/ul/li[3]/a/@data-field'
            try:
                video_author = parse_html.xpath(xpath_name)[0]
                video_author = eval(video_author)
                id.append(video_author['id'])
            except:
                continue
            time.sleep(0.5)
        id = list(set(id))
        print(id)
        return id

    # 根据id得到他发的贴子，只有最近的几条，由于涉及到按键加载更多，先这样吧
    def get_list_by_id(self):
        id = self.get_userid_by_list()
        personal_url = 'https://tieba.baidu.com/home/main?id='
        all_list = list()
        for i in range(len(id)):
            main_page = personal_url + id[i]
            html = requests.get(url=main_page, headers=self.headers).content.decode("utf-8")
            parse_html = etree.HTML(html)

            # 这个标签下是贴子链接和吧链接，要取0，2，4
            xpath = '//div[@class="thread_name"]/a/@href'

            video_list = parse_html.xpath(xpath)
            for i in range(0, len(video_list), 2):
                all_list.append(video_list[i])
            time.sleep(0.5)
        print(all_list)
        return all_list

    # 找到贴子中的视频跳转链接
    def get_video_url(self):
        all_list = self.get_list_by_id()
        all_video = list()
        r_url = 'https://tieba.baidu.com'
        for t in all_list:
            html = requests.get(url=r_url + t, headers=self.headers).content.decode("utf-8")
            parse_html = etree.HTML(html)

            # 这个标签下是贴子链接和吧链接，要取0，2，4
            xpath = '//span[@class="apc_src_wrapper"]/a/@href'
            # xpath = '//video/@src'
            video_list = parse_html.xpath(xpath)
            # print(video_list)
            if len(video_list) > 0:
                all_video.append(video_list[0])
            time.sleep(0.5)
        print(all_video)
        return all_video

    #得到MP4格式视频链接
    def get_mp4_url(self):
        all_video = self.get_video_url()
        mp4_list = list()
        for t in all_video:
            html = requests.get(url=t, headers=self.headers).content.decode("utf-8")
            video = html[html.find('videoUrl') + 12:html.find('mp4') + 3]
            video = video.replace('\\', '')
            mp4_list.append(video)
        print(mp4_list)
        return mp4_list

    #下载视频
    def download_video(self, path):
        mp4_list = self.get_mp4_url()
        for mp4 in mp4_list:
            try:
                html = requests.get(url=mp4, headers=self.headers).content

                filename = path + mp4.split('/')[-1]
                # print(filename)
                with open(filename, 'wb') as f:
                    f.write(html)
                    print("%s下载成功" % mp4)
            except:
                print("%s 下载失败" % mp4)
                continue


if __name__ == '__main__':
    # 你的百度贴吧收藏地址
    url = 'https://tieba.baidu.com/i/i/storethread?'
    headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Cookie' : ''


}
    d = Download_by_faviour(url, headers)

    save_path = './video1/'
    d.download_video(save_path)