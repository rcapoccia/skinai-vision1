import streamlit as st
from PIL import Image
import openai

st.set_page_config(page_title="SkinAI Vision", layout="centered")

st.title("💡 SkinAI Vision")
st.write("Carica una tua foto per scoprire il tuo tipo di pelle, ricevere consigli skincare personalizzati e altro ancora.")

uploaded_file = st.file_uploader("📷 Carica un'immagine del tuo viso", type=["jpg", "jpeg", "png"])

questionario = st.text_area("📝 (Opzionale) Rispondi al questionario se vuoi migliorare la consulenza", placeholder="Scrivi qui se vuoi inserire risposte...")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Immagine caricata", use_column_width=True)

    with st.spinner("Analisi in corso con GPT-4 Vision..."):

        openai.api_key = st.secrets["OPENAI_API_KEY"]

        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "Sei una consulente skincare professionale ed empatica."},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analizza il viso nella foto. Fornisci:\n\n1. Un riepilogo professionale e chiaro, in italiano\n2. Una routine skincare personalizzata (mattina e sera) per clima mediterraneo, pelle sensibile, con prodotti consigliati e link\n3. Consigli su make up e armocromia\n4. Eventuali consigli su alimentazione, sonno o idratazione.\n\nQuestionario (facoltativo):\n{questionario}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{uploaded_file.getvalue().decode('latin1')}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=1800,
        )

        st.success("✅ Analisi completata!")
        st.markdown(response.choices[0].message.content)

---

