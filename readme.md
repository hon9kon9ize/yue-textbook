# Yue Textbook Generator

This repository contains code for generating an educational knowledge dataset in Cantonese (Yue) that is optimized for LLM training. The generator creates textbook-style content from Wikipedia articles, transforming them into structured educational material.

## Overview

The Yue Textbook Generator crawls Wikipedia articles in Cantonese (specifically focusing on Hong Kong-related content) and transforms them into comprehensive educational materials including:

- Custom educational topics derived from the source material
- Structured outlines with bilingual points (Cantonese/English)
- Detailed lectures in Markdown format
- Glossaries of specialized terminology

The resulting dataset is designed to be easily consumable for training Large Language Models (LLMs) on Cantonese educational content.

## Features

- **Intelligent Topic Selection**: Focuses on Hong Kong-related topics from Cantonese Wikipedia
- **Content Transformation**: Converts encyclopedia articles into structured educational resources
- **Bilingual Elements**: Creates content with bilingual components to enhance language learning
- **Content Filtering**: Removes irrelevant sections and ensures quality thresholds
- **Format Standardization**: Outputs in consistent Markdown format for easy processing
- **Proxy Support**: Includes proxy configuration for API access from restricted regions

## Requirements

- Python 3.6+
- Pandas
- Requests
- tqdm
- tenacity
- wikipedia-api

## Configuration

Before running the code, you need to set the following:

- Google AI Studio API key
- Nord VPN credentials (if using proxy)

## How It Works

1. **Data Collection**: Extracts Hong Kong-related articles from Cantonese Wikipedia
2. **Content Filtering**: Removes irrelevant sections and ensures minimum content length
3. **Prompt Engineering**: Uses carefully designed prompts for the Gemini to transform content
4. **Content Generation**: Creates educational materials with four components:
   - Topic selection
   - Outline creation
   - Detailed lecture
   - Terminology glossary
5. **Quality Control**: Filters out content that contains too many Simplified Chinese characters
6. **Output**: Saves generated textbooks as Markdown files

## Output Format

Each generated textbook includes:

```
<topic>
[Topic Title]
</topic>

<outline>
1. [Point 1] ([English Translation])
2. [Point 2] ([English Translation])
...
</outline>

<lecture>
[Detailed educational content in Markdown format]
</lecture>

<glossary>
| Term | Definition |
|------|------------|
| Term 1 | Definition 1 |
...
</glossary>
```

## Usage

```python
# Configure your API keys
GOOGLE_AISTUDIO_API_KEY = 'your_api_key'
NODRVPN_SERVICE_USERNAME = 'your_username'
NODRVPN_SERVICE_PASSWORD = 'your_password'

# Run the generator
num_textbooks = 10000  # Target number of textbooks to generate
# The script will automatically run until this number is reached
```

## Limitations

- Requires API access to Google's Gemini Pro model
- Generation can be time-consuming due to API rate limits
- May require proxies depending on your location

## License

Pending

## Acknowledgements

- Wikipedia for providing the source material
- Google for the Gemini Pro API