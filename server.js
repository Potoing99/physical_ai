const express = require("express");
const axios = require("axios");
const cheerio = require("cheerio");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, "public")));

app.get("/api/news", async (req, res) => {
  try {
    const url = "https://news.naver.com/section/100";
    const { data: html } = await axios.get(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
      },
      timeout: 10000,
    });

    const $ = cheerio.load(html);
    const seen = new Set();
    const articles = [];

    $("a.sa_text_title").each((_, el) => {
      const title = $(el).text().trim();
      const href = $(el).attr("href");

      if (!title || !href || seen.has(title)) return;
      seen.add(title);
      articles.push({ title, link: href });
    });

    res.json({
      source: url,
      count: articles.length,
      items: articles.slice(0, 15),
      fetchedAt: new Date().toISOString(),
    });
  } catch (error) {
    res.status(500).json({
      message: "뉴스를 가져오는 중 오류가 발생했습니다.",
      detail: error.message,
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
