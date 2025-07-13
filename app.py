
import streamlit as st
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Twibbon Maker - KSR UNIGA", layout="centered")
st.title("🎨 Twibbon Maker - KSR UNIGA")
st.markdown("Upload twibbon transparan dan fotomu, sesuaikan posisi, lalu download hasilnya.")

# Upload twibbon
twibbon_file = st.file_uploader("📤 Upload Twibbon PNG (dengan bagian tengah transparan)", type=["png"])
foto_file = st.file_uploader("📷 Upload Foto Kamu", type=["jpg", "jpeg", "png"])

if twibbon_file and foto_file:
    twibbon = Image.open(twibbon_file).convert("RGBA")
    foto = Image.open(foto_file).convert("RGBA")
    tw_w, tw_h = twibbon.size

    # Resize foto agar seukuran twibbon dulu
    foto = foto.resize((tw_w, tw_h))

    st.markdown("### ✏️ Atur Posisi dan Ukuran Foto")

    # Slider untuk skala dan posisi
    scale = st.slider("🔍 Perbesar/Kecilkan", 0.5, 2.0, 1.0, 0.01)
    offset_x = st.slider("↔️ Geser Kanan-Kiri", -tw_w//2, tw_w//2, 0, 1)
    offset_y = st.slider("↕️ Geser Atas-Bawah", -tw_h//2, tw_h//2, 0, 1)

    # Buat kanvas kosong
    background = Image.new("RGBA", (tw_w, tw_h), (255, 255, 255, 0))

    # Resize dan paste foto ke background
    scaled_size = (int(tw_w * scale), int(tw_h * scale))
    foto_scaled = foto.resize(scaled_size)
    bg_x = offset_x
    bg_y = offset_y
    background.paste(foto_scaled, (bg_x, bg_y))

    # Tempelkan twibbon di atasnya
    result = Image.alpha_composite(background, twibbon)

    st.markdown("### ✅ Hasil Akhir")
    st.image(result, use_column_width=True)

    # Convert to downloadable bytes
    result_bytes = io.BytesIO()
    result.save(result_bytes, format="PNG")
    result_bytes.seek(0)

    st.download_button("💾 Download Hasil PNG", data=result_bytes, file_name="twibbon_terpasang.png", mime="image/png")
else:
    st.info("Silakan upload twibbon dan foto terlebih dahulu.")
