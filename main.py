import requests
from bs4 import BeautifulSoup
import re
import json
serchurl = 'https://www.gequbao.com/s/'
DownURL='https://www.gequbao.com/api/play_url?id='
music_info = []
#获取搜索内容函数
def getSearch(key):
    # 执行GET请求
    response = requests.get(serchurl+key)
    if response.status_code == 200:
        html_content=response.text
        # 创建 BeautifulSoup 对象
        soup = BeautifulSoup(html_content, 'html.parser')
        # 查找所有包含歌曲名称和歌手名称的行
        rows = soup.find_all('div', class_='row')
        # 初始化存储歌曲名称、歌手名称和ID的列表
        music_info.clear()
        #设置歌曲编号
        i = 1;
        # 遍历每一行并提取信息
        print("##########################################################")
        for row in rows:
            title_span = row.find('span', class_='music-title')
            artist_small = row.find('small', class_='text-jade')
            link = row.find('a', href=True)
            if title_span and artist_small and link:
                title = title_span.get_text(strip=True)
                artist = artist_small.get_text(strip=True)
                href = link['href']
                music_info.append((i,title, artist, href))
                i=i+1;
        # 打印所有匹配的歌曲、歌手和链接ID
        for i,title, artist, href in music_info:
            print(f"序号：{i}，歌曲名称: {title}, 歌手: {artist}")
        print("##########################################################")
        user_input2 =len(input("请输入需要下载的序号："))
        if len(music_info) >= user_input2:
            save_path = str(music_info[user_input2 - 1][0])+"_"+music_info[user_input2 - 1][1]+"_"+music_info[user_input2 - 1][2]+".mp3"
            getDownUrl(music_info[user_input2 - 1][3],save_path)
    else:
        print(f"获取数据失败。HTTP状态码: {response.status_code}")
#获取下载链接函数
def getDownUrl(id,save_path):
    match = re.search(r'/music/(\d+)',id)
    if match:
        music_id = match.group(1)
    else:
        return
    response = requests.get(DownURL+music_id+'&json=1')
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 JSON 字符串
        data = json.loads(response.text)
        # 提取 URL 参数
        url = data['data']['url']
        # 打印 URL
        #print(f"下载的 URL 是: {url}")
        Downfile(url,save_path)
    else:
        print(f"获取数据失败。HTTP状态码: {response.status_code}")
#下载文件函数
def Downfile(file_url,save_path):
    # 发送 GET 请求下载文件
    response = requests.get(file_url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 将内容写入文件
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"文件已成功下载并保存为 {save_path}")
    else:
        print(f"下载失败，HTTP 状态码: {response.status_code}")

if __name__ == '__main__':
    user_input = input("请输入关键词:")
    getSearch(user_input)



