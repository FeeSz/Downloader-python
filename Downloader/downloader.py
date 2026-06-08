import yt_dlp

def baixar_audio_ou_video(url, formato="mp4"):
    # Configurações para baixar MP3 ou MP4
    opcoes = {
        'format': 'bestaudio' if formato == 'mp3' else 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    if formato == 'mp3':
        opcoes['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        print("Download concluído com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        print("Dica: Se o erro for relacionado a ffmpeg, instale-o com: pip install ffmpeg-python")

# Exemplo de uso
url_video = input("Insira o link: ")
baixar_audio_ou_video(url_video, "mp3")  # Para baixar MP3
baixar_audio_ou_video(url_video, "mp4")    # Para baixar MP4
