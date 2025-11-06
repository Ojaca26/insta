import streamlit as st
import instaloader
import yt_dlp
import os
import re
import shutil

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Descargar Videos (Instagram / TikTok / YouTube)", page_icon="📲", layout="centered")

st.title("📲 Descargador Universal de Videos")
st.write("Selecciona la plataforma, pega el enlace y descarga tu video en formato MP4 (solo contenido público).")

# --- SIDEBAR ---
st.sidebar.header("💡 Guía rápida")
st.sidebar.markdown("""
1. Selecciona la **plataforma**: Instagram, TikTok o YouTube.  
2. Copia y pega el **enlace público** del video.  
3. Presiona **“📥 Descargar Video”**.  
4. Espera unos segundos y podrás **ver y descargar el video en MP4**.

⚠️ Solo funciona con contenido **público**.
""")

st.sidebar.divider()

# Selector de plataforma
plataforma = st.sidebar.selectbox("🌐 Plataforma:", ["Instagram", "TikTok", "YouTube"])

# Limpieza de archivos
st.sidebar.subheader("🧹 Limpieza de archivos")
if st.sidebar.button("Eliminar videos descargados"):
    if os.path.exists("video_descargado"):
        shutil.rmtree("video_descargado")
        st.sidebar.success("✅ Carpeta 'video_descargado' eliminada correctamente.")
    else:
        st.sidebar.info("No hay archivos para eliminar.")

st.sidebar.divider()
st.sidebar.markdown("""
**📘 Aviso Legal**  
Esta herramienta es solo para uso personal y educativo.  
Respeta los derechos de autor y privacidad de los creadores.
""")

# --- LÓGICA PRINCIPAL ---
url = st.text_input("🔗 Pega el enlace del video:")
output_folder = "video_descargado"

if st.button("📥 Descargar Video"):
    if not url:
        st.warning("Por favor ingresa un enlace válido.")
    else:
        os.makedirs(output_folder, exist_ok=True)
        video_path = None

        # ---------------- INSTAGRAM ----------------
        if plataforma == "Instagram":
            st.info("⬇️ Descargando video desde Instagram...")
            try:
                L = instaloader.Instaloader(dirname_pattern=output_folder, save_metadata=False, download_comments=False)

                # Acepta /p/, /reel/ y /tv/
                match = re.search(r"/(p|reel|tv)/([A-Za-z0-9_-]+)", url)
                if not match:
                    st.error("❌ Enlace no válido. Debe ser un enlace de publicación o reel (ejemplo: https://www.instagram.com/reel/XXXX/)")
                else:
                    shortcode = match.group(2)
                    post = instaloader.Post.from_shortcode(L.context, shortcode)
                    L.download_post(post, target=output_folder)

                    for file in os.listdir(output_folder):
                        if file.endswith(".mp4"):
                            video_path = os.path.join(output_folder, file)
                            break

            except Exception as e:
                st.error(f"❌ Error en descarga de Instagram: {e}")

        # ---------------- TIKTOK ----------------
        elif plataforma == "TikTok":
            st.info("⬇️ Descargando video desde TikTok...")
            try:
                options = {
                    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'merge_output_format': 'mp4',
                    'format': 'mp4',
                    'noplaylist': True,
                    'nocheckcertificate': True,
                    'geo_bypass': True,
                    'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
                }
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_path = ydl.prepare_filename(info)

            except Exception as e:
                st.error(f"❌ Error en descarga de TikTok: {e}")

        # ---------------- YOUTUBE ----------------
        elif plataforma == "YouTube":
            st.info("⬇️ Descargando video desde YouTube...")
            try:
                options = {
                    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'merge_output_format': 'mp4',
                    'format': 'best[ext=mp4]/best',
                    'noplaylist': True,
                }
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_path = ydl.prepare_filename(info)

            except Exception as e:
                st.error(f"❌ Error en descarga de YouTube: {e}")

        # ---------------- MOSTRAR RESULTADO ----------------
        if video_path and os.path.exists(video_path):
            st.success("✅ Video descargado correctamente.")
            st.video(video_path)
            with open(video_path, "rb") as file:
                st.download_button(
                    label="💾 Descargar archivo MP4",
                    data=file,
                    file_name=os.path.basename(video_path),
                    mime="video/mp4"
                )
        else:
            st.warning("⚠️ No se pudo encontrar o procesar el video.")
