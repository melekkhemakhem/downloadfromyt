import streamlit as st
import yt_dlp
import os

st.title("🎵 Téléchargeur YouTube en MP3")

# Zone d'entrée pour l'URL
url = st.text_input("Entrez l'URL de la vidéo YouTube")

# Fonction pour télécharger l'audio YouTube
def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'postprocessors': [],
    }
    try:
        os.makedirs("downloads", exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info_dict)
            return file_name
    except Exception as e:
        st.error(f"Erreur lors du téléchargement : {e}")
        return None

# Fonction pour convertir l'audio téléchargé en MP3
def convert_to_mp3(file_name):
    output_file = f"downloads/{os.path.splitext(os.path.basename(file_name))[0]}.mp3"
    os.system(f'ffmpeg -i "{file_name}" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "{output_file}"')
    return output_file

# Bouton de téléchargement et de conversion
if st.button("Télécharger et convertir en MP3"):
    if url:
        st.info("📥 Téléchargement en cours...")
        file_name = download_youtube_audio(url)
        if file_name:
            st.info("🎶 Conversion en MP3 en cours...")
            mp3_file = convert_to_mp3(file_name)
            st.success("✅ Téléchargement et conversion terminés !")
            st.download_button("⬇️ Télécharger le MP3", mp3_file, file_name=mp3_file.split('/')[-1])
    else:
        st.warning("⚠️ Veuillez entrer une URL valide.")
