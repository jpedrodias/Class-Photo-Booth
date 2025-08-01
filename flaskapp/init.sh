#!/bin/bash

# Criar diretórios se não existirem e definir permissões
mkdir -p /app/fotos /app/thumbs /app/zips

# Tentar definir permissões para escrita (pode falhar silenciosamente)
chmod 777 /app/fotos /app/thumbs /app/zips 2>/dev/null || true

# Verificar se conseguimos escrever nos diretórios
for dir in /app/fotos /app/thumbs /app/zips; do
    if [ -w "$dir" ]; then
        echo "✓ Diretório $dir está acessível para escrita"
    else
        echo "⚠ Aviso: Diretório $dir pode não estar acessível para escrita"
    fi
done

# Executar o comando original
exec "$@"
