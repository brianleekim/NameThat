const express = require('express');
const cors = require('cors');
const { getPreviewUrl } = require('spotify-preview-finder');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());

app.get('/preview', async (req, res) => {
  const { track, artist } = req.query;
  if (!track || !artist) {
    return res.status(400).json({ error: 'Missing track or artist parameter.' });
  }
  try {
    const url = await getPreviewUrl({ track, artist });
    if (!url) {
      return res.status(404).json({ error: 'No preview URL found.' });
    }
    res.json({ preview: url });
  } catch (err) {
    res.status(500).json({ error: err.message || 'Internal server error.' });
  }
});

app.listen(PORT, () => {
  console.log(`Preview Finder server running on port ${PORT}`);
}); 