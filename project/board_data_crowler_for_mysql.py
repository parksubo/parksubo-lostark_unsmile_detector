import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import mysql.connector

def crowling():
    url = f"https://lostark.game.onstove.com/Community/Free/List?page={1}&searchtype=0&searchtext=&ordertype=latest&category=0"
    response = requests.get(url)

    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    
    posts = soup.find_all("li", class_="")
    
    for post in posts:
        title, nickname, reg_date = "", "", ""
        if post.find("span", class_="list__title") != None and \
            post.find("span", class_="member-info__nickname") != None and \
            post.find(class_="list__date") != None:
                title = post.find("span", class_="list__title").text.strip()
                nickname = post.find("span", class_="member-info__nickname").text.strip()
                reg_date = post.find(class_="list__date").text.strip()
                # Convert "n시간 전" to "%Y-%m-%d" format, sub 9h for KST
                if "시간" in reg_date:
                    h = int(reg_date.split("시간")[0])
                    reg_date = str(datetime.datetime.now() + datetime.timedelta(hours=9) - datetime.timedelta(hours=int(h))).split(" ")[0]
                
                # Convert "n분 전" to "%Y-%m-%d" format, add 9h for KST
                elif "분" in reg_date:
                    m = int(reg_date.split("분")[0])
                    reg_date = str(datetime.datetime.now() + datetime.timedelta(hours=9) - datetime.timedelta(minutes=int(m))).split(" ")[0]
                else:
                    reg_date = reg_date.replace(".", "-")
                
                return [nickname, title, reg_date]

    return 

def load_data_to_mysql():
    conn = mysql.connector.connect(
        host="0.0.0.0",
        user="root",
        password="Tnqh0521!",
        database="lostark_raw_data"
    )

    # Load recent data in mysql
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchall()
    mysql_data = [row[0][1], row[0][2], row[0][3].strftime("%Y-%m-%d")]
    
    # Load recent data using crowling
    crowling_data = crowling()
    
    if mysql_data == crowling_data:
        print("데이터 중복")
    else:
        values = (crowling_data[0], crowling_data[1], crowling_data[2])
        query = "INSERT INTO board_data (nickname, title, reg_date) VALUES (%s, %s, %s)"
        cursor.execute(query, values)
        conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    return


# Main
if __name__=="__main__":
    load_data_to_mysql()