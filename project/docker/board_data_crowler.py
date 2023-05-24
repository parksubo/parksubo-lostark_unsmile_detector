import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

def crowling_from_page(page):
    url = f"https://lostark.game.onstove.com/Community/Free/List?page={page}&searchtype=0&searchtext=&ordertype=latest&category=0"
    response = requests.get(url)

    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    
    data = []
    posts = soup.find_all("li", class_="")
    
    for post in posts:
        title, nickname, reg_date = "", "", ""
        if post.find("span", class_="list__title") != None and \
            post.find("span", class_="member-info__nickname") != None and \
            post.find(class_="list__date") != None:
                title = post.find("span", class_="list__title").text.strip()
                nickname = post.find("span", class_="member-info__nickname").text.strip()
                reg_date = post.find(class_="list__date").text.strip()
                # Convert "n시간 전" to "%Y-%m-%d" format 
                if "시간" in reg_date:
                    h = int(reg_date.split("시간")[0])
                    reg_date = str(datetime.datetime.now() - datetime.timedelta(hours=int(h))).split(" ")[0]
                # Convert "n분 전" to "%Y-%m-%d" format 
                elif "분" in reg_date:
                    m = int(reg_date.split("분")[0])
                    reg_date = str(datetime.datetime.now() - datetime.timedelta(minutes=int(m))).split(" ")[0]
                else:
                    reg_date = reg_date.replace(".", "-")
                
                data.append([nickname, title, reg_date])
                
    return data

# generate 15 data per page
def board_data_generator(n, path):
    data = []
    for i in range(1, n + 1):
        page_data = crowling_from_page(i)
        data.extend(page_data)
  
    df = pd.DataFrame(data, columns=["nickname", "title", "reg_date"])
    df.to_csv(path, index=False)
    
    return

    
board_data_generator(200, path)
    
