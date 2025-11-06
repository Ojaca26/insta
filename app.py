import streamlit as st
import instaloader
import os
import re
import shutil

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Descargar Video de Instagram", page_icon="📲", layout="centered")

st.title("📲 Descargar Video de Instagram")
st.write("Pega aquí el enlace de un video **público** de Instagram (post o reel) y descárgalo directamente.")

# --- SIDEBAR ---
st.sidebar.header("💡 Guía rápida")
st.sidebar.markdown("""
1. Copia el enlace del **post o reel público** desde Instagram.  
2. Pégalo en el cuadro principal.  
3. Presiona **“📥 Descargar Video”**.  
4. Espera unos segundos y podrás **ver y descargar el video .mp4**.

⚠️ Solo funciona con publicaciones **públicas**.
""")

st.sidebar.divider()

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
Respeta los derechos de autor del contenido descargado.  
""")

# --- LÓGICA PRINCIPAL ---
url = st.text_input("🔗 Enlace del video de Instagram:")
output_folder = "video_descargado"

if st.button("📥 Descargar Video"):
    if not url:
        st.warning("Por favor ingresa un enlace de Instagram.")
    else:
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
