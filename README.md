# Whisper Local

Fiz esse projeto para deixar a transcrição de áudio e vídeo o mais simples
possível.

A ideia é bem direta: você baixa a pasta, coloca os arquivos em `input`, dá
dois cliques e encontra o texto pronto em `output`. Tudo é processado no seu
computador, sem enviar seus áudios para uma API de transcrição.

## Só quero usar

Baixe a versão pronta na página de
[Releases](https://github.com/rafaelmougenot/whisper-local/releases/latest).

Depois:

1. Extraia o ZIP.
2. Coloque os áudios ou vídeos na pasta `input`.
3. Execute `Iniciar Whisper.bat`.
4. Pegue os arquivos prontos na pasta `output`.

Também dá para arrastar um ou mais arquivos diretamente sobre
`Iniciar Whisper.bat`.

Não precisa instalar Python nem configurar ambiente virtual.

## O que ele entrega

Para cada arquivo processado, o programa gera:

- `.txt` com a transcrição;
- `.srt` com texto e marcações de tempo.

Se já existir uma transcrição com o mesmo nome, ela é preservada. O novo
resultado recebe `_2`, `_3` e assim por diante.

## Primeiro uso

Na primeira execução, o programa precisa de internet para baixar o modelo
`small`. Depois disso, ele reaproveita o modelo salvo na pasta `modelos` e
pode trabalhar offline.

Dependendo do tamanho do arquivo e da velocidade do computador, a transcrição
pode levar alguns minutos.

## Privacidade

Os arquivos são processados localmente. Áudios, vídeos e transcrições não são
enviados para uma API de transcrição.

As pastas `input`, `output` e `modelos` ficam fora do Git para evitar que
arquivos pessoais sejam publicados por acidente.

## Rodando pelo código-fonte

É necessário ter Python 3.11, 3.12 ou 3.13 de 64 bits.

```powershell
python -m pip install --user -r requirements.txt
python src\transcrever.py
```

Isso também funciona sem criar ambiente virtual.

## Desenvolvimento

As instruções para gerar a distribuição e revisar uma publicação estão em
[CONTRIBUTING.md](CONTRIBUTING.md).
