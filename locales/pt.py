"""Strings de interface em português."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Baixe vídeos, áudio e transcrições do YouTube.",
    "help_url": "URL do vídeo do YouTube",
    "help_quality": "Qualidade: max / medium / low / audio",
    "help_lang": "Idioma do áudio/transcrição (padrão: {default})",
    "help_mp3": "Salvar também uma faixa mp3",
    "help_output": "Pasta de saída (padrão: downloads)",
    "help_ui_lang": "Idioma da interface: en/ru/uk/pt/de/fr (padrão: detecção automática)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Escolha a qualidade:",
    "q_max": "  1 — máxima (1080p+ via DASH)",
    "q_medium": "  2 — média",
    "q_low": "  3 — baixa",
    "q_audio": "  4 — somente áudio (mp3)",
    "prompt_quality": "Número (1/2/3/4) [1]: ",
    "prompt_url": "🔗 URL do YouTube: ",
    "prompt_lang": "Idioma do áudio/transcrição [{default}]: ",
    "prompt_mp3": "Salvar também uma faixa mp3? (y/N): ",

    # ---------- CLI: extended help ----------
    "extended_help": """YouTube Downloader — ajuda estendida

MODOS DE QUALIDADE:
  max     — melhor disponível (1080p, 1440p, 4K via DASH)
  medium  — média
  low     — mais baixa (144p–360p)
  audio   — somente áudio em mp3 (ótimo para ouvir em qualquer lugar)

OPÇÕES EXTRAS:
  --mp3            salva também uma faixa mp3 junto ao mp4
  --lang ru|en|…   idioma do áudio e da transcrição (padrão: ru)
  --ui-lang LL     idioma da interface: en/ru/uk/pt/de/fr (padrão: automático)
  -o DIR           pasta de saída (padrão: downloads)

EXEMPLOS:
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

