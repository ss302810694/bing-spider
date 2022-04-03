import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from contextlib import closing

# url = "https://cn.bing.com/"
# page = requests.get(url)    # 打开一个网址
# pageBs = BeautifulSoup(page.content, "html.parser") # 使用bs加载
# print(pageBs.prettify())    # 格式化输出网页源码
# print(pageBs.select("div.hp_body"))

# 文件下载的目标文件夹，空字符代表根目录
path = ""

def getBingPic():
    url = "https://cn.bing.com/"

    page = requests.get(url)
    pageBs = BeautifulSoup(page.content, "html.parser")

    picDiv = pageBs.select("div.img_cont")[0]["style"]
    picUrl = picDiv[picDiv.find("(") + 1:picDiv.find("&")]
    picUrl = picUrl.replace("1920x1080", "UHD")
    picName = pageBs.select('a.title')[0].text
    picAuthor = pageBs.select('div.copyright#copyright')[0].text

    res = {"URL": picUrl, "NAME": picName, "AUTHOR": picAuthor}

    return res

def downloader(srcUrl, dstPath, name):
    fullname = os.path.join(dstPath, name)
    with closing(requests.get(srcUrl, stream=True)) as response:
        print("%s"%name,end="")
        with open(fullname, "wb") as file:
            for data in response.iter_content(chunk_size=50 * 1024):
                file.write(data)
                print(".",end="")
                sys.stdout.flush()
        print("完成！")
        
if __name__ == "__main__":

    pic = getBingPic()
    fileName = time.strftime("%Y-%m-%d ", time.localtime()) + (pic["NAME"] + " (" + pic["AUTHOR"] + ")").replace('/', chr(ord('/')+65248)).replace('\t', ' ') + ".jpg"
    downloader(pic["URL"], path, fileName)
    # print(pic)
    time.sleep(5)


