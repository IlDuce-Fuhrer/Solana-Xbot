const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');

const app = express();
const PORT = 3000;

// Basic route to test the server
app.get('/', (req, res) => {
  res.send('Solana-XBot Server is running.');
});

// Scraping function
async function scrapeTwitter(username) {
  try {
    const url = `https://nitter.net/search?f=tweets&q=${username.replace(' ', '+')}`;
    
    console.log(url)
    const { data } = await axios.get(url);
    const $ = cheerio.load(data);

    const posts = [];
    console.log('scraping')
    $('div.timeline-item').each((i, el) => {
      const text = $(el).find('.tweet-content').text().trim();
      const time = $(el).find('span.tweet-date a').attr('title');
      posts.push({ text, time });
    });

    return posts;
  } catch (error) {
    console.error('Scrape error:', error.message);
    return [];
  }
}

// Scrape route
app.get("/scrape/:username", async (req, res) => {
  const username = req.params.username;
  
  try {
    console.log('trying')
    // const { data } = await axios.get(url);
    const data = await scrapeTwitter(username)
    
    console.log(data); // 👈 this logs the raw HTML of the page

    const $ = cheerio.load(data);
    const tweets = [];

    $(".timeline-item").each((index, element) => {
      const content = $(element).find(".tweet-content").text().trim();
      tweets.push(content);
    });

    res.json(tweets);
  } catch (error) {
    console.error("Scraping error:", error.message);
    res.status(500).send("Failed to scrape.");
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
