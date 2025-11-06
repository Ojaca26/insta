import streamlit as st
import instaloader
import os
import re

st.set_page_config(page_title="Descargar Video de Instagram", page_icon="📲", layout="centered")

st.title("📲 Descargar Video de Instagram")
st.write("Pega aquí el enlace de un video **público** de Instagram (post o reel) y descárgalo directamente.")

# Input del usuario
url = st.text_input("🔗 Enlace del video de Instagram:")

# Carpeta donde se guardarán los videos
output_folder = "video_descargado"

if st.button("📥 Descargar Video"):
    if not url:
        st.warning("Por favor ingresa un enlace de Instagram.")
    else:
        try:
            # Crear instancia de Instaloader
            L = instaloader.Instaloader(dirname_pattern=output_folder, save_metadata=False, download_comments=False)

            # Aceptar tanto /p/ como /reel/ o /tv/
            match = re.search(r"/(p|reel|tv)/([A-Za-z0-9_-]+)", url)
            if not match:
                st.error("❌ Enlace no válido. Debe ser un enlace de publicación o reel (ejemplo: https://www.instagram.com/reel/XXXX/)")
            else:
                shortcode = match.group(2)

                # Descargar el post
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target=output_folder)

                # Buscar el archivo .mp4 descargado
                video_path = None
                for file in os.listdir(output_folder):
                    if file.endswith(".mp4"):
                        video_path = os.path.join(output_folder, file)
                        break

                if video_path:
                    st.success("✅ Video descargado correctamente.")
                    st.video(video_path)
                    with open(video_path, "rb") as file:
                        st.download_button(
                            label="💾 Descargar archivo MP4",
                            data=file,
                            file_name="mi_estado.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("⚠️ No se encontró el video. Verifica que la publicación contenga un video público.")

        except Exception as e:
            st.error(f"❌ Error al descargar: {e}")
