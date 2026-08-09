import subprocess
import sys
import time
import webbrowser

def main():
    print("🚀 PromptQW Servisleri Başlatılıyor...")

    # 1. FastAPI (Backend) Sürecini Başlat
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000"
    ])

    # 2. Streamlit (Frontend) Sürecini Başlat
    frontend_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "app.py", 
        "--server.port", "8501",
        "--server.headless", "true"
    ])

    # Servislerin hazır olması için 3 saniye bekle
    print("⏳ Servislerin ayağa kalkması bekleniyor...")
    time.sleep(3)

    # 3. Varsayılan Tarayıcıda Aç
    print("🌐 Tarayıcı açılıyor: http://localhost:8501")
    webbrowser.open("http://localhost:8501")

    print("\n---------------------------------------------------")
    print("✅ Uygulama çalışıyor! Kapatmak için CTRL+C yapabilirsiniz.")
    print("---------------------------------------------------\n")

    try:
        # Süreçleri canlı tut
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        # Terminalde CTRL+C yapıldığında her iki servisi de temizce kapat
        print("\n🛑 Uygulama kapatılıyor. Arka plan servisleri sonlandırılıyor...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Tüm servisler temiz bir şekilde kapatıldı!")

if __name__ == "__main__":
    main()