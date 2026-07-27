# 🎨 Screenshot Color Palette Extractor

A simple web app that extracts the dominant colors from any uploaded screenshot or image, and displays them as a clickable, copyable color palette with hex codes.

Upload an image → pick how many colors you want → get back a palette sorted by how much of the image each color covers.

---

## Live Demo

**[pixelhue.onrender.com](https://pixelhue.onrender.com/)**

---

## Features

- Drag-and-drop or click-to-upload image input
- Adjustable number of extracted colors (3–10)
- Dominant color detection using ColorThief
- Palette shown as swatches with hex code + % coverage
- Click any swatch to copy its hex code to your clipboard
- Uploaded images are deleted immediately after processing — nothing is stored

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python + Flask |
| Color extraction | Pillow (image processing) + ColorThief (dominant color extraction) |
| Frontend | Plain HTML, CSS, JavaScript (no framework) |

---

## Project Structure

```
color-palette-extractor/
│
├── app.py                  # Flask app (routes + server)
├── color_extractor.py      # Core logic: image → palette
├── requirements.txt        # Python dependencies
├── static/
│   ├── style.css           # Frontend styling
│   └── script.js           # Upload handling + rendering palette
├── templates/
│   └── index.html          # Main page (Jinja2 template)
├── uploads/                # Temporary storage for uploaded images
└── venv/                   # Virtual environment (not committed)
```

---

## Getting Started

### 1. Clone / create the project folder

```bash
mkdir color-palette-extractor && cd color-palette-extractor
```

### 2. Set up a virtual environment

```bash
python3 -m venv venv

# Activate it:
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

You'll know it worked when your terminal prompt shows `(venv)` at the start.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**What each package does:**
- **Flask** — runs the web server and handles routes/uploads
- **Pillow (PIL)** — opens and resizes the uploaded image, reads pixel data
- **scikit-learn** — runs K-Means clustering to find the dominant colors
- **numpy** — handles pixel arrays efficiently


---

## How It Works

1. User uploads an image → sent to `/extract` via `fetch()` as `FormData`
2. Flask saves it temporarily, then passes the file path to `extract_palette()`
3. ColorThief extracts the dominant colors using median cut algorithm
4. Each pixel is matched to its nearest dominant color to calculate coverage percentage
5. The uploaded file is deleted from disk
6. JSON response is sent back → JavaScript renders clickable swatches

---

## Configuration

| Setting | Where | Default |
|---|---|---|
| Max upload size | `app.py` → `MAX_CONTENT_LENGTH` | 10 MB |
| Allowed file types | `app.py` → `ALLOWED_EXTENSIONS` | png, jpg, jpeg, webp |
| Image resize (speed vs. detail) | `color_extractor.py` → `resize_to` | 150px |
| Number of colors | Adjustable in UI | 3–10 (default 6) |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Make sure `venv` is activated before running `pip install` or `python app.py` |
| `pip install` hangs / seems frozen | Run with `-v` for verbose output, or try `pip install --upgrade pip` first. See below for more. |
| Upload fails silently | Check `MAX_CONTENT_LENGTH` in `app.py` isn't smaller than your image |
| Colors look "muddy" | Increase `resize_to` in `extract_palette()` for more detail, or increase `num_colors` |
| Slow extraction | Lower `resize_to` (fewer pixels = faster K-Means) |
| CORS errors (frontend hosted separately) | Add `flask-cors` and enable it on the `/extract` route |

**If `pip install` seems stuck:**
```bash
pip install -r requirements.txt -v          # see verbose progress
pip install --upgrade pip                   # update pip resolver
pip install -r requirements.txt --no-cache-dir   # rule out a corrupted cache
```
`numpy` and `scikit-learn` can take a few minutes to install/build depending on your machine — it's often just slow, not frozen.

---

## Roadmap / Ideas

- [ ] Export palette as `.png` strip, `.css` variables file, or JSON download
- [ ] Drag-to-reorder swatches
- [ ] Save history of extracted palettes (`localStorage` or SQLite)
- [ ] Accept a URL instead of a file upload (screenshot a webpage server-side via Playwright/Selenium)
- [ ] Swap K-Means for the lighter-weight `colorthief` library

---

