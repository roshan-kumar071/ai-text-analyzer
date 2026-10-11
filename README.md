# AI Text Analyzer

A beginner-friendly web application that analyzes text using Python and Flask.

## Features

- Count words and characters
- Count characters without spaces
- Count sentences and paragraphs
- Find the five most frequent words
- Perform basic rule-based sentiment analysis
- Responsive web interface
- Live character counter
- Clear text input

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript

## Project Structure

```text
ai-text-analyzer/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── templates/
    └── index.html
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-text-analyzer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

## How Sentiment Analysis Works

The current version uses predefined positive and negative English word lists. It compares the number of matching words to classify the text as Positive, Negative, or Neutral.

This is a basic rule-based approach, not a trained machine-learning model. It may not correctly interpret negation, sarcasm, or context.

## Future Improvements

- Integrate a trained sentiment-analysis model
- Improve sentiment detection for negation and context
- Add text export functionality
- Add automated tests

## Learning Purpose

This project was created to practice Python, Flask, frontend development, text processing, and GitHub version control.