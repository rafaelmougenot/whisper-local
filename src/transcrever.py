from __future__ import annotations

import argparse
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable

from faster_whisper import WhisperModel


MODELO_PADRAO = "small"
FORMATOS_SUPORTADOS = {
    ".aac", ".avi", ".flac", ".m4a", ".mkv", ".mov", ".mp3",
    ".mp4", ".mpeg", ".mpg", ".ogg", ".opus", ".wav", ".webm", ".wma",
}


def pasta_do_programa() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


PASTA_PROGRAMA = pasta_do_programa()
PASTA_ENTRADA_PADRAO = PASTA_PROGRAMA / "input"
PASTA_SAIDA_PADRAO = PASTA_PROGRAMA / "output"
PASTA_MODELOS_PADRAO = PASTA_PROGRAMA / "modelos"


def formatar_tempo_srt(segundos: float) -> str:
    milissegundos = int(round(segundos * 1000))
    horas, resto = divmod(milissegundos, 3_600_000)
    minutos, resto = divmod(resto, 60_000)
    segundos, milissegundos = divmod(resto, 1_000)
    return f"{horas:02}:{minutos:02}:{segundos:02},{milissegundos:03}"


def monitor(stop_event: threading.Event) -> None:
    inicio = time.perf_counter()
    while not stop_event.wait(30):
        tempo = int(time.perf_counter() - inicio)
        horas = tempo // 3600
        minutos = (tempo % 3600) // 60
        segundos = tempo % 60
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"Ainda processando... ({horas:02}:{minutos:02}:{segundos:02})",
            flush=True,
        )


def listar_entradas(caminhos: Iterable[Path], pasta_entrada: Path) -> list[Path]:
    entradas: list[Path] = []
    informados = list(caminhos)
    if not informados:
        pasta_entrada.mkdir(parents=True, exist_ok=True)
        informados = [pasta_entrada]

    for caminho in informados:
        caminho = caminho.expanduser()
        if caminho.is_dir():
            candidatos = sorted(
                (item for item in caminho.iterdir() if item.is_file()),
                key=lambda item: item.name.casefold(),
            )
            entradas.extend(
                item for item in candidatos if item.suffix.lower() in FORMATOS_SUPORTADOS
            )
        elif caminho.is_file():
            if caminho.suffix.lower() not in FORMATOS_SUPORTADOS:
                print(f"Ignorado (formato não reconhecido): {caminho}")
                continue
            entradas.append(caminho)
        else:
            print(f"Ignorado (não encontrado): {caminho}")

    unicos: list[Path] = []
    vistos: set[str] = set()
    for entrada in entradas:
        chave = os.path.normcase(str(entrada.resolve()))
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(entrada.resolve())
    return unicos


def caminhos_de_saida(pasta_saida: Path, nome_base: str) -> tuple[Path, Path]:
    numero = 1
    while True:
        sufixo = "" if numero == 1 else f"_{numero}"
        caminho_txt = pasta_saida / f"{nome_base}{sufixo}.txt"
        caminho_srt = pasta_saida / f"{nome_base}{sufixo}.srt"
        if not caminho_txt.exists() and not caminho_srt.exists():
            return caminho_txt, caminho_srt
        numero += 1


def criar_modelo(
    modelo_nome: str, dispositivo: str, pasta_modelos: Path
) -> WhisperModel:
    pasta_modelos.mkdir(parents=True, exist_ok=True)
    compute_type = "float16" if dispositivo == "cuda" else "int8"
    print("Carregando modelo. No primeiro uso, o download pode demorar...", flush=True)
    return WhisperModel(
        modelo_nome,
        device=dispositivo,
        compute_type=compute_type,
        download_root=str(pasta_modelos),
    )


