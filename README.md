# Wikipedia-in-Space

Let's try to use AI to find the path between two completely unrelated topics on wikipedia [like this!](https://www.thewikigamedaily.com/)

## What it does

Wikipedia-in-Space navigates from one Wikipedia article to another by intelligently following links. Instead of randomly clicking around, it uses a cross-encoder model to predict which links are most likely to lead toward your target article. 

## How it works

1. **Start somewhere** - Pick any Wikipedia article
2. **Set a destination** - Choose where you want to end up
3. **Let the AI navigate** - The tool uses a cross-encoder model to score all available links and picks the most promising path
4. **Watch it go** - It backtracks when stuck and avoids cycles until it reaches the target.

The magic happens through semantic similarity scoring—the model understands which links are conceptually closer to your target.

## Setup

You'll need a Hugging Face token to use the cross-encoder model:

1. Copy `.env.example` to `.env`
2. Add your Hugging Face token: `HF_TOKEN=your_token_here`
3. Install dependencies: `uv sync`

## Usage

Just run the main script and watch it navigate:

```bash
python src/SpiderVerse.py
```

Want to try different start/end points? Edit the last two lines in `SpiderVerse.py`:

```python
spider_verse = SpiderVerse(start_term="Your Start", target_term="Your Target")
spider_verse.enter_the_spiderverse(max_iterations=10)
```

## Example output

```
 Entering the SpiderVerse...
──────────────────────────────────────────────────
Start:  Keir Starmer
Target: The Simpsons
──────────────────────────────────────────────────

  → United Kingdom (87.3%)
  → Television (92.1%)
  → Animated sitcom (95.4%)
  → The Simpsons (98.7%)

──────────────────────────────────────────────────
✓ Success! Reached target in 4 iterations
```

## Tech stack

- **sentence-transformers** - Cross-encoder model for semantic similarity
- **wikipedia** - Python API wrapper for Wikipedia
- **thefuzz** - Fuzzy string matching to detect when we've arrived
- **python-dotenv** - Environment variable management