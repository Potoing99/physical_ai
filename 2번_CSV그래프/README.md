# 2번 과제: CSV 추이 그래프 출력 (Kaggle Daily Delhi Climate 기준)

## 과제 목표
- CSV 파일을 읽어서
- 날짜별 추이 그래프를 만들고
- 결과를 파일(`output.html`)로 출력

## 권장 데이터셋 (Kaggle)
- Daily Delhi Climate Data
- 보통 파일명 예시: `DailyDelhiClimateTrain.csv`
- 주요 컬럼: `date`, `meantemp`

## 폴더 구성
- `generate_chart_html.js` : CSV를 읽어 그래프 HTML 생성
- `sample_daily_delhi_climate.csv` : 실행 확인용 샘플 CSV
- `output.html` : 실행 후 생성되는 결과 파일

## 실행 방법
1) CSV 파일을 이 폴더에 둡니다. (없으면 샘플 CSV를 자동 사용)
2) 아래 명령 실행

```bash
node generate_chart_html.js
```

선택적으로 파일 지정도 가능:

```bash
node generate_chart_html.js DailyDelhiClimateTrain.csv
```

3) 생성된 `output.html`을 브라우저로 열어 그래프를 확인합니다.

## 참고
- 그래프 렌더링은 HTML 내부에서 Chart.js CDN을 사용합니다.
- 과제 제출 시에는 Kaggle 원본 CSV 파일명/출처를 함께 적는 것을 권장합니다.