def transcrever(
    arquivo: Path,
    modelo: WhisperModel,
    modelo_nome: str,
    idioma: str | None,
    dispositivo: str,
    pasta_saida: Path,
) -> tuple[Path, Path]:
    if not arquivo.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
    pasta_saida.mkdir(parents=True, exist_ok=True)
    inicio = time.perf_counter()

    print("\n" + "=" * 60)
    print("WHISPER LOCAL")
    print("=" * 60)
    print(f"Arquivo......: {arquivo.name}")
    print(f"Modelo.......: {modelo_nome}")
    print(f"Dispositivo..: {dispositivo.upper()}")
    print(f"Início.......: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60, flush=True)

    stop_event = threading.Event()
    monitor_thread = threading.Thread(target=monitor, args=(stop_event,), daemon=True)
    monitor_thread.start()
    try:
        segmentos, informacoes = modelo.transcribe(
            str(arquivo), language=idioma, beam_size=5, vad_filter=True
        )
        segmentos = list(segmentos)
    finally:
        stop_event.set()
        monitor_thread.join(timeout=1)

    print(
        f"\nIdioma detectado: {informacoes.language} "
        f"({informacoes.language_probability:.1%})"
    )
    caminho_txt, caminho_srt = caminhos_de_saida(pasta_saida, arquivo.stem)

    with caminho_txt.open("w", encoding="utf-8") as txt:
        for segmento in segmentos:
            texto = segmento.text.strip()
            if texto:
                txt.write(texto + "\n")

    with caminho_srt.open("w", encoding="utf-8") as srt:
        numero_legenda = 1
        for segmento in segmentos:
            texto = segmento.text.strip()
            if not texto:
                continue
            srt.write(f"{numero_legenda}\n")
            srt.write(
                f"{formatar_tempo_srt(segmento.start)} --> "
                f"{formatar_tempo_srt(segmento.end)}\n"
            )
            srt.write(f"{texto}\n\n")
            numero_legenda += 1

    tempo_total = int(time.perf_counter() - inicio)
    horas = tempo_total // 3600
    minutos = (tempo_total % 3600) // 60
    segundos = tempo_total % 60
    print("\n" + "=" * 60)
    print("TRANSCRIÇÃO CONCLUÍDA")
    print("=" * 60)
    print(f"Tempo total..: {horas:02}:{minutos:02}:{segundos:02}")
    print(f"TXT..........: {caminho_txt}")
    print(f"SRT..........: {caminho_srt}")
    print("=" * 60, flush=True)
    return caminho_txt, caminho_srt


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Transcreve arquivos com Faster Whisper. Sem caminhos, processa todos "
            "os arquivos reconhecidos da pasta input."
        )
    )
    parser.add_argument(
        "arquivos", nargs="*", type=Path,
        help="Arquivos ou pastas. Se omitidos, usa a pasta input.",
    )
    parser.add_argument("--modelo", default=MODELO_PADRAO)
    parser.add_argument("--idioma", default=None)
    parser.add_argument(
        "--dispositivo", choices=["cpu", "cuda"], default="cpu"
    )
    parser.add_argument("--entrada", type=Path, default=PASTA_ENTRADA_PADRAO)
    parser.add_argument("--saida", type=Path, default=PASTA_SAIDA_PADRAO)
    parser.add_argument("--modelos", type=Path, default=PASTA_MODELOS_PADRAO)
    return parser


def main() -> None:
    argumentos = criar_parser().parse_args()
    entradas = listar_entradas(argumentos.arquivos, argumentos.entrada)
    if not entradas:
        print(f"Nenhum áudio ou vídeo reconhecido em: {argumentos.entrada}")
        print("Coloque arquivos na pasta input e tente novamente.")
        raise SystemExit(2)

    print(f"{len(entradas)} arquivo(s) encontrado(s).")
    try:
        modelo = criar_modelo(
            argumentos.modelo, argumentos.dispositivo, argumentos.modelos
        )
    except Exception as erro:
        print(f"\nNão foi possível carregar o modelo: {erro}")
        raise SystemExit(1) from erro

    falhas = 0
    for indice, arquivo in enumerate(entradas, start=1):
        print(f"\nProcessando {indice} de {len(entradas)}: {arquivo.name}")
        try:
            transcrever(
                arquivo, modelo, argumentos.modelo, argumentos.idioma,
                argumentos.dispositivo, argumentos.saida,
            )
        except Exception as erro:
            falhas += 1
            print(f"\nErro ao transcrever {arquivo.name}: {erro}")

    concluidos = len(entradas) - falhas
    print(f"\nResumo: {concluidos} concluído(s), {falhas} falha(s).")
    if falhas:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
