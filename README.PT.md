[English](README.md) | [Русский](README.RU.md) | [Українська](README.UK.md) | Português | [Deutsch](README.DE.md) | [Français](README.FR.md)

# 🎬 YouTube Downloader

Baixa **vídeo (mp4)**, **áudio (mp3)** e **transcrições de texto** (a partir das legendas) do YouTube — qualquer um deles, ou todos de uma vez. Duas interfaces:

- **CLI** — `download.py`, uma ferramenta de console escrita em Python;
- **Web UI** — `web_server.py` (Flask) + `web_ui.html` (JS no navegador): barra de progresso, registro de downloads, lista de arquivos com links para download.

![YouTube Downloader](Screeshot/YouTubDownloader.png)

Idiomas da interface: **English, Русский, Українська, Português, Deutsch, Français**.

Licença: **MIT** — uso livre sem restrições (consulte a [LICENSE](LICENSE)).

## Funcionalidades

- 🎥 Vídeo na qualidade máxima (1080p / 1440p / 4K via fluxos DASH mesclados com ffmpeg), média ou baixa
- 🎧 Somente áudio, convertido para mp3 (192 kbps) — ótimo para ouvir em qualquer lugar
- 📄 Transcrição de texto a partir das legendas (limpa de marcações de tempo e de formatação) salva junto ao arquivo de mídia
- 🌍 Seleção do idioma da faixa de áudio e das legendas (`--lang ru`, `en`, …); a faixa em russo tem prioridade em vídeos multilíngues
- 🔁 Proteção contra duplicatas: vídeos já baixados são ignorados (um registro baseado em ID é mantido)
- 📝 Registro de downloads em dois formatos: `download_log.txt` e `download_log.html`
- 🖥️ Web UI: informações do vídeo antes do download, progresso ao vivo, histórico e download de arquivos direto do navegador
- 🌐 Idioma da interface alternável tanto na CLI quanto na Web UI (6 idiomas, detecção automática por padrão)

## Estrutura do repositório

```
├── download.py            # CLI de download (lógica central)
├── web_server.py          # Servidor web (API Flask + serve a interface)
├── web_ui.html            # Interface web (HTML/JS)
├── i18n.py                # Motor de idioma da interface
├── locales/               # Traduções: en, ru, uk, pt, de, fr
├── requirements.txt       # Dependências Python
├── Screeshot/             # Captura de tela usada nos READMEs
├── .github/workflows/     # GitHub Actions: download sem instalação local
├── .devcontainer/         # Configuração do GitHub Codespaces
└── legacy/                # Versões antigas dos scripts (histórico de desenvolvimento)
```

Os arquivos baixados vão para `downloads/`, e o registro fica na raiz do projeto. Ambos os caminhos (e arquivos pessoais) são excluídos do git via `.gitignore`.

## Instalação (local)

### 1. Requisitos

- **Python 3.10+** (testado no 3.12)
- **ffmpeg** — necessário para mesclar fluxos DASH (qualidade acima de 720p) e converter para mp3. Sem ele o programa funciona, mas o vídeo fica limitado a 720p (progressive) e o áudio permanece no formato original (m4a)

### 2. Instalando o ffmpeg

| SO | Comando |
|---|---|
| macOS | `brew install ffmpeg` |
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| Windows | `winget install Gyan.FFmpeg` (ou `choco install ffmpeg`), depois reinicie o terminal |

Verifique: `ffmpeg -version`

### 3. Clonando e instalando dependências

