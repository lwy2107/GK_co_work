import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_news(keyword):
    url = f'https://news.google.com/search?q={keyword}&hl=ko&gl=KR&ceid=KR%3Ako'

    # 해당 URL에 대한 크롤링 코드 작성
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 데이터를 저장할 리스트 생성
    news_data = []

    # 기사 제목과 내용 일부 크롤링
    articles = soup.find_all('h3', class_='ipQwMb ekueJc RD0gLb')
    for article in articles:
        title = article.text
        # 기사 내용 크롤링을 원한다면 추가 작업 필요

        # 리스트에 데이터 추가
        news_data.append({
            '제목': title,
            '내용': None  # 원하는 경우 기사 내용을 크롤링하여 추가
        })

    # 데이터프레임 생성
    df = pd.DataFrame(news_data)

    # 데이터프레임을 엑셀 파일로 저장
    df.to_excel(f'{keyword}_news.xlsx', index=False)

if __name__ == "__main__":
    keyword = input("뉴스를 검색할 키워드를 입력하세요: ")
    crawl_news(keyword)
