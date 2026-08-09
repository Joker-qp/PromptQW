import streamlit as st
import httpx

def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max (1, int(len(text) / 3.7))

# Katmanlı ve Zenginleştirilmiş Domaine Özel Alt Seçenekler
DOMAIN_EXTRA_OPTIONS = {
    "Genel": {
        "basic": {
            "Amaç": ["Bilgilendirme / Öğretme", "Problem Çözme", "Fikir Üretme / Beyin Fırtınası", "Eğlence / İçerik"],
            "Çıktı Formatı": ["Ayrıntılı Metin & Rapor", "Özet & Liste (Bullet Points)", "Soru-Cevap Biçimi", "Adım Adım Rehber"]
        },
        "advanced": {
            "Yaratıcılık Seviyesi": ["Standart & Mantıksal", "Yüksek Yaratıcılık & Serbest", "Katı & Sadece Gerçekler"],
            "Dil / Üslup": ["Yalın & Kolay Anlaşılır", "Teknik & Profesyonel", "Akademik & Ciddi"]
        }
    },
    "Software Development": {
        "basic": {
            "Programlama Dili": ["Python", "JavaScript / TypeScript", "Rust", "Go", "C++ / C#", "Java", "Diğer"],
            "Görev Türü": ["Sıfırdan Mimari Kurma", "Hata Düzeltme (Bugfix)", "Refactoring / Temiz Kod", "Unit / Integration Test"]
        },
        "advanced": {
            "Kod Seviyesi": ["Temel Seviye", "Clean Code & Design Patterns", "High Performance / Enterprise"],
            "Mimari Yaklaşım": ["Async / Concurrent Processing", "Microservices & Docker Uyumlu", "Modüler & Standart"]
        }
    },
    "Data Science": {
        "basic": {
            "Araç / Kütüphane": ["Pandas / NumPy / Polars", "PyTorch / TensorFlow", "Scikit-Learn", "SQL & ETL Pipeline", "LLM / RAG / LangChain"],
            "Proje Tipi": ["Keşifsel Veri Analizi (EDA)", "Makine Öğrenmesi Modeli", "Derin Öğrenme / Computer Vision", "NLP / Metin İşleme"]
        },
        "advanced": {
            "Hedef Çıktı": ["Jupyter Notebook Kodu", "Prodüksiyon Sınıfı Python Scripti", "Görselleştirme Raporu", "Model Metrikleri"],
            "Optimizasyon Metodu": ["Cross-Validation & GridSearch", "GPU / Cuda Hızlandırma", "Quantization & Model Sıkıştırma"]
        }
    },
    "Content Creation": {
        "basic": {
            "İçerik Formatı": ["YouTube Video Scripti", "Blog / SEO Makalesi", "LinkedIn Gönderisi", "X / Twitter Floodu", "E-Kitap Bölümü"],
            "İçerik Tonu": ["Profesyonel & Kurumsal", "Samimi & Hikaye Anlatıcı", "Eğlenceli & İkna Edici", "Ciddi & Bilgilendirici"]
        },
        "advanced": {
            "Hedef Kitle": ["Genel İzleyici / Müşteriler", "Yazılımcılar / Teknik Ekip", "Girişimciler / Yöneticiler", "Öğrenciler"],
            "Görsel / Medya Önerisi": ["Görsel Tasvirleri Dahil Et", "Metin İçi B-Roll Önerileri Ekle", "Sadece Düz Metin"]
        }
    },
    "Academic": {
        "basic": {
            "Çalışma Türü": ["Tez / Akademik Makale", "Araştırma Özeti (Abstract)", "Literatür Taraması (Literature Review)", "Hibe / Proje Başvurusu"],
            "Akademik Alan": ["Mühendislik & Fen Bilimleri", "Sosyal Bilimler & Psikoloji", "Tıp & Sağlık Bilimleri", "İktisat & İşletme"]
        },
        "advanced": {
            "Atıf Formatı": ["APA 7", "IEEE", "MLA", "Chicago / Harvard"],
            "Metodoloji Tipi": ["Nitel Araştırma (Qualitative)", "Nicel Araştırma (Quantitative)", "Karma Metot (Mixed Methods)"]
        }
    },
    "Business & Marketing": {
        "basic": {
            "İş/Pazarlama Hedefi": ["Pazarlama / Satış Metni (Copywriting)", "Pitch Deck / Yatırımcı Sunumu", "Cold Email Kampanyası", "İş Planı & Strateji"],
            "Hedef Kitle": ["B2B (Şirketler)", "B2C (Tüketiciler)", "Yatırımcılar / Melek Yatırımcılar", "Şirket İçi Ekip"]
        },
        "advanced": {
            "Çağrı Türü (CTA)": ["Doğrudan Satış / Satın Al", "Toplantı Randevusu Al", "Bültene Abone Ol", "Bilgilendirme / Farkındalık"],
            "Rakip Analizi Açısı": ["Fiyat Advantage Odaklı", "Kalite & İnovasyon Odaklı", "Problem-Çözüm Odaklı"]
        }
    },
    "Tarih & Sosyal Bilimler": {
        "basic": {
            "Disiplin": ["Tarih / Tarihsel Analiz", "Sosyoloji / Toplumsal İnceleme", "Felsefe & Düşünce Tarihi", "Psikoloji & Davranış", "Siyaset Bilimi"],
            "Tarihsel Dönem": ["Antik Çağ & İlk Çağ", "Orta Çağ", "Yeni Çağ & Osmanlı / Doğu Tarihi", "Yakın Çağ & Modern Dönem", "Çağdaş / Günümüz"]
        },
        "advanced": {
            "Analiz Metodu": ["Kronolojik İnceleme", "Karşılaştırmalı Analiz", "Biyografik / Kişilik Odaklı", "Düşünce / Fikir Akımı Analizi"],
            "Kaynak Yaklaşımı": ["Birincil Kaynak Odaklı", "Eleştirel & Revizyonist Yaklaşım", "Genel Tarihsel Özet"]
        }
    }
}
AVAILABLE_MODELS = {
    "gemini": [
        "gemini-3.6-flash",
        "gemma-4-31b-it",
        "gemma-4-26b-a4b-it",
        "gemini-2.5-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.1-pro-preview",
    ],
    "openrouter": [
        "openrouter/free",                     
        "moonshotai/kimi-k3",                  
        "deepseek/deepseek-r1",                 
        "deepseek/deepseek-v3",                
        "qwen/qwen-2.5-coder-32b-instruct",    
        "z-ai/glm-5.2",                       
        "anthropic/claude-3.5-sonnet",         
        "anthropic/claude-3-5-haiku",          
        "openai/gpt-4o",
        "openrouter/pareto-code"
    ]
}


