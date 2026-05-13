const fs = require('fs');
const path = require('path');

function parseCsv(text) {
  const lines = text.split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) throw new Error('CSV 데이터가 충분하지 않습니다.');

  const header = lines[0].split(',').map((h) => h.trim());
  const dateIdx = header.findIndex((h) => h.toLowerCase() === 'date');
  const tempIdx = header.findIndex((h) => h.toLowerCase() === 'meantemp');

  if (dateIdx === -1 || tempIdx === -1) {
    throw new Error("필수 컬럼(date, meantemp)을 찾을 수 없습니다.");
  }

  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].split(',');
    const date = (cols[dateIdx] || '').trim();
    const tempRaw = (cols[tempIdx] || '').trim();
    const temp = Number(tempRaw);

    if (!date || Number.isNaN(temp)) continue;
    rows.push({ date, meantemp: temp });
  }

  if (rows.length === 0) {
    throw new Error('유효한 데이터 행이 없습니다.');
  }

  rows.sort((a, b) => new Date(a.date) - new Date(b.date));
  return rows;
}

function resolveInputCsv(argvInput) {
  if (argvInput) return path.resolve(argvInput);

  const cwd = process.cwd();
  const preferred = path.join(cwd, 'DailyDelhiClimateTrain.csv');
  if (fs.existsSync(preferred)) return preferred;

  const sample = path.join(cwd, 'sample_daily_delhi_climate.csv');
  if (fs.existsSync(sample)) return sample;

  const firstCsv = fs.readdirSync(cwd).find((f) => f.toLowerCase().endsWith('.csv'));
  if (firstCsv) return path.join(cwd, firstCsv);

  throw new Error('CSV 파일을 찾을 수 없습니다. 이 폴더에 CSV 파일을 넣어주세요.');
}

function buildHtml(labels, values, sourceName) {
  return `<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CSV 추이 그래프</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    h1 { margin-bottom: 8px; }
    .meta { color: #555; margin-bottom: 16px; }
    .chart-wrap { max-width: 1000px; }
  </style>
</head>
<body>
  <h1>Daily Delhi Climate - 평균기온 추이</h1>
  <div class="meta">소스 CSV: <strong>${sourceName}</strong></div>
  <div class="chart-wrap">
    <canvas id="trendChart"></canvas>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    const labels = ${JSON.stringify(labels)};
    const dataValues = ${JSON.stringify(values)};

    const ctx = document.getElementById('trendChart');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: '평균기온(meantemp)',
          data: dataValues,
          borderWidth: 2,
          tension: 0.2,
          pointRadius: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: '날짜(date)' } },
          y: { title: { display: true, text: '평균기온' } }
        }
      }
    });
  </script>
</body>
</html>`;
}

(function main() {
  try {
    const inputArg = process.argv[2];
    const inputCsvPath = resolveInputCsv(inputArg);
    const csvText = fs.readFileSync(inputCsvPath, 'utf8');
    const rows = parseCsv(csvText);

    const labels = rows.map((r) => r.date);
    const values = rows.map((r) => r.meantemp);

    const outputHtml = buildHtml(labels, values, path.basename(inputCsvPath));
    const outputPath = path.join(process.cwd(), 'output.html');
    fs.writeFileSync(outputPath, outputHtml, 'utf8');

    console.log('[완료] output.html 생성:', outputPath);
    console.log('[정보] 사용한 CSV:', inputCsvPath);
    console.log('[정보] 데이터 건수:', rows.length);
  } catch (err) {
    console.error('[오류]', err.message);
    process.exit(1);
  }
})();
