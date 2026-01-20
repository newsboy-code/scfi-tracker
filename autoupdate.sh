#!/bin/bash
# 1. 파일이 있는 폴더로 이동
cd $(dirname "$0")

# 2. 파이썬 스크립트 실행 (데이터 수집)
python3 scraper.py

# 3. 깃허브로 변경사항 전송
git add scfi_data.csv
git commit -m "자동 업데이트: $(date +'%Y-%m-%d %H:%M')"
git push origin main
