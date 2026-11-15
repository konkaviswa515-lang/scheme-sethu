# Scheme Sethu

A voice-first assistant that helps rural citizens and farmers find government schemes in Telugu and English. The user speaks, the app extracts the details, plain Python rules decide eligibility, and the result is explained in simple language with voice, documents checklist and an official source link.

The whole project is Python and runs on Streamlit.

## Problem statement

Many people know a scheme exists but not the eligibility, amount, documents or how to apply. Official information is mostly in English or formal language, rules are spread across many portals, and typing is hard for many users. Scheme Sethu lets them speak in their own language and get a clear answer.

## Why this is different

| Tool | What it does | What Scheme Sethu adds |
|---|---|---|
| Jugalbandi | WhatsApp chatbot for scheme questions | Web app with a rule-based eligibility check, not only answers from text |
| Kisan e-Mitra | Voice and text help for PM-KISAN only | Many schemes across farmer and citizen flows |
| MyScheme | Government portal with filters and forms | Voice-first input and spoken answers in Telugu |
| Haqdarshak | Scheme discovery with human agents | Fully automated and free to run |

This comparison is based on public descriptions of these tools. Please re-check it before you present.

Features that are part of this prototype:

1. Rule-based eligibility engine. Rules live in JSON and only Python code decides eligibility. The LLM never decides eligibility or amounts.
2. Almost-eligible engine. If a user misses by a small margin, the app shows the margin and suggests other schemes that fit.
3. Documents checklist with guidance on where to get each missing document.
4. Separate farmer and citizen flows with different questions.
5. Official source link and last updated date on every result.
6. Low-bandwidth mode with text only and no audio.
7. Feedback buttons saved to `feedback.json`.

## Architecture

```
User voice or text
      |
      v
Streamlit UI (app.py)
      |
      +--> SpeechRecognition (te-IN, en-IN)      speech to text
      |
      +--> nlp.py: keyword extraction, or OpenAI extraction if a key is set
      |
      +--> ask for missing details, then confirm with the user
      |
      +--> schemes_loader.py: load citizen.json or farmer.json, filter by state
      |
      +--> eligibility.py: eligible, almost eligible, not eligible (pure Python rules)
      |
      +--> nlp.py: simple explanation (template, or OpenAI rewrite of the same facts)
      |
      +--> gTTS: spoken summary (skipped in low-bandwidth mode)
      |
      v
Result cards: benefit, reason, documents checklist, how to apply, source, last updated
      |
      v
Feedback (feedback.json)
```

## Project structure

```
scheme-sethu/
├── app.py
├── eligibility.py
├── nlp.py
├── schemes_loader.py
├── data/schemes/citizen.json
├── data/schemes/farmer.json
├── feedback.json
├── requirements.txt
├── packages.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

`nlp.py` holds extraction, explanation and speech-to-text so that `app.py` stays about the interface.

## Install and run

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate with `.venv\Scripts\activate`.

The browser records the audio, so you do not need PyAudio. Speech recognition uses Google's free web service, so it needs internet. If the microphone fails, the app falls back to the text box.

## Environment setup

The app works without any key, using keyword extraction and template explanations.

To turn on the AI assistant:

```
cp .env.example .env
```

Then put your key in `.env`:

```
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

Never commit `.env`. It is already in `.gitignore`.

## How eligibility rules work

Each scheme in the JSON files has `eligibility_rules`. Supported rules:

| Rule | Meaning |
|---|---|
| `income_lt` | Family income up to the value (inclusive) |
| `land_lt_acre` | Land up to the value in acres (inclusive) |
| `land_gt_acre` | Land more than the value in acres |
| `category_in` | Category must be in the list |
| `age_between` | Age within `[min, max]` |
| `age_gte` | Age at least the value |
| `crop_in` | Crop must be in the list |
| `student_is` | `true` for students only |
| `gender_in` | Gender must be in the list |
| `irrigation_in` | Water source must be in the list |

A scheme is almost eligible when exactly one numeric rule fails and the gap is within 20 percent of the limit (3 years for age rules).

To add a scheme, add an entry to `citizen.json` or `farmer.json` with the same fields and the rules above.

## Data accuracy

The sample data covers 12 schemes. Amounts and limits were entered from public sources and can change, so check each scheme on its official link and update `last_updated` before you demo or publish. Some real conditions are not modelled, for example BPL status for the old age pension, pregnancy for the maternity scheme, and exclusions for PM-KISAN. These appear as a note on the result card.

On Streamlit Cloud the file system resets on restart, so `feedback.json` is not permanent there.

## Deploy to Streamlit Cloud

1. Push this folder to a public GitHub repository.
2. Go to share.streamlit.io and sign in with GitHub.
3. Click New app, choose your repository and branch `main`, and set the main file to `app.py`.
4. Open Advanced settings and paste `OPENAI_API_KEY = "your_key_here"` under Secrets if you want the AI assistant. Skip this to use keyword mode.
5. Click Deploy. `packages.txt` installs ffmpeg for audio conversion.

## License

MIT. See `LICENSE`.
