# FMI Script

## Introduction

The FMI Script is part of a larger iOS device management project, designed to disable the Find My iPhone feature. This script is open for public use and contribution.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/liomuguchia/fmi-off.git
    cd fmi-script
    ```

2. **Install Python 3:**

    If you don't have Python 3 installed, you can download it from [Python's official website](https://www.python.org/downloads/).

3. **Install pip dependencies:**

    Open a terminal in the project directory and run the following command to install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

    If you encounter any issues, make sure to install each package individually using `pip install package-name`.

4. **Download chromedriver:**

    For Selenium to work with Chrome, you need to download chromedriver. Download it from [here](https://sites.google.com/chromium.org/driver/) and make sure it's in your system's PATH.

5. **Check required Python packages:**

    Open a terminal in the project directory and run the following command to check if required Python packages are installed:
    ```bash
    python -c "import time, selenium, os, json, subprocess, re, webbrowser, sys, random, threading; print('All dependencies are installed')"
    ```

## Usage

Run the script:
```bash
python FMI.py
```

Follow the on-screen instructions to provide the Apple Support confirmation link and choose the desired entry method (auto or manual).

### Disclaimer
This script is provided as-is and is not intended for malicious purposes. Ensure that you have the right to use and modify the script according to your needs. Use it responsibly and in compliance with Apple's terms and conditions.
https://support.apple.com/HT201365
https://www.apple.com/legal/internet-services/icloud/en/terms.html

### Author
Leomuguchia
GitHub: leomuguchia
https://www.buymeacoffee.com/muguchialio
