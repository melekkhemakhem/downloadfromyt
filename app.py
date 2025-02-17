import streamlit as st
import yt_dlp
import os
import platform

# Vérification et installation des dépendances manquantes
try:
    import yt_dlp
except ImportError:
    os.system('pip install yt-dlp')

# Vérification de l'installation de ffmpeg
try:
    import ffmpeg
except ImportError:
    os.system('pip install ffmpeg')

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

# Fonction pour convertir l'audio téléchargé en MP3 et sauvegarder dans le dossier de téléchargement
def convert_to_mp3(file_name):
    # Détecter le système d'exploitation et définir le chemin du dossier de téléchargement par défaut
    if platform.system() == "Windows":
        downloads_folder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    elif platform.system() == "Darwin":  # macOS
        downloads_folder = os.path.join(os.environ['HOME'], 'Downloads')
    else:  # Linux
        downloads_folder = os.path.join(os.environ['HOME'], 'Téléchargements')

    # Créer le chemin du fichier de sortie
    output_file = os.path.join(downloads_folder, f"{os.path.splitext(os.path.basename(file_name))[0]}.mp3")
    
    # Exécuter la conversion en MP3
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
            st.success(f"✅ Téléchargement et conversion terminés ! Le fichier MP3 a été sauvegardé dans le dossier de téléchargements.")
            # Affichage du bouton de téléchargement
            st.download_button("⬇️ Télécharger le MP3", mp3_file, file_name=mp3_file.split('/')[-1])
    else:
        st.warning("⚠️ Veuillez entrer une URL valide.")
