# Segurança e privacidade

## Dados processados

O Whisper Local processa áudio e vídeo no computador do usuário. O modelo é
baixado do Hugging Face no primeiro uso; as mídias e transcrições não são
enviadas a uma API de transcrição.

Arquivos colocados em `input/`, resultados em `output/` e modelos em `modelos/`
são dados locais e não devem ser adicionados ao Git ou a relatórios públicos.

## Antes de publicar

Execute a auditoria na raiz do projeto:

```powershell
.\auditar_publicacao.ps1
```

Revise também o conteúdo exato preparado para commit com `git status` e
`git diff --cached`. Não publique arquivos reais usados em testes.

## Relato responsável

Se encontrar uma vulnerabilidade, não publique dados pessoais, mídias ou
credenciais em uma issue. Entre em contato de forma privada com o mantenedor do
repositório pelo canal indicado no perfil do GitHub.
