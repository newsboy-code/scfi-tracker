import requests
import re
import pandas as pd
import sys

def get_scfi_data():
    url = "https://www.kcla.kr/web/inc/html/4-1_3.asp"
    # 브라우저처럼 보이게 헤더를 더 보강합니다.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        print(f"📡 응답 상태 코드: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ 사이트 접속에 실패했습니다.")
            sys.exit(1)

        html_text = response.text

        # 정규표현식 보강: ['날짜', 숫자] 패턴 (공백 및 특수문자 대응)
        pattern = r"\[\s*['\"](.*?)['\"]\s*,\s*([\d\.]+)\s*\]"
        matches = re.findall(pattern, html_text)

        if not matches:
            print("⚠️ 데이터를 찾지 못했습니다. 깃허브 로그에 찍힌 아래 내용을 확인하세요.")
            print("-" * 50)
            print(html_text[:1000]) # HTML 앞부분 출력하여 차단 여부 확인
            print("-" * 50)
            sys.exit(1) # 데이터를 못 찾으면 에러를 발생시켜 로그를 보게 함

        # 데이터 정리
        scfi_data = [{"날짜": d, "SCFI지수": v} for d, v in matches]
        df = pd.DataFrame(scfi_data)
        
        # 파일 저장
        df.to_csv("scfi_data.csv", index=False, encoding='utf-8-sig')
        print(f"✅ 수집 성공! ({len(df)}건)")
        print(f"최근 데이터: {scfi_data[-1]}")

    except Exception as e:
        print(f"❌ 실행 중 치명적 에러: {e}")
        sys.exit(1)

if __name__ == "__main__":
    get_scfi_data()
