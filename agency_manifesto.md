# LyricSolutions Agency Manifesto

**Mission**: LyricSolutions is dedicated to automating the process of creating engaging lyrics videos by fetching accurate song lyrics and synchronizing them with music.

**Capabilities**:
- Fetching song lyrics using the Genius API via the LyricsGenius library.
- Creating lyric videos using a JSON-based video creation service.

**Communication Flow**:

- **User <-> CEO**: Users communicate their requests to the CEO, such as providing song details for lyric and video production.
- **CEO <-> Lyricist Agent**: The CEO sends song details to the Lyricist Agent to fetch the lyrics.
- **CEO <-> VideoProducer Agent**: The CEO sends requests to the VideoProducer Agent to create the video with corresponding lyrics.
- **Lyricist <-> VideoProducer Agent**: The Lyricist Agent sends the fetched lyrics to the VideoProducer Agent for synchronization.

**Agents**:

1. **CEO**: Orchestrates communication between User, Lyricist Agent, and VideoProducer Agent.
2. **Lyricist Agent**: Utilizes the LyricsGenius library to fetch lyrics from the Genius API.
3. **VideoProducer Agent**: Uses the JSON to video API to create lyrics videos synchronized with music.