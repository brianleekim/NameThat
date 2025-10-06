require('dotenv').config();
const express = require('express');
const cors = require('cors');
const searchAndGetLinks = require('spotify-preview-finder');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());

app.get('/preview', async (req, res) => {
  const { track, artist } = req.query;
  if (!track || !artist) {
    return res.status(400).json({ error: 'Missing track or artist parameter.' });
  }
  try {
    const results = await searchAndGetLinks(track, artist, 2);
    console.log('Results:', results);
    if (
      !results ||
      !results.results ||
      results.results.length === 0 ||
      !results.results[0] ||
      !results.results[0].previewUrls ||
      results.results[0].previewUrls.length === 0
    ) {
      return res.status(404).json({ error: 'No preview URL found.' });
    }
    // Return the first preview URL from the first result
    res.json({ preview: results.results[0].previewUrls[0], all: results });
  } catch (err) {
    res.status(500).json({ error: err.message || 'Internal server error.' });
  }
});

app.listen(PORT, () => {
  console.log(`Preview Finder server running on port ${PORT}`);
}); 