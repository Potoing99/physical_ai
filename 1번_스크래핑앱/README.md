# 1번 과제: 인터넷 정보 스크래핑 결과 출력 앱

## 과제 개요
- 네이버 뉴스(정치 섹션)에서 제목/링크를 스크래핑
- 서버 API로 결과(JSON) 제공
- 정적 페이지(`public/index.html`)에서 확인 가능

## 주요 파일
- `server.js` : Express 서버 + 스크래핑 API
- `public/index.html` : 프론트 화면
- `package.json` : 실행 스크립트 및 의존성

## 실행 방법
```bash
npm install
npm start
```

실행 후 접속:
- 웹 화면: `http://localhost:3000`
- API: `http://localhost:3000/api/news`

## 비고
- 현재는 로컬 실행 기준이며,
- 필요 시 Render/Railway 등에 배포해서 실제 공개 URL로 제출 가능합니다.
