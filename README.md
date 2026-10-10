# Movie Recommendation System

A movie discovery application that recommends titles with similar metadata. It pairs a Streamlit web interface with a FastAPI service and uses a precomputed similarity artifact to generate recommendations.

## Features

- Select a movie from the available catalog and view similar titles.
- Display movie posters retrieved from The Movie Database (TMDB), with a local fallback image when a poster is unavailable.
- Serve recommendations through a FastAPI endpoint.
- Explore the data preparation and similarity workflow in the included Jupyter notebook.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Streamlit user interface |
| `app.py` | FastAPI recommendation service |
| `image_url.py` | Looks up movie posters through TMDB |
| `recommendations.pkl` | Precomputed movie catalog and similarity data used by the application |
| `model.ipynb` | Notebook for preparing movie metadata and generating similarity data |
| `images.png` | Fallback image for titles without an available poster |
| `requirements.txt` | Python dependencies for the application |

## Requirements

- Python 3.9 or newer
- `pip`
- A TMDB API key for poster lookups (optional; the app uses its fallback image when the key is not configured)

## Setup

Open a terminal in the project directory and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

For poster lookups, create a `.env` file in the project directory and add your TMDB API key:

```dotenv
api_key=YOUR_TMDB_API_KEY
```

The application can run without this key, but poster lookups will be unavailable.

## Run the application

The interface and API run as separate processes. Keep both terminals open, and start each command from the project directory so the application can find `recommendations.pkl` and `images.png`.

In the first terminal, start the recommendation API:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal, start the Streamlit interface:

```bash
streamlit run main.py
```

Streamlit will print the local address for opening the interface in a browser. The interface sends recommendation requests to the API at `http://localhost:8000`.

## API

The application exposes a `POST /recommend` endpoint. Send a movie ID in the request body:

```json
{
  "id": 19995
}
```

The response is a JSON array of recommended movie titles. For example, with `curl`:

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"id": 19995}'
```

## Rebuilding the recommendation data

The application uses the included `recommendations.pkl` artifact at runtime. The notebook documents a workflow that combines movie metadata, creates TF-IDF vectors from the prepared tags, calculates cosine similarities, and saves the resulting catalog and similarity data.

To run the notebook, install Jupyter and scikit-learn in the environment:

```bash
pip install jupyter scikit-learn
jupyter notebook model.ipynb
```

The notebook expects `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` in the project directory. Those source CSV files are not included in the provided project files. Place the datasets there before rerunning the notebook. The generated `recommendations.pkl` must remain in the project directory for the API to load it.

## Troubleshooting

- **The interface cannot reach the API:** Make sure the FastAPI service is running on port `8000`.
- **The API cannot find the recommendation data:** Start the API from the project directory and confirm that `recommendations.pkl` is present.
- **Posters are missing:** Confirm that the `.env` file contains a valid `api_key`; missing keys and titles without posters use the fallback image where available.

