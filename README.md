
# Pinterest_Pin_Title_Generator

#### Welcome to the Pinterest Pin Title Generator Bot! 🎉

This bot helps you create catchy, SEO-friendly Pinterest pin titles based on keywords using the power of ChatGPT and Google Sheets API. Perfect for Pinterest marketers and content creators looking to level up their pin game and save time on title generation!

## Features 🌟

AI-Generated Titles: Generates unique, optimized titles for Pinterest pins based on your keywords.

Google Sheets Integration: Easily read and write keywords and titles using Google Sheets.

Fully Automated: Get customized titles for all your pins with just a few clicks.

### How It Works ⚙️

Enter Keywords: Add your keywords to a Google Sheet.

Generate Titles: The bot pulls in keywords, runs them through ChatGPT, and returns engaging, optimized pin titles.

Save to Google Sheets: The results are added back to your sheet for easy access and editing.

## Setup Guide 🛠️

To set up the bot, follow these steps:

* Clone the Repo: Download or clone this repository to your local machine.

### Google Cloud Setup:

* Go to the Google Cloud Console, create a new project, and navigate to the "APIs & Services" section.

* Enable the Google Sheets API and Google Drive API for your project.

* Create a Service Account:

* Go to Credentials > Manage Service Accounts.

* Click on the service account you just created, then go to Manage Keys and Create New JSON Key.

* Download the JSON key file and place it inside the data folder as keyfile.json.

* Google Sheet ID:

* Identify the Google Sheet ID from the URL of the Google Sheet you want to use. For example, in the URL https://docs.google.com/spreadsheets/d/12345/edit?gid=0#gid=0, 12345 is the Google Sheet ID.

## Sheet Structure:

Ensure your Google Sheet has these three tables with the specified columns=> prompt_builder: Columns: Keyword, Title Prompt, Final Title Prompt, Description Prompt (raw), Final Description Prompt, Tips Prompt (raw), Final Tips Prompt video_prompts: Columns: Keyword, Title Prompt, Description Prompt image_prompts: Columns: Keyword, Title Prompt, Description Prompt, Tips Prompt Environment Variables:
Here is a Sample google sheet that this generator uses.

Set up your Google Sheets API credentials and OpenAI API key in your environment variables for secure access.

Once everything is set up, run the bot script to start generating Pinterest pin titles based on your keyword list!

### Requirements 📋

Python 3.x Google Sheets API credentials


#### 🔗 Links

[![Link to Sample Google Sheet](https://img.shields.io/badge/Link%20to%20Sample%20Google%20Sheet-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)](https://docs.google.com/spreadsheets/d/1tDcDFL8HpBuVMvoDKpG-_YGx--WLhoukacQ8Cdtur5I/edit?usp=sharing)
