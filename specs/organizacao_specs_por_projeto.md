# Organização das specs do Whisper Local

## Status

Implementada

## Problema

O Whisper Local ainda não possuía instruções nem modelo de specs próprios.
Regras de privacidade, processamento local e distribuição não devem ser
misturadas com as de outros programas do workspace.

## Comportamento esperado

O `WHISPER_LOCAL` mantém localmente suas instruções, seu modelo e suas specs.
Entradas de áudio ou vídeo, transcrições, modelos baixados, ambiente virtual e
pacote de distribuição recebem cuidados específicos deste projeto.

## Regras de negócio e privacidade

- Specs do Whisper Local ficam somente em `WHISPER_LOCAL/specs/`.
- Toda spec nova parte de `WHISPER_LOCAL/specs/_modelo.md`.
- Conteúdo de entrada e transcrições não devem ser usados como documentação
  nem incluídos na distribuição sem decisão explícita.
- O comportamento declarado de processamento local deve ser preservado.

## Dados e componentes afetados

- `WHISPER_LOCAL/AGENTS.md`;
- `WHISPER_LOCAL/specs/`;
- `README.md` do projeto.

## Critérios de aceite

- O projeto possui `AGENTS.md`, modelo e README de specs locais.
- O modelo contempla privacidade, arquivos de mídia, saídas, modelos e
  distribuição.
- Nenhuma spec de outro programa permanece nesta pasta.
- As regras do projeto permanecem autocontidas neste repositório.

## Validação de encerramento

- [x] Links entre as specs relacionadas validados.
- [x] Ausência de specs deslocadas confirmada.
- [x] Separação entre código, entradas, saídas e distribuição revisada.
- [x] Sintaxe Python e estado dos arquivos revisados.

## Compatibilidade e riscos

- A mudança é documental e não transcreve nem move arquivos de mídia.
- A criação da governança local não altera o pacote distribuído existente.

## Fora de escopo

- Refatoração do transcritor ou recriação do pacote ZIP.
- Remoção de entradas, saídas ou ambientes existentes.