```bash
git clone https://github.com/YOUR_LOGIN/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso: CLI

### Modo interativo

```bash
python download.py
```

Pergunta passo a passo: URL → qualidade → idioma → se deve salvar mp3.

### Com argumentos

```bash
python download.py "https://youtu.be/XXXX" max          # vídeo na melhor qualidade + transcrição
python download.py "https://youtu.be/XXXX" audio        # somente mp3 + transcrição
python download.py "https://youtu.be/XXXX" medium --lang en
python download.py "https://youtu.be/XXXX" max --mp3 -o video   # + mp3, pasta video/
python download.py "https://youtu.be/XXXX" max --ui-lang de     # interface em alemão
```

| Argumento | Significado |
|---|---|
| `url` | URL do vídeo (sem ela — modo interativo) |
| `quality` | `max` / `medium` / `low` / `audio` |
| `--lang`, `-l` | idioma do áudio e da transcrição (padrão: `ru`) |
| `--mp3` | salvar adicionalmente uma faixa mp3 junto ao mp4 |
| `-o`, `--output` | pasta de saída (padrão: `downloads`) |
| `--ui-lang`, `-u` | idioma da interface: `en`/`ru`/`uk`/`pt`/`de`/`fr` |

O idioma da interface é detectado automaticamente a partir da localidade do sistema (`LANG`/`LC_ALL`); use `--ui-lang` para substituir, ou defina a variável de ambiente `YTD_LANG`.

Ajuda completa: `python download.py --help`

Resultado em `downloads/`:

```
Video title.mp4                  # vídeo (ou .mp3 no modo audio)
Video title.mp3                  # com --mp3 ou quality=audio
Video title.transcript.txt       # transcrição a partir das legendas
```

## Uso: Web UI

```bash
python web_server.py
```

Abra **http://127.0.0.1:5000** no seu navegador:

1. Cole um link → **“Obter informações”**: miniatura, autor, duração, resoluções disponíveis, disponibilidade de legendas, status (“novo” / “já baixado”)
2. Escolha qualidade e idioma → **“Baixar”**: barra de progresso ao vivo e registro no console
3. Abaixo — a lista de arquivos prontos (baixe direto do navegador) e o registro completo de downloads

O idioma da interface é escolhido com o seletor 🌐 no canto superior direito; a escolha fica lembrada no navegador. O registro de downloads/saída do console também segue o idioma selecionado.

Host e porta podem ser alterados com variáveis de ambiente:

```bash
HOST=0.0.0.0 PORT=8080 python web_server.py
```

## Executando direto no GitHub

Um site estático (GitHub Pages) não funciona aqui — é necessário um backend Python. Duas opções viáveis.

### Opção 1: GitHub Actions (sem instalação local)

O repositório inclui um workflow acionado manualmente, `.github/workflows/download.yml`:

1. Abra a aba **Actions** → **Download YouTube video** → **Run workflow**
2. Forneça a URL, a qualidade (`max`/`medium`/`low`/`audio`), o idioma do conteúdo, o idioma da interface e se o mp3 é necessário
3. Aguarde a conclusão → o resumo da execução mostra o **artifact `youtube-download`** — baixe o zip com seus arquivos

Dica: o formulário de execução tem um endereço permanente — `https://github.com/SEU_LOGIN/SEU_REPOSITORIO/actions/workflows/download.yml` (adicione aos favoritos). Marque **publish** no formulário para anexar os arquivos a um **Release** do GitHub — uma página permanente com links diretos de download (veja *Releases* no repositório, ou o link no resumo da execução). Essa é a maneira correta de manter os arquivos “dentro do repositório”: fazer commit de vídeos no histórico do git o incha (e o GitHub bloqueia arquivos acima de 100 MB).

⚠️ **Limitações**: os artifacts ficam armazenados por tempo limitado (1 dia aqui), o tamanho é limitado, e o YouTube costuma bloquear IPs de datacenters (o erro “Sign in to confirm you're not a bot”). Para uso regular, execute localmente.

### Opção 2: GitHub Codespaces (Web UI completa na nuvem)

1. Botão **Code** → aba **Codespaces** → **Create codespace on master**
2. O contêiner é configurado via `.devcontainer/devcontainer.json`: Python 3.12, ffmpeg, dependências — instalados automaticamente
3. No terminal: `python web_server.py` — a porta 5000 é encaminhada automaticamente e o navegador abre sozinho

Para referência: a cota gratuita do Codespaces para contas pessoais do GitHub é de 120 core-hours por mês — suficiente para uso ocasional.

## Registro de downloads

Cada download adiciona uma entrada:

- `download_log.txt` — registro legível por máquinas (usado para detectar “já baixado”);
- `download_log.html` — uma tabela amigável com links.

Para baixar novamente um vídeo, remova seu ID de `download_log.txt` (e o arquivo de `downloads/`).

## Solução de problemas

| Problema | Solução |
|---|---|
| O vídeo baixa no máximo a 720p | ffmpeg não encontrado → mesclagem DASH indisponível. Instale o ffmpeg e verifique com `ffmpeg -version` |
| “Sign in to confirm you're not a bot” | O YouTube bloqueia seu IP (comum em VPNs/datacenters). Tente outra rede ou execute localmente |
| Sem mp3, resta um `.m4a` | ffmpeg não está instalado — conversão impossível, o fluxo de áudio original foi mantido |
| Sem transcrição | O vídeo não tem legendas. Legendas geradas automaticamente pelo YouTube também são suportadas, quando disponíveis |
| “Address already in use” ao iniciar a Web UI | No macOS a porta 5000 costuma ser ocupada pelo AirPlay (Control Center) — use outra porta: `PORT=8080 python web_server.py` |
| pytubefix para de funcionar após uma atualização do YouTube | `pip install -U pytubefix` — a biblioteca é corrigida ativamente conforme o YouTube muda |

## Licença

[MIT](LICENSE) — uso, cópia, modificação e distribuição livres, incluindo uso comercial.

⚠️ **Nota legal**: este programa destina-se ao download de conteúdo sobre o qual você tem direitos (conteúdo próprio, conteúdo com licença aberta ou download permitido na sua jurisdição). Respeite os Termos de Serviço do YouTube e os direitos autorais.
