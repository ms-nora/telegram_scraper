# Telegram Scraper - Research Tool

## Overview
This tool uses the **Telethon** library to search for **Telegram groups and channels** based on keywords, extract **members and links**, and save the results in a CSV file. It is designed for **research and investigative purposes only**.

## Features
- **Search Telegram groups and channels** using keywords
- **Extract user data** (User ID, Username, First & Last Name)
- **Extract shared links** from messages
- **Save results in a structured CSV file**
- **Handles Telegram API rate limits** automatically
- **Supports keyword input from a file (`keywords.txt`)**

## Prerequisites
1. **Python 3.8+**
2. Install required dependencies:
   ```bash
   pip install telethon pandas
   ```
3. **Telegram API Credentials**
   - Register for an API ID and API Hash at [my.telegram.org/apps](https://my.telegram.org/apps)
   - Replace `API_ID` and `API_HASH` in the script with your actual credentials

## Setup Instructions
### 1️ Define Keywords
- Create a **`keywords.txt`** file in the same directory.
- Add one keyword per line (e.g., group topics, research terms, etc.).
- If the file is missing, the script will use predefined example keywords.

### 2️ Run the Script
Execute the script in your terminal:
```bash
python script.py
```

## Expected Output
- The script logs into Telegram, **searches for groups and channels**, and **extracts relevant data**.
- The data is saved in **`telegram_scrape_results.csv`**.
- If a rate limit is hit, the script **waits and retries automatically**.

## License
This project is released under the **MIT Research-Only License**:
- **For research and investigative purposes only**.
- **No commercial use is allowed without permission**.
- **Must comply with all relevant laws and regulations**.

## Disclaimer
- **Use this tool responsibly** and in accordance with **Telegram's API Terms of Service**.
- Unauthorized scraping of private data may **violate privacy laws**.
- The author is **not responsible for misuse** of this tool.

## Contributions
Contributions to improve the tool are welcome. Submit a **pull request** or report issues via GitHub.





## License
This project is licensed under the **MIT Research-Only License**.

**Allowed Uses:**
- Academic research
- Law enforcement investigations
- Forensic analysis

**Restrictions:**
- No commercial use without permission
- No use for unauthorized surveillance, cybercrime, or malicious intent

See the [LICENSE](LICENSE) file for details.
