import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_scfi_data():import requests
import re
import pandas as pd

def get_scfi_data():
    url = "https://www.kcla.kr/web/inc/html/4-1_3.asp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html_text = response.text

        # 1. 자바스크립트 내의 데이터 배열(var line1) 추출
        # 형태: ['03-Jan-25', 2505.17]
        pattern = r"\[\s*'(.*?)',\s*([\d\.]+)\s*\]"
        matches = re.findall(pattern, html_text)

        if not matches:
            print("❌ 데이터를 찾지 못했습니다. 사이트 구조가 변경되었을 수 있습니다.")
            # 디버깅을 위해 HTML 일부 출력
            print("HTML 서두 일부:", html_text[:500])
            return

        # 2. 데이터 정제
        scfi_data = []
        for date_str, value in matches:
            scfi_data.append({
                "날짜": date_str,
                "SCFI지수": value
            })

        # 3. CSV 저장
        df = pd.DataFrame(scfi_data)
        
        # 월 이름을 숫자로 바꾸고 싶다면 추가 처리가 가능하지만, 
        # 일단 원본 데이터가 잘 들어오는지 확인하기 위해 그대로 저장합니다.
        df.to_csv("scfi_data.csv", index=False, encoding='utf-8-sig')
        
        print(f"✅ 수집 성공! 총 {len(df)}주의 데이터를 가져왔습니다.")
        print(f"최근 데이터 확인: {scfi_data[-1]}")

    except Exception as e:
        print(f"❌ 실행 중 에러 발생: {e}")

if __name__ == "__main__":
    get_scfi_data()
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
