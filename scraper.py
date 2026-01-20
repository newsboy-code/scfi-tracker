import requests
import re
import pandas as pd
import sys

def get_scfi_data():
    # URL 주소를 다시 한번 점검합니다.
    url = "https://www.kcla.kr/web/inc/html/4-1_3.asp"
    
    # 실제 브라우저처럼 보이게 하는 필수 헤더 세트
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.kcla.kr/",
        "Connection": "keep-alive"
    }

    try:
        # 세션을 사용하여 쿠키 등을 유지하며 접속 시도
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30, verify=True)
        
        print(f"📡 최종 요청 URL: {response.url}")
        print(f"📡 응답 상태 코드: {response.status_code}")
        
        if response.status_code != 200:
            # 만약 404가 계속 뜬다면, www를 제거한 주소로 한 번 더 시도
            alt_url = url.replace("www.", "")
            print(f"⚠️ 404 에러 발생. 대안 주소로 시도: {alt_url}")
            response = session.get(alt_url, headers=headers, timeout=30)
            if response.status_code != 200:
                print("❌ 모든 시도가 실패했습니다. 사이트에서 깃허브 IP를 차단했을 수 있습니다.")
                sys.exit(1)

        html_text = response.text

        # 자바스크립트 변수 'line1' 안의 데이터를 직접 추출 (가장 확실한 방법)
        # 데이터 예시: ['16-Jan-26', 1574.12]
        pattern = r"\[\s*['\"](\d{2}-[a-zA-Z]{3}-\d{2})['\"]\s*,\s*([\d\.]+)\s*\]"
        matches = re.findall(pattern, html_text)

        if not matches:
            print("⚠️ 데이터를 찾지 못했습니다. HTML 구조를 분석합니다.")
            # 패턴 매칭이 안 될 경우 날짜 형식이 다를 수 있으므로 광범위한 패턴으로 재시도
            pattern = r"\[\s*['\"](.*?)['\"]\s*,\s*([\d\.]+)\s*\]"
            matches = re.findall(pattern, html_text)

        if matches:
            scfi_data = [{"날짜": d, "SCFI지수": v} for d, v in matches]
            df = pd.DataFrame(scfi_data)
            df.to_csv("scfi_data.csv", index=False, encoding='utf-8-sig')
            print(f"✅ 수집 성공! ({len(df)}건)")
        else:
            print("❌ 데이터 패턴 매칭 실패.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    get_scfi_data()
