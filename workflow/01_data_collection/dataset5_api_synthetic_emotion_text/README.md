# Dataset 5: API-Generated Emotion Text

This folder addresses Part 1.3, API interaction for structured data retrieval.
It uses a generative API to create structured urban emotion observations for
the project theme: an emotional city map.

The output is not a replacement for scraped datasets. It is an augmentation
dataset that helps translate emotional descriptions into spatial rules.

## How to Run

Set your OpenAI API key:

```powershell
$env:OPENAI_API_KEY="YOUR_KEY_HERE"
python workflow\01_data_collection\dataset5_api_synthetic_emotion_text\scripts\generate_emotion_text_api.py --items-per-category 40
```

This creates:

```text
outputs/api_emotion_text_dataset.csv
outputs/api_emotion_text_dataset.json
```

Do not upload API keys or `.env` files to GitHub.
