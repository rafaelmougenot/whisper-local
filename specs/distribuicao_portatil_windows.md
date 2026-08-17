# Distribuição portátil para Windows

## Status

Implementada

## Problema

A distribuição atual exige que a pessoa instale Python, crie um ambiente
virtual e instale dependências. O processo é técnico demais para quem apenas
precisa colocar arquivos em uma pasta e transcrevê-los.

## Comportamento esperado

A pessoa deve poder extrair a distribuição em um Windows 10 ou 11 de 64 bits,
colocar áudios ou vídeos em `input/` e iniciar a transcrição com dois cliques,
sem instalar Python ou criar um ambiente virtual. Também deve ser possível
arrastar arquivos sobre o iniciador.

O uso e a construção pelo código-fonte também não devem exigir ambiente
virtual: as dependências podem ser instaladas para o usuário do Windows e os
scripts devem localizar o Python 3 disponível no sistema.

## Regras de negócio e privacidade

- O processamento da mídia e a geração das transcrições permanecem locais.
- O modelo `small` pode ser baixado no primeiro uso e armazenado em uma pasta de
  cache dentro da distribuição; ele não integra o pacote produzido pelo projeto.
- Arquivos existentes em `input/` e `output/` não podem ser removidos ou
  sobrescritos silenciosamente.
- Quando uma saída com o mesmo nome já existir, a nova transcrição deve receber
  um sufixo numérico comum nos arquivos TXT e SRT.
- No modo em lote, são processados somente formatos de mídia reconhecidos e a
  falha de um arquivo não impede a tentativa dos demais.

## Dados e componentes afetados

- `src/transcrever.py`, como fonte única do transcritor;
- `input/` e `output/`, preservadas como pastas de trabalho do desenvolvimento;
- `WHISPER_LOCAL_DISTRIBUICAO/`, como modelo legível da entrega;
- scripts de construção e dependências de desenvolvimento usadas para gerar o
  executável Windows;
- cache local do modelo na pasta `modelos/` da distribuição executada.

## Critérios de aceite

- Dada uma distribuição construída, quando ela for executada em Windows 10 ou
  11 de 64 bits sem Python instalado, então o programa deve iniciar normalmente.
- Dados arquivos compatíveis em `input/`, quando o iniciador for executado sem
  argumentos, então todos devem ser tentados e as saídas devem ir para `output/`.
- Dado um arquivo arrastado sobre o iniciador, quando ele for executado, então
  somente os caminhos informados devem ser tentados.
- Dadas saídas preexistentes, quando o mesmo nome for transcrito novamente,
  então os arquivos antigos devem permanecer inalterados.
- Dado que o modelo já foi baixado para `modelos/`, quando uma nova transcrição
  for executada sem internet, então o programa deve reutilizar esse modelo.
- Dado um pacote final, quando seu conteúdo for inspecionado, então ele não deve
  conter mídias, transcrições, ambientes virtuais ou modelos baixados.
- Dado Python 3.11 a 3.13 instalado no Windows, quando o código-fonte ou o script
  de build for executado, então nenhuma `.venv` deve ser exigida ou criada.

## Validação de encerramento

- [x] Critérios de aceite que não exigem carregar o modelo foram validados no
  ambiente disponível. O primeiro download e uma transcrição real permanecem
  como validação manual para não usar as mídias existentes sem autorização.
- [x] Sintaxe e caminhos dos scripts afetados verificados.
- [x] Código, arquivos, dependências e recursos substituídos revisados para
  evitar resíduos sem uso.
- [x] Áudios, vídeos, transcrições, modelos e ambientes virtuais não foram
  incluídos indevidamente na distribuição.
- [x] Estado dos arquivos e pacote de distribuição revisados.

## Compatibilidade e riscos

- A construção é específica para Windows de 64 bits e deve ser feita no
  sistema-alvo.
- Antivírus podem inspecionar ou bloquear executáveis Python não assinados.
- O primeiro uso depende de internet e espaço em disco para baixar o modelo.
- O modo CUDA continua fora do fluxo comum porque depende de bibliotecas NVIDIA
  compatíveis instaladas no computador.

## Fora de escopo

- Interface gráfica, instalador MSI, assinatura digital e distribuição do
  modelo dentro do pacote.
- Alteração ou exclusão dos arquivos reais existentes nas pastas de trabalho.
