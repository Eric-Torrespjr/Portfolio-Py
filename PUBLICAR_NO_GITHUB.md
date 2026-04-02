# Como publicar este repositório no GitHub

## 1. Criar o repositório vazio no site GitHub

1. Acesse [https://github.com/new](https://github.com/new).
2. Escolha um nome (ex.: `automacoes-python`).
3. **Não** marque “Initialize with README” (o projeto já tem arquivos locais).
4. Crie o repositório.

## 2. No seu PC (PowerShell), na pasta do projeto

Substitua `SEU_USUARIO` e `NOME_DO_REPO` pelos valores reais.

```powershell
cd "c:\Users\erice\OneDrive\Desktop\automacoes"

git init
git add .
git commit -m "feat: automações Python (integração API, FastAPI, painel tkinter)"

git branch -M main
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
git push -u origin main
```

Se o Git pedir login, use **Personal Access Token** (GitHub → Settings → Developer settings → Personal access tokens) como senha no HTTPS, ou configure [SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

## 3. Alternativa: GitHub Desktop

Instale [GitHub Desktop](https://desktop.github.com/), adicione a pasta `automacoes` como repositório local e use **Publish repository**.