SEM ARGUMENTOS, a ferramenta entra no modo interativo e pergunta passo a passo.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  O registro já contém {count} entradas.",
    "err_get_video": "❌ Erro ao obter o vídeo: {error}",
    "warn_already_downloaded": "⚠️  Já baixado anteriormente. Ignorando.",
    "already_id": "   ID: {id}",
    "already_title": "   Título: {title}",
    "video_title": "🎬 Título: {title}",
    "video_author": "👤 Autor: {author}",
    "video_duration": "⏱  Duração: {duration}",
    "video_id": "🆔 ID: {id}",

    # ---------- Streams ----------
    "err_no_video_stream": "❌ Nenhum fluxo de vídeo adequado encontrado",
    "err_no_audio_stream": "❌ Não foi possível selecionar uma faixa de áudio",
    "audio_tracks_available": "🎧 Faixas de áudio disponíveis:",
    "audio_track_line": "   • {track} | {abr} | itag={itag} | ext={ext}{default}",
    "audio_selected": "✅ Faixa de áudio selecionada: {track} ({abr})",
    "audio_using_default": "ℹ️  Nenhuma faixa no idioma solicitado, usando a padrão ({abr})",
    "audio_using_best": "ℹ️  Usando a faixa de maior qualidade ({abr})",
    "audio_header": "🎧 Áudio: {name} ({abr})",
    "video_stream_info": "🎞  Vídeo: {res} ({mode})",
    "merge_label": "🔧 Mesclagem: {value}",
    "word_yes": "sim",
    "word_no": "não",
    "audio_lang_embedded": "embutido",

    # ---------- ffmpeg ----------
    "warn_no_ffmpeg_dash": "⚠️  ffmpeg não encontrado — DASH (1080p+) indisponível.",
    "warn_fallback_progressive": "   Recorrendo ao progressive (máx. 720p).",
    "err_no_progressive": "❌ Fluxo progressive indisponível. Instale o ffmpeg.",
    "dl_video_stream": "⬇️  Baixando fluxo de vídeo...",
    "dl_audio_stream": "⬇️  Baixando fluxo de áudio...",
    "downloaded": "⬇️  Baixado: {path}",
    "err_tmp_corrupt": "❌ Arquivo temporário corrompido ou vazio: {path}",
    "merging": "🔗 Mesclando vídeo e áudio...",
    "merge_cmd": "🔗 Mesclagem ffmpeg: {cmd}",
    "err_ffmpeg_code": "❌ ffmpeg terminou com código {code}",
    "stderr_tail": "   stderr: {stderr}",
    "err_output_missing": "❌ O arquivo de saída não existe ou é suspeitosamente pequeno.",
    "err_no_audio_track_out": "❌ Nenhuma faixa de áudio encontrada no arquivo de saída.",
    "warn_merge_failed": "⚠️  Falha na mesclagem. Tentando alternativa: progressive.",
    "ok_saved_fallback": "✅ Salvo (alternativa): {path}",

    # ---------- mp3 ----------
    "converting_mp3": "🎵 Convertendo para mp3...",
    "ok_audio_saved": "✅ Áudio salvo: {path}",
    "warn_mp3_failed": "⚠️  Falha na conversão para mp3, mantendo o arquivo original",
    "err_mp3_convert": "❌ Erro na conversão para mp3: {stderr}",
    "extra_mp3": "🎵 Salvando também uma faixa mp3...",
    "ok_mp3_saved": "✅ mp3 salvo: {path}",
    "warn_mp3_kept_source": "⚠️  mp3 não convertido, arquivo original mantido: {path}",

    # ---------- Result ----------
    "ok_video_saved": "✅ Vídeo salvo: {path}",
    "err_download": "❌ Erro no download: {error}",
    "ok_log_entry": "📝 Entrada adicionada a {txt} e {html}",

    # ---------- Transcript ----------
    "info_no_captions": "ℹ️  Legendas/transcrição indisponíveis.",
    "info_available_subs": "📄 Legendas disponíveis: {codes}",
    "info_transcript_lang": "📄 Idioma da transcrição: {code}",
    "ok_transcript": "✅ Transcrição: {path}",
    "warn_transcript_error": "⚠️  Erro na transcrição: {error}",
    "tr_title": "# Transcrição: {title}",
    "tr_author": "# Autor: {author}",
    "tr_lang": "# Idioma: {lang}",
    "tr_source": "# Fonte: {url}",

    # ---------- HTML log ----------
    "html_title": "Registro de vídeos baixados",
    "html_total": "Total de entradas: {count}",
    "html_empty": "Ainda não há entradas",
    "html_col_date": "Data",
    "html_col_type": "Tipo",
    "html_col_title": "Título",
    "html_col_author": "Autor",
    "html_col_quality": "Qualidade",
    "html_col_audio_lang": "Idioma do áudio",
    "html_col_duration": "Duração",
    "html_col_size": "Tamanho",
    "html_col_audio_file": "Arquivo de áudio",

    # ---------- Web server ----------
    "srv_url_missing": "URL ausente",
    "srv_bad_quality": "Qualidade inválida",
    "srv_ui_missing": "web_ui.html não encontrado junto a web_server.py",
    "srv_open_browser": "🌐 Abra no seu navegador: {url}",
    "srv_task_starting": "Iniciando…",
    "srv_task_done": "Concluído",

    # ---------- Web UI ----------
    "web_app_title": "🎬 YouTube Downloader",
    "web_subtitle": "Vídeo, áudio e transcrições — direto do seu navegador",
    "web_lang": "🌐 Idioma",
    "web_url_label": "URL do vídeo",
    "web_url_placeholder": "https://www.youtube.com/watch?v=...",
    "web_quality_label": "Qualidade",
    "web_q_max": "Máxima (1080p+ DASH)",
    "web_q_medium": "Média",
    "web_lang_audio": "Idioma do áudio / transcrição",
    "web_q_audio": "Somente áudio (mp3)",
    "web_extra_label": "Extras",
    "web_save_mp3": "Salvar também mp3 junto ao mp4",
    "web_btn_info": "🔍 Obter informações",
    "web_btn_download": "⬇️ Baixar",
    "web_btn_loading": '<span class="spinner"></span>Carregando…',
    "web_info_title": "Informações do vídeo",
    "web_author": "Autor",
    "web_duration": "Duração",
    "web_id": "ID",
    "web_status": "Status",
    "web_resolutions": "Resoluções disponíveis",
    "web_captions_yes": "  •  legendas disponíveis",
    "web_captions_no": "  •  sem legendas",
    "web_badge_new": "Novo",
    "web_badge_downloaded": "Já baixado",
    "web_progress_title": "Progresso do download",
    "web_files_title": "📁 Arquivos baixados",
    "web_log_title": "📊 Registro de downloads",
    "web_col_file": "Arquivo",
    "web_col_size": "Tamanho",
    "web_col_date": "Data",
    "web_col_type": "Tipo",
    "web_col_title": "Título",
    "web_col_author": "Autor",
    "web_col_quality": "Qualidade",
    "web_col_audio_file": "Arquivo de áudio",
    "web_download_link": "baixar",
    "web_empty_files": "Ainda não há arquivos",
    "web_empty_log": "Ainda não há entradas",
    "web_err_no_url": "Insira uma URL de vídeo",
    "web_err_server": "Erro do servidor",
    "web_err_prefix": "Erro: ",
    "web_error_prefix": "❌ Erro: ",
    "web_launching": "Iniciando…",
    "web_done": "✅ Concluído",
}
