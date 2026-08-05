import streamlit as st
import httpx

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

    gemini_key = st.sidebar.text_input("Gemini API Key", type="password")
    openrouter_key = st.sidebar.text_input("OpenRouter API Key", type="password")

    provider = st.sidebar.selectbox("Aktif Sağlayıcı", ["gemini","openrouter"])
    model_options = AVAILABLE_MODELS.get(provider, [])
    model = st.sidebar.selectbox("Tercih Edilen Model", options=model_options)

    if st.sidebar.button("Ayarları Kaydet"):
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
        col1, col2, col3 = st.columns(3)
        with col1:
            domain = st.selectbox("Alan", ["Software Development", "Data Science", "Content Creation", "Academic", "Business"])
        with col2:
            knowledge_level = st.select_slider("Bilgi Seviyeniz", options=["Beginner", "Intermediate", "Advanced"], value="Intermediate")
        with col3:
            wants_turkish = st.checkbox("Türkçe Açıklama İçersin", value=True)
            
        if st.button("🚀 Soruları Üret ve Başlat"):
            if not raw_idea.strip():
                st.warning("Lütfen bir fikir girin!")
            else:
                payload = {
                    "user_input": raw_idea,
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
