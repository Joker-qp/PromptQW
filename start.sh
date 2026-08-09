#!/bin/bash
echo "========================================="
echo " PromptQW Uygulaması Başlatılıyor..."
echo "========================================="

# Kütüphaneleri yükle
pip install -r requirements.txt || pip3 install -r requirements.txt

# Uygulamayı çalıştır
python run.py || python3 run.py