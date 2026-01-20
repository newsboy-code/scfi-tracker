import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 데이터 가져오기
url = "https://www.kcla.kr/web/inc/html/4-1_3.asp"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

# 2. 가로형 테이블 파싱 (행 2개, 열 52개 구조)
rows = soup.select('table tr')
if len(rows) >= 2:
    # 첫 번째 행에서 날짜 추출, 두 번째 행에서 지수 추출
    dates = [td.get_text(strip=True) for td in rows[0].find_all(['td', 'th'])]
    values = [td.get_text(strip=True) for td in rows[1].find_all('td')]

    # 데이터 결합 (날짜가 있는 것만)
    data = []
    for d, v in zip(dates, values):
        if any(char.isdigit() for char in d):
            data.append({"날짜": d, "SCFI지수": v})

    # 3. CSV로 저장
    df = pd.DataFrame(data)
    df.to_csv("scfi_data.csv", index=False, encoding='utf-8-sig')
    print("성공적으로 데이터를 긁어왔습니다!")
