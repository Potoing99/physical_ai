const fs = require('fs');
const path = require('path');

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`[생성] 폴더: ${dirPath}`);
  } else {
    console.log(`[유지] 폴더 이미 존재: ${dirPath}`);
  }
}

function writeFile(filePath, content) {
  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`[생성] 파일: ${filePath}`);
}

function main() {
  const baseDir = process.cwd();

  // 1) 하위 폴더 만들기
  const subDirs = ['posts', 'assets', 'drafts'];
  subDirs.forEach((dir) => ensureDir(path.join(baseDir, dir)));

  // 2) 블로그 시리즈 목차(3편) 작성 -> index.md
  const indexContent = `# 블로그 시리즈 목차 (3편)\n\n` +
`## 시리즈 주제: CSV 데이터로 시작하는 데이터 시각화\n\n` +
`1. **1편 - CSV 데이터 읽기와 전처리 기초**\n` +
`   - CSV 구조 이해\n` +
`   - 필요한 컬럼 선택\n` +
`   - 결측치/형변환 처리\n\n` +
`2. **2편 - 추이 그래프(line chart) 만들기**\n` +
`   - 시간축 데이터 정렬\n` +
`   - 시계열 시각화 구성\n` +
`   - 그래프 해석 포인트\n\n` +
`3. **3편 - 결과 공유와 리포트 작성**\n` +
`   - 그래프 결과 정리\n` +
`   - 인사이트 문장화\n` +
`   - 재현 가능한 실행 방법 정리\n`;
  writeFile(path.join(baseDir, 'index.md'), indexContent);

  // 3) 1편 초안 작성 -> post1.md
  const post1Content = `# 1편 초안: CSV 데이터 읽기와 전처리 기초\n\n` +
`## 들어가며\n` +
`데이터 분석의 시작은 대부분 CSV 파일입니다. 이번 글에서는 CSV를 읽고,\n` +
`그래프를 그리기 전에 꼭 필요한 전처리 과정을 간단히 정리합니다.\n\n` +
`## 1) CSV 구조 파악\n` +
`먼저 헤더(컬럼명)를 확인하고, 어떤 컬럼을 사용할지 결정합니다.\n` +
`예를 들어 기온 추이 분석이라면 date, meantemp 컬럼이 핵심입니다.\n\n` +
`## 2) 컬럼 선택과 타입 변환\n` +
`date는 날짜형으로, meantemp는 숫자형으로 다루어야 합니다.\n` +
`타입이 맞지 않으면 그래프가 깨지거나 계산 결과가 잘못될 수 있습니다.\n\n` +
`## 3) 결측치/이상치 처리\n` +
`빈 값이 있는 행은 제거하거나 보정합니다.\n` +
`극단값이 있다면 기준을 정해 제외 여부를 판단합니다.\n\n` +
`## 마무리\n` +
`전처리는 분석 품질을 좌우합니다.\n` +
`다음 편에서는 정리된 데이터를 바탕으로 추이 그래프를 실제로 만들어보겠습니다.\n`;
  writeFile(path.join(baseDir, 'post1.md'), post1Content);

  console.log('\n[완료] 3개 작업을 순서대로 처리했습니다.');
}

main();
