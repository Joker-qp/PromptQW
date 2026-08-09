# 🤖 Interactive Prompt Architect (PromptQW)

![version](https://img.shields.io/badge/version-v1.0.0-orange.svg)
![python](https://img.shields.io/badge/python-3.10+-3776AB.svg?logo=python&logoColor=white)
![fastapi](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)
![streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-green.svg)

> 🇹🇷 *Türkçe dokümantasyon için [buraya tıklayın](#-türkçe-dokümantasyon).*

**Interactive Prompt Architect (PromptQW)** is a modern, local-first, multi-model AI prompt engineering wizard that matures raw concepts into production-grade prompts through interactive AI-guided questioning, domain-specific options, and encrypted security.

---

## ✨ Key Features

- 🎯 **2-Stage Dynamic Prompt Wizard:** Analyzes your initial idea, generates targeted clarifying questions via LLM, and builds a professional prompt based on your answers.
- 🔒 **Local-First & Encrypted Security:** API keys are encrypted locally in SQLite using `Fernet 256-bit` symmetric encryption. Your keys and prompts never leave your local environment.
- 🤖 **Multi-Provider LLM Integration:**
  - **Google Gemini:** `gemini-2.5-flash`, `gemini-1.5-pro`, etc.
  - **OpenRouter:** `DeepSeek R1/V3`, `Claude 3.5 Sonnet`, `GPT-4o`, `Free Models`, etc.
- 🌐 **Rich Domain & Multi-Tier Sub-Options:**
  - Includes *General*, *Software Development*, *Data Science & AI*, *Content Creation*, *Academic & Research*, *Business & Marketing*, and *History & Social Sciences*.
  - Optional 2-tier toggles (Basic & Advanced Sub-Options) that conditionally inject context into the prompt processing.
- 📊 **Real-time Token Estimator:** Instant input/output token estimation before and after generation.
- 🇹🇷 **Educational Turkish Output:** Generates structured English prompts alongside precise Turkish translations and educational usage guides tailored to your knowledge level.
- 🚀 **One-Click Launchers:** Pre-configured `BAŞLAT.bat` (Windows) and `BAŞLAT.sh` (Linux/macOS) scripts.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python 3.10+, FastAPI, SQLModel, SQLite, Cryptography (Fernet)
- **Frontend:** Streamlit, HTTPX
- **AI Integrations:** Google GenAI SDK (`google-genai`), OpenRouter Async API

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher installed on your machine.

### Installation & Execution

1. **Clone or Download the Repository:**
   ```bash
   git clone https://github.com/yourusername/PromptQW.git
   cd PromptQW

    Run with One-Click Launchers:

        Windows: Double-click BAŞLAT.bat

        Linux / macOS: Run bash BAŞLAT.sh in your terminal

    (Or run manually via Python)
    code Bash

    pip install -r requirements.txt
    python run.py

    Access the App: Open your browser at http://localhost:8501

⚙️ How to Use

    Open the "⚙️ System Settings" panel on the left sidebar.

    Select your preferred provider (Gemini or OpenRouter) and model.

    Enter your API Key and click Save Settings (Keys are stored encrypted locally).

    Enter your prompt idea, pick a domain, answer the AI's refining questions, and get your optimized prompt!

🇹🇷 Türkçe Dokümantasyon
Hızlı Başlangıç

    Bilgisayarınızda Python 3.10+ yüklü olduğundan emin olun.

    Windows kullanıyorsanız BAŞLAT.bat dosyasına çift tıklayın (Linux/Mac için BAŞLAT.sh).

    Tarayıcıda açılan http://localhost:8501 adresinden sol paneldeki Ayarlar kısmına API anahtarınızı girip kaydedin.

    Fikrinizi yazarak olgunlaştırma sihirbazını başlatın!

📄 License

Distributed under the MIT License. See LICENSE for more information.
code Code

---

### ✨ Görseldeki Stilin Karşılıkları:
1. **Rozetler (Badges):** Python versiyonu, FastAPI, Streamlit, Sürüm (v1.0.0) ve MIT Lisansı renkli rozetlerle en üste eklendi.
2. **Türkçe Yönlendirme:** Görseldeki bayraklı ve italik çizgi içi yapının birebir aynısı eklendi.
3. **Kapak Açıklaması:** Kalın metinle (bold) başlayan, projenin ne işe yaradığını anlatan İngilizce özet yazıldı.
4. **Çift Dilli Destek:** Sayfanın alt kısmına Türkçe dokümantasyon bölümü eklendi, böylece iki taraf da hedeflenmiş oldu.