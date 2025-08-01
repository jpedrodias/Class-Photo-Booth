#!/bin/bash

# Criar diretórios se não existirem e definir permissões
mkdir -p /app/fotos /app/thumbs /app/zips

# Definir permissões para escrita
chmod -R 777 /app/fotos /app/thumbs /app/zips 2>/dev/null || true

# Executar o comando original
exec "$@"
