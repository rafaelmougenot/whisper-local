# Desenvolvimento e publicação

## Preparar o ambiente

O projeto usa Python 3.11 a 3.13 de 64 bits sem exigir ambiente virtual.

```powershell
python -m pip install --user -r requirements-build.txt
```

## Gerar a distribuição portátil

```powershell
.\build.ps1
```

O resultado fica em `releases/WHISPER_LOCAL_PORTATIL/`. O script interrompe se
essa pasta já existir para não substituir uma release por acidente.

O diretório `WHISPER_LOCAL_DISTRIBUICAO/` contém os arquivos textuais
acrescentados ao pacote. O executável e a pasta `_internal/` são gerados
durante o build.

## Revisar antes de publicar

```powershell
.\auditar_publicacao.ps1
git status --short --ignored
git diff --cached
```

O repositório deve receber somente código-fonte, documentação e o modelo textual
da distribuição. Não publique mídias, transcrições, modelos, caches, ambientes
virtuais, executáveis ou credenciais.

Para distribuir o aplicativo pronto:

1. Confira que `input/` e `output/` estão vazias.
2. Confira que não existe uma pasta `modelos/` dentro da release.
3. Compacte `releases/WHISPER_LOCAL_PORTATIL/`.
4. Anexe o ZIP a uma GitHub Release.

O ZIP final não deve ser adicionado diretamente ao histórico do repositório.
