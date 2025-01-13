# AI Scraping Engine

This project is an AI-powered scraping engine built with Python 3.12, leveraging the power of Large Language Models (LLMs) for advanced and intelligent web scraping.

## Features

* **Intelligent Scraping:** Utilizes LLMs to understand webpage structure and extract data with high accuracy.
* **Flexible and Adaptable:** Easily adapts to different website layouts and data formats.
* **FastAPI Backend:** Provides a robust API for interacting with the scraping engine.
* **Streamlit Frontend:** Offers an intuitive user interface for managing scraping tasks and visualizing results.

## Setup

### Prerequisites

* Python 3.12

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/chai-dev682/decodata-RAG-llama.git 
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the FastAPI backend:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
2. **Start the Streamlit frontend:**
   ```bash
   streamlit run .\app.py 
   ```

## Usage

Once both the backend and frontend are running, you can access the Streamlit UI in your browser at `http://localhost:8501`. 

From the UI, you can:

* Define scraping tasks by specifying target URLs and desired data points.
* Monitor the progress of scraping tasks.
* View and scraped data.
