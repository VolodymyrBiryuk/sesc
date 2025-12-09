# 🕸️ SeSc

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight, **Python web scraper** powered by **Selenium WebDriver**.  

---

## 🚀 Features

- Selenium-based content rendering  
- CAPTCHA solving  
- Custom Javascript injection  

---

## 📦 Requirements

- Python 3.13+  
- uv
- Selenium `>= 4.0`  
- Chrome Browser

---

## 🔧 Installation

```bash
git clone https://github.com/volodymyrbiryuk/sesc.git
cd sesc
uv sync
```

## Usage

```python
from sesc.src import scraper

for markup  in scraper.download_rendered_markup(['https://google.com']):
    print(markup)
```

## License
This project is licensed under the MIT License — see the [LICENSE](./LICENSE.md) file for details.
