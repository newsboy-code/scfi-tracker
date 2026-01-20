import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_scfi_data():
    url = "https://www.kcla.kr/web/inc/html/4-1_3.asp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. SCFI 테이블 정확히 찾기 (summary 속성 활용)
        table = soup.find('table', attrs={'summary': 'scfi'})
        if not table:
            print("테이블을 찾을 수 없습니다.")
            return

        rows = table.find_all('tr')
        
        # 2. 날짜와 지수 추출
        # 첫 번째 tr: '지수' 텍스트 + 날짜들
        # 두 번째 tr: 지수 값들
        dates_raw = rows[0].find_all('td')
        values_raw = rows[1].find_all('td')

        # 첫 번째 td는 '지수'라는 제목이므로 제외하고 나머지만 추출
        dates = [td.get_text(strip=True) for td in dates_raw if '지수' not in td.get_text()]
        values = [td.get_text(strip=True) for td in values_raw]

        # 3. 데이터 결합
        scfi_data = []
        for d, v in zip(dates, values):
            scfi_data.append({"날짜": d, "SCFI지수": v})

        # 4. 결과 확인 및 저장
        df = pd.DataFrame(scfi_data)
        
        # 최신 데이터가 가장 위로 오게 정렬 (선택 사항)
        df = df.iloc[::-1] 
        
        df.to_csv("scfi_data.csv", index=False, encoding='utf-8-sig')
        print(f"✅ 총 {len(df)}개의 데이터를 성공적으로 수집했습니다.")
        print(f"최신 데이터: {scfi_data[-1]}") # 2026.01.16 데이터 출력 확인용

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    get_scfi_data()
