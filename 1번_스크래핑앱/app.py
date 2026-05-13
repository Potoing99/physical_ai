import json
import re
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen

HOST = "0.0.0.0"
PORT = 3000
SOURCE_URL = "https://news.naver.com/section/100"

INDEX_HTML = """<!doctype html>
<html lang=\"ko\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>1번 - 파이썬 스크래핑 앱</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    button { padding: 8px 14px; cursor: pointer; }
    li { margin: 6px 0; }
    .meta { color: #666; margin-top: 8px; }
  </style>
</head>
<body>
  <h1>네이버 정치 뉴스 스크래핑 (Python)</h1>
  <button id=\"loadBtn\">뉴스 불러오기</button>
  <div class=\"meta\" id=\"meta\"></div>
  <ul id=\"list\"></ul>

  <script>
    async function loadNews() {
      const list = document.getElementById('list');
      const meta = document.getElementById('meta');
      list.innerHTML = '<li>불러오는 중...</li>';
      meta.textContent = '';
      try {
        const res = await fetch('/api/news');
        const data = await res.json();
        list.innerHTML = '';
        if (!data.items || data.items.length === 0) {
          list.innerHTML = '<li>가져온 뉴스가 없습니다.</li>';
          return;
        }
        data.items.forEach(item => {
          const li = document.createElement('li');
          li.innerHTML = `<a href="${item.link}" target="_blank">${item.title}</a>`;
          list.appendChild(li);
        });
        meta.textContent = `출처: ${data.source} | 건수: ${data.count} | 시각: ${data.fetchedAt}`;
      } catch (e) {
        list.innerHTML = '<li>오류가 발생했습니다.</li>';
        meta.textContent = String(e);
      }
    }
    document.getElementById('loadBtn').addEventListener('click', loadNews);
  </script>
</body>
</html>
"""


def fetch_news():
  req = Request(SOURCE_URL, headers={
    "User-Agent": "Mozilla/5.0"
  })
  with urlopen(req, timeout=10) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

  pattern = re.compile(r'<a[^>]*class="[^"]*sa_text_title[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S)
  seen = set()
  items = []
  for href, raw_title in pattern.findall(html):
    title = re.sub(r"<[^>]+>", "", raw_title).strip()
    if not title or title in seen:
      continue
    seen.add(title)
    if href.startswith("/"):
      href = "https://news.naver.com" + href
    items.append({"title": title, "link": href})
    if len(items) >= 15:
      break

  return {
    "source": SOURCE_URL,
    "count": len(items),
    "items": items,
    "fetchedAt": datetime.utcnow().isoformat() + "Z"
  }


class Handler(BaseHTTPRequestHandler):
  def _send_json(self, code, obj):
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    self.send_response(code)
    self.send_header("Content-Type", "application/json; charset=utf-8")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def _send_html(self, code, html):
    body = html.encode("utf-8")
    self.send_response(code)
    self.send_header("Content-Type", "text/html; charset=utf-8")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def do_GET(self):
    if self.path == "/" or self.path == "/index.html":
      self._send_html(200, INDEX_HTML)
      return

    if self.path == "/api/news":
      try:
        data = fetch_news()
        self._send_json(200, data)
      except Exception as e:
        self._send_json(500, {"message": "뉴스를 가져오는 중 오류가 발생했습니다.", "detail": str(e)})
      return

    self._send_json(404, {"message": "Not Found"})


if __name__ == "__main__":
  server = HTTPServer((HOST, PORT), Handler)
  print(f"Server running at http://localhost:{PORT}")
  server.serve_forever()
