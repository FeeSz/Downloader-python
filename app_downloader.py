import PySimpleGUI as sg
import yt_dlp
import os
from pathlib import Path

# Configuração do tema
sg.theme('Reddit')

# Credenciais válidas (você pode expandir isso)
USUARIOS_VALIDOS = {
    'admin': 'admin',
    'user': '123456'
}

# ==================== FUNÇÕES DE DOWNLOAD ====================
def baixar_audio_ou_video(url, formato="mp4", pasta_destino=None):
    """
    Baixa áudio ou vídeo do YouTube
    Retorna: (sucesso: bool, mensagem: str)
    """
    try:
        if not url.strip():
            return False, "❌ Insira uma URL válida!"
        
        # Usar pasta de Downloads do usuário se não especificada
        if pasta_destino is None:
            pasta_destino = str(Path.home() / "Downloads" / "YouTube_Downloader")
        
        # Criar pasta se não existir
        os.makedirs(pasta_destino, exist_ok=True)
        
        # Configurações para download
        opcoes = {
            'format': 'bestaudio' if formato == 'mp3' else 'best',
            'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        if formato == 'mp3':
            opcoes['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        # Download
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'Desconhecido')
        
        mensagem = f"✅ Download de {formato.upper()} concluído!\nArquivo: {titulo}\nPasta: {pasta_destino}"
        return True, mensagem
        
    except Exception as e:
        erro = str(e)
        if 'ffmpeg' in erro.lower():
            mensagem = f"❌ Erro: FFmpeg não encontrado.\nInstale com: pip install ffmpeg-python\nDetalhes: {erro}"
        elif 'url' in erro.lower() or 'video' in erro.lower():
            mensagem = f"❌ URL inválida ou vídeo não disponível.\nDetalhes: {erro}"
        else:
            mensagem = f"❌ Erro no download: {erro}"
        return False, mensagem


# ==================== TELA DE LOGIN ====================
def tela_login():
    """Janela de login"""
    layout_login = [
        [sg.Text('🎵 YouTube Downloader Pro', font=('Arial', 18, 'bold'), text_color='#E74C3C')],
        [sg.Text('')],
        [sg.Text('Usuário:', size=(12, 1)), sg.Input(key='usuario', size=(25, 1))],
        [sg.Text('Senha:', size=(12, 1)), sg.Input(key='senha', password_char='*', size=(25, 1))],
        [sg.Checkbox('Lembrar credenciais', key='lembrar')],
        [sg.Text('')],
        [sg.Button('Entrar', size=(10, 1)), sg.Button('Sair', size=(10, 1))],
    ]
    
    janela = sg.Window('Login - YouTube Downloader', layout_login, finalize=True)
    
    while True:
        eventos, valores = janela.read()
        
        if eventos == sg.WINDOW_CLOSED or eventos == 'Sair':
            janela.close()
            return None
        
        if eventos == 'Entrar':
            usuario = valores['usuario'].strip()
            senha = valores['senha'].strip()
            
            # Validar credenciais
            if usuario in USUARIOS_VALIDOS and USUARIOS_VALIDOS[usuario] == senha:
                janela.close()
                return usuario
            else:
                sg.popup_error('❌ Usuário ou senha incorretos!', title='Erro de Login')


# ==================== TELA PRINCIPAL (DOWNLOAD) ====================
def tela_download(usuario):
    """Janela principal de download"""
    layout_download = [
        [sg.Text(f'👋 Bem-vindo, {usuario}!', font=('Arial', 14, 'bold'))],
        [sg.Text('')],
        [sg.Text('Cole a URL do vídeo do YouTube:', font=('Arial', 10, 'bold'))],
        [sg.Input(key='url', size=(50, 1), focus=True)],
        [sg.Text('')],
        [sg.Text('Selecione o formato:', font=('Arial', 10, 'bold'))],
        [
            sg.Radio('🎬 MP4 (Vídeo)', 'formato', default=True, key='mp4'),
            sg.Radio('🎵 MP3 (Áudio)', 'formato', key='mp3')
        ],
        [sg.Text('')],
        [sg.Text('Pasta de destino (opcional):', font=('Arial', 10, 'bold'))],
        [
            sg.Input(key='pasta', size=(35, 1)),
            sg.FolderBrowse('Procurar', size=(10, 1))
        ],
        [sg.Text('')],
        [sg.Multiline(size=(50, 8), key='output', disabled=True, background_color='#2C3E50', text_color='#ECF0F1')],
        [sg.Text('')],
        [
            sg.Button('📥 Baixar', size=(12, 1)),
            sg.Button('🗑️ Limpar', size=(12, 1)),
            sg.Button('🚪 Sair', size=(12, 1))
        ],
    ]
    
    janela = sg.Window('YouTube Downloader - Download', layout_download, finalize=True, size=(600, 600))
    
    while True:
        eventos, valores = janela.read()
        
        if eventos == sg.WINDOW_CLOSED or eventos == '🚪 Sair':
            break
        
        if eventos == '🗑️ Limpar':
            janela['url'].update('')
            janela['output'].update('')
            janela['pasta'].update('')
        
        if eventos == '📥 Baixar':
            url = valores['url'].strip()
            formato = 'mp3' if valores['mp3'] else 'mp4'
            pasta = valores['pasta'].strip() if valores['pasta'].strip() else None
            
            # Atualizar output com status
            janela['output'].update('⏳ Processando download...\n', append=False)
            janela.refresh()
            
            # Executar download
            sucesso, mensagem = baixar_audio_ou_video(url, formato, pasta)
            
            # Exibir resultado
            if sucesso:
                janela['output'].update(mensagem + '\n', append=False)
            else:
                janela['output'].update(mensagem + '\n', append=False)
    
    janela.close()


# ==================== FUNÇÃO PRINCIPAL ====================
def main():
    """Função principal da aplicação"""
    usuario = tela_login()
    
    if usuario:
        tela_download(usuario)
    
    sg.popup('👋 Obrigado por usar o YouTube Downloader!', title='Saída')


if __name__ == '__main__':
    main()