API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="Interactive Prompt Archtect",
    page_icon="🤖",
    layout="wide"
)

def get_current_settings():
    try:
        response = httpx.get(f"{API_BASE_URL}/settings")
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None

def render_sidebar():
    st.sidebar.title("⚙️ Ayarlar")

    settings = get_current_settings() or {}

    current_provider = settings.get("active_provider", "gemini")
    current_model = settings.get("preferred_model", "gemini-2.5-flash")
    has_gemini = settings.get("has_gemini_key", False)
    has_openrouter = settings.get("has_openrouter_key", False)

    st.sidebar.markdown("### 📊 Aktif Durum")
    st.sidebar.info(f"**Sağlayıcı:** `{current_provider.upper()}`\n\n**Model:** `{current_model}`")

    col_k1, col_k2 = st.sidebar.columns(2)
    with col_k1:
        st.caption(f"Gemini Key: {'🟢 Kayıtlı' if has_gemini else '🔴 Eksik'}")
    with col_k2:
        st.caption(f"OpenRouter: {'🟢 Kayıtlı' if has_openrouter else '🔴 Eksik'}")

    st.sidebar.divider()
    st.sidebar.markdown("### 🔧 Ayarları Güncelle")

    gemini_key = st.sidebar.text_input(
        "Gemini API Key", 
        type="password", 
        placeholder="Kayıtlı (Değiştirmek için yazın)" if has_gemini else "API Key girin..."
    )
    openrouter_key = st.sidebar.text_input(
        "OpenRouter API Key", 
        type="password", 
        placeholder="Kayıtlı (Değiştirmek için yazın)" if has_openrouter else "API Key girin..."
    )

    provider_options = ["gemini", "openrouter"]
    provider_index = provider_options.index(current_provider) if current_provider in provider_options else 0
    provider = st.sidebar.selectbox("Aktif Sağlayıcı", provider_options, index=provider_index)

    model_options = AVAILABLE_MODELS.get(provider, [])
    model_index = model_options.index(current_model) if current_model in model_options else 0
    model = st.sidebar.selectbox("Tercih Edilen Model", options=model_options, index=model_index)

    if st.sidebar.button("Ayarları Kaydet", use_container_width=True):
        payload = {
            "active_provider": provider,
            "preferred_model": model
        }
        if gemini_key.strip():
            payload["gemini_api_key"] = gemini_key.strip()
        if openrouter_key.strip():
            payload["openrouter_api_key"] = openrouter_key.strip()

        try:
            res = httpx.post(f"{API_BASE_URL}/settings", json=payload, timeout=30)
            if res.status_code == 200:
                st.sidebar.success("Ayarlar Kaydedildi!")
                st.rerun()
        except Exception as e:
            st.sidebar.error(f"Bağlantı hatası: {e}")


st.title("🤖 Interactive Prompt Architect")
st.caption("Local-First Dinamik Prompt Mühendisliği ve Olgunlaştırma Sistemi")
render_sidebar()

tab1, tab2 = st.tabs(["🚀 Prompt Mimarı Sihirbazı", "📜 Geçmiş Prompt'lar"])

with tab1:
    if "current_prompt" not in st.session_state:
        st.subheader("1. Fikrini Gir ve Başlat")

        raw_idea = st.text_area("Proje veya Prompt Fikriniz", placeholder="Örn: " \
        "Python ile e-ticaret stok takip otomasyonu yazmak istiyorum...")

        input_tokens = estimate_tokens(raw_idea)
        st.caption(f"📊 Tahmini Giriş Token Sayısı: ~{input_tokens} token")

        col1, col2, col3 = st.columns(3)
        with col1:
            domain = st.selectbox("Alan", ["Software Development", "Data Science", "Content Creation", "Academic", "Business & Marketing", "Tarih & Sosyal Bilimler", "Genel"])
        with col2:
            knowledge_level = st.select_slider("Bilgi Seviyeniz", options=["Beginner", "Intermediate", "Advanced"], value="Intermediate")
        with col3:
            wants_turkish = st.checkbox("Türkçe Açıklama İçersin", value=True)

        use_domain_details = st.checkbox("🔍 Alan Detaylarını Göster ve Kullan", value=False)
        extra_selected = {}

        if use_domain_details and domain in DOMAIN_EXTRA_OPTIONS:
            # 1. Temel Alt Seçenekler
            st.markdown("##### 🎯 Temel Alt Seçenekler")
            basic_opts = DOMAIN_EXTRA_OPTIONS[domain].get("basic", {})
            b_cols = st.columns(len(basic_opts))
            for idx, (sub_key, options) in enumerate(basic_opts.items()):
                with b_cols[idx]:
                    selected_val = st.selectbox(sub_key, options, key=f"basic_{sub_key}")
                    extra_selected[sub_key] = selected_val

            # 2. Gelişmiş Alt Seçenekler (İkinci Checkbox)
            use_advanced_details = st.checkbox("➕ Daha Fazla Seçenek / Gelişmiş Ayarlar Göster", value=False)
            if use_advanced_details:
                st.markdown("##### ⚙️ Gelişmiş Alt Seçenekler")
                adv_opts = DOMAIN_EXTRA_OPTIONS[domain].get("advanced", {})
                a_cols = st.columns(len(adv_opts))
                for idx, (sub_key, options) in enumerate(adv_opts.items()):
                    with a_cols[idx]:
                        selected_val = st.selectbox(sub_key, options, key=f"adv_{sub_key}")
                        extra_selected[sub_key] = selected_val

        if st.button("🚀 Soruları Üret ve Başlat", type="primary"):
            if not raw_idea.strip():
                st.warning("Lütfen bir fikir girin!")
            else:
                # Eğer detaylar tiklendiyse ekle, tiklenmediyse sadece yalın fikri gönder
                if use_domain_details and extra_selected:
                    full_idea_context = f"{raw_idea}\n\n[Ek Detaylar: {extra_selected}]"
                else:
                    full_idea_context = raw_idea

                payload = {
                    "user_input": full_idea_context,
                    "domain": domain,
                    "knowledge_level": knowledge_level,
                    "wants_turkish_response": wants_turkish
                }
                res = httpx.post(f"{API_BASE_URL}/prompts", json=payload, timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.current_prompt = data["prompt"]
                    st.session_state.questions = data["questions"]
                    st.rerun()

    elif "final_outputs" not in st.session_state:
        st.subheader("2. AI Fikrinizi Olgunlaştırmak İçin Bu Soruları Sordu")
        questions = st.session_state.questions
        user_answers = {}

        with st.form("answers_form"):
            for q in questions:
                answer = st.text_area(f"❓ {q['question']}", key=f"q_{q['id']}")
                user_answers[q["id"]] = answer

            submit_btn = st.form_submit_button("✨ Nihai Prompt'u Oluştur")
            if submit_btn:
                prompt_id = st.session_state.current_prompt["id"]
                payload = {"answers": user_answers}
                
                res = httpx.post(f"{API_BASE_URL}/prompts/{prompt_id}/answers", json=payload, timeout=120)
                if res.status_code == 200:
                    st.session_state.final_outputs = res.json()
                    st.rerun()
                else:
                    st.error("Cevaplar gönderilirken bir hata oluştu.")

    else:
        st.success("🎉 Promptunuz Başarıyla Oluşturuldu!")
        outputs = st.session_state.final_outputs
        
        st.subheader("🇬🇧 Gelişmiş İngilizce Prompt")
        st.code(outputs.get("english_prompt", ""), language="markdown")
        
        st.subheader("🇹🇷 Türkçe Çevirisi")
        st.code(outputs.get("turkish_translation", ""), language="markdown")
        
        st.subheader("📚 Türkçe Öğrenme ve Kullanım Rehberi")
        st.markdown(outputs.get("turkish_explanation", ""))
        
        st.divider()
        if st.button("🔄 Yeni Bir Prompt Süreci Başlat"):
            st.session_state.pop("current_prompt", None)
            st.session_state.pop("questions", None)
            st.session_state.pop("final_outputs", None)
            st.rerun()

    
with tab2:
    st.subheader("Geçmiş Prompt Geçmişi")
    try:
        res = httpx.get(f"{API_BASE_URL}/prompts", timeout=10.0)
        if res.status_code == 200:
            prompts = res.json()
            if not prompts:
                st.info("Henüz kaydedilmiş bir prompt bulunmuyor.")
            else:
                for p in prompts:
                    with st.expander(f"📌 {p['user_input'][:60]}... | Status: {p['status']}"):
                        st.write(f"**Domain:** {p['domain']} | **Level:** {p['knowledge_level']}")
                        if p["english_prompt"]:
                            st.subheader("🇬🇧 English Prompt")
                            st.code(p["english_prompt"], language="markdown")
                        if p["turkish_translation"]:
                            st.subheader("🇹🇷 Türkçe Çevirisi")
                            st.code(p["turkish_translation"], language="markdown")
    except Exception as e:
        st.error(f"Geçmiş yüklenirken hata oluştu: {e}")
