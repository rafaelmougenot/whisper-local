# Diretrizes do Whisper Local

Estas orientações se aplicam a todo este repositório.

## Specs

- Mantenha specs deste programa somente em `WHISPER_LOCAL/specs/`.
- Comece novas specs por `WHISPER_LOCAL/specs/_modelo.md`.
- Não use arquivos de áudio, vídeo ou transcrições como documentação de
  desenvolvimento.

## Privacidade e processamento local

- Preserve o processamento local declarado pelo programa; não envie mídia ou
  transcrições a serviços externos sem decisão explícita do usuário.
- Trate arquivos em `input/` e `output/` como conteúdo potencialmente sensível.
- Não inclua mídia, transcrições, modelos baixados, caches ou ambientes
  virtuais no pacote de distribuição.

## Código e distribuição

- Avalie separadamente o código de desenvolvimento e
  `WHISPER_LOCAL_DISTRIBUICAO/`; alterações que devam chegar ao usuário final
  precisam manter ambos coerentes ou documentar por que divergem.
- Não recrie o arquivo ZIP sem validar seu conteúdo e sem solicitação
  explícita.
- Não reutilize nem distribua uma `.venv` criada em outra máquina.

## Validação local

- Valide sintaticamente os arquivos Python afetados.
- Execute `--help` ou testes que não carreguem modelos quando forem suficientes.
- Não transcreva arquivos reais apenas para validar uma alteração sem
  solicitação explícita.
- Revise arquivos duplicados entre desenvolvimento e distribuição, dependências,
  entradas, saídas e artefatos temporários antes de concluir.
