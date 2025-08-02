# 📸 Especificação de Requisitos – Class Photo Booth v2.0

## 1. Introdução

### 1.1 Objetivo
O **Class Photo Booth** é uma aplicação web moderna e responsiva desenvolvida para facilitar a captura, gestão e organização de fotografias de alunos por turma. A aplicação utiliza dados fornecidos através de ficheiro CSV e oferece uma interface intuitiva otimizada para dispositivos móveis e desktop.

### 1.2 Escopo
A aplicação é uma solução web completa, desenvolvida em **Python com Flask**, com as seguintes capacidades:

- **Autenticação segura** com palavra-passe configurável
- **Gestão inteligente de dados** via upload de ficheiros CSV
- **Interface responsiva** otimizada para dispositivos móveis
- **Captura de fotografias** com suporte a múltiplas câmaras
- **Processamento automático** de imagens e thumbnails
- **Download organizado** das fotografias por turma
- **Deployment via Docker** com mapeamento de permissões

### 1.3 Público-Alvo
O sistema destina-se a:
- **Operadores de fotografia escolar** 
- **Professores e auxiliares**
- **Administradores escolares**
- **Qualquer utilizador** responsável por documentação fotográfica de turmas

### 1.4 Tecnologias Implementadas
- **Backend**: Python 3.12, Flask, OpenCV
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript ES6+
- **Containerização**: Docker & Docker Compose
- **Armazenamento**: Sistema de ficheiros com estrutura organizada
- **Design**: Mobile-first, responsivo, glassmorphism

## 2. Arquitetura e Deployment

### 2.1 Estrutura de Deployment
```
├── docker-compose.yml      # Orquestração de containers
├── Dockerfile             # Imagem da aplicação
├── start.sh               # Script de inicialização com UID/GID
├── .env                   # Configurações de ambiente
└── flaskapp/             # Código da aplicação
    ├── app.py            # Backend Flask
    ├── requirements.txt  # Dependências Python
    ├── templates/        # Templates HTML
    ├── static/          # Assets estáticos
    ├── fotos/           # Fotografias originais
    ├── thumbs/          # Miniaturas (250x250)
    └── zips/            # Arquivos temporários
```

### 2.2 Mapeamento de Permissões
- **UID/GID dinâmico**: Container usa o mesmo UID/GID do host
- **Volumes persistentes**: Dados mantidos entre reinicializações
- **Permissões automáticas**: Criação segura de diretórios

## 3. Sistema de Autenticação

### 3.1 Login Flexível (RF-AUTH)
- **Palavra-passe configurável**: Suporta letras, números e símbolos
- **Sem limitação de tamanho**: Até 255 caracteres
- **Configuração via ambiente**: `FLASKAPP_LOGIN_PIN` no ficheiro .env
- **Interface moderna**: Design mobile-first com gradientes

### 3.2 Gestão de Sessões
- **Sessões Flask**: Controlo de acesso baseado em cookies
- **Middleware de segurança**: Redirecionamento automático para login
- **Logout seguro**: Limpeza completa da sessão

## 4. Gestão de Dados CSV

### 4.1 Upload Inteligente (RF-CSV)
- **Formato obrigatório**: `turma,numero,processo,nome`
- **Validação automática**: Verificação de extensão .csv
- **Interface drag & drop**: Suporte para arrastar ficheiros
- **Feedback visual**: Estados de loading e sucesso
- **Substituição segura**: Backup automático de dados existentes

### 4.2 Detecção Automática
- **Redirecionamento inteligente**: Se CSV não existe → Settings
- **Verificação consistente**: Todas as rotas verificam existência
- **Tratamento de erros**: Fallback graceful para configurações

## 5. Interface Responsiva

### 5.1 Design Mobile-First
- **Viewport otimizado**: `user-scalable=no` para experiência consistente
- **Grid responsivo**: Adaptação automática a diferentes ecrãs
- **Touch-friendly**: Botões com tamanho adequado para dedos
- **Haptic feedback**: Vibração em dispositivos móveis

### 5.2 Páginas Principais

#### 5.2.1 Login (`/login`)
- **Design moderno**: Gradientes e sombras suaves
- **Campo flexível**: Aceita qualquer tipo de palavra-passe
- **Auto-focus**: Cursor automático no campo de entrada
- **Prevenção de zoom**: iOS-friendly

#### 5.2.2 Listagem de Turmas (`/turmas`)
- **Cards interativos**: Efeitos hover e animações
- **Estatísticas visuais**: Contagem de turmas disponíveis
- **Glassmorphism**: Efeitos de transparência e blur
- **Navegação intuitiva**: Botões de ação na parte inferior

#### 5.2.3 Pauta da Turma (`/turma/<nome>`)
- **Grid adaptativo**: Layout responsivo para alunos
- **Estatísticas em tempo real**: Contagem de fotos / progresso
- **Thumbnails dinâmicos**: Preview das fotos capturadas
- **Indicadores visuais**: Status de foto existente/faltante

#### 5.2.4 Configurações (`/settings`)
- **Interface condicional**: Mostra opções baseadas no estado
- **Upload avançado**: Drag & drop + validação
- **Feedback detalhado**: Informações sobre formato CSV
- **Estado adaptativo**: Diferentes layouts conforme dados existentes

### 5.3 Elementos Visuais
- **Ícones consistentes**: Bootstrap Icons em toda a aplicação
- **Esquema de cores**: Azul primário (#667eea) + gradientes
- **Tipografia**: Segoe UI para máxima legibilidade
- **Favicon personalizado**: Ícone de câmera temático

## 6. Sistema de Captura

### 6.1 Interface de Captura (`/capture_photo/<turma>/<processo>`)
- **Seleção de câmara**: Dropdown com dispositivos disponíveis
- **Memória persistente**: localStorage para lembrar câmara escolhida
- **Preview em tempo real**: Stream de vídeo ao vivo
- **Controles por teclado**: Enter (capturar) / Escape (voltar)

### 6.2 Processamento de Imagens
- **Captura em alta qualidade**: Resolução original da câmara
- **Conversão automática**: Canvas → JPEG com compressão otimizada
- **Thumbnails inteligentes**: Crop quadrado 250x250px
- **Qualidade diferenciada**: 95% para originais, 50% para thumbnails

### 6.3 Armazenamento Organizado
```
fotos/
├── 5A/
│   ├── 3035.jpg          # Processo do aluno
│   └── 3999.jpg
└── 5B/
    └── 4763.jpg

thumbs/
├── 5A/
│   ├── 3035.jpg          # Thumbnail 250x250
│   └── 3999.jpg
└── 5B/
    └── 4763.jpg
```

## 7. Sistema de Download

### 7.1 Geração de ZIP (`/download/<turma>`)
- **Criação em memória**: Sem ficheiros temporários no disco
- **Compressão otimizada**: ZIP standard com boa taxa de compressão
- **Nome descritivo**: `{turma}.zip`
- **Verificação de conteúdo**: Alerta se não há fotos disponíveis

### 7.2 Serving de Thumbnails (`/thumbs/<turma>/<processo>.jpg`)
- **Cache disabled**: Sempre mostra versão mais recente
- **Fallback inteligente**: Ícone padrão se thumbnail não existe
- **Otimização de rede**: Compressão adequada para web

## 8. Funcionalidades Avançadas

### 8.1 Contagem Dinâmica
- **Backend counting**: Python conta fotos reais no sistema de ficheiros
- **Estatísticas em tempo real**: Progresso por turma
- **Percentagem de conclusão**: Indicador visual de progresso

### 8.2 Navegação Inteligente
- **Breadcrumbs implícitos**: Botões de "Voltar" contextuais
- **Estados preservados**: Câmara selecionada mantida entre sessões
- **Redirecionamentos automáticos**: Fluxo guiado baseado no estado

### 8.3 Tratamento de Erros
- **Permissões robustas**: Compatível Windows/Linux
- **Criação segura de diretórios**: Função `safe_makedirs()`
- **Fallbacks inteligentes**: Redirecionamento para configurações quando necessário

## 9. Requisitos Técnicos

### 9.1 Sistema Base
- **Python 3.12+**: Linguagem principal
- **Docker & Docker Compose**: Containerização
- **Sistema operativo**: Linux, Windows, macOS
- **Navegador moderno**: Chrome 90+, Firefox 90+, Safari 14+

### 9.2 Dependências
```txt
Flask                      # Framework web
opencv-python             # Processamento de imagens
```

### 9.3 Configuração de Ambiente
```env
FLASKAPP_LOGIN_PIN=1234           # Palavra-passe de acesso
FLASKAPP_SECRET_KEY=secretkey     # Chave para sessões Flask
FLASKAPP_PORT=80                  # Porta de exposição
TZ=Lisbon/Portugal               # Timezone
UID=1000                         # User ID (auto-configurado)
GID=1000                         # Group ID (auto-configurado)
```

## 10. Fluxo de Utilizador Completo

### 10.1 Primeiro Acesso
1. **Navegador** → `http://localhost` → Redirecionamento automático para `/login`
2. **Login** → Inserir palavra-passe → Se CSV não existe → `/settings`
3. **Upload CSV** → Carregar ficheiro → Validação → Redirecionamento para `/turmas`
4. **Seleção de turma** → Click no card da turma → `/turma/{nome}`

### 10.2 Operação Normal
1. **Login** → Palavra-passe → `/turmas` (se CSV existe)
2. **Escolha da turma** → Visualização da pauta com estatísticas
3. **Captura individual** → Click no aluno → Seleção/memorização de câmara → Captura
4. **Retorno automático** → Pauta atualizada com thumbnail
5. **Download final** → Botão "Download" → ZIP com todas as fotos da turma

### 10.3 Gestão Contínua
- **Logout seguro**: Botão sempre disponível na barra inferior
- **Reconfiguração**: Acesso a `/settings` para novo CSV
- **Câmara lembrada**: Próximas capturas usam última câmara selecionada

## 11. Considerações de Segurança

### 11.1 Autenticação
- **Palavra-passe obrigatória**: Acesso protegido a todas as funcionalidades
- **Sessões seguras**: Gestão adequada de cookies de sessão
- **Logout automático**: Sessões expiram quando navegador fecha

### 11.2 Armazenamento
- **Ficheiros locais**: Dados nunca saem do sistema local
- **Permissões controladas**: Acesso restrito aos diretórios da aplicação
- **Validação de entrada**: Apenas ficheiros CSV aceites

### 11.3 Rede
- **Bind local**: Aplicação disponível apenas na rede local
- **Sem exposição externa**: Não há configuração para acesso público
- **Headers de segurança**: Cache control para proteger dados sensíveis

## 12. Manutenção e Suporte

### 12.1 Logs e Debugging
- **Logs estruturados**: Output detalhado para resolução de problemas
- **Debug mode**: Configurável via variável de ambiente
- **Error handling**: Tratamento graceful de erros com feedback ao utilizador

### 12.2 Backup e Recovery
- **Dados persistentes**: Volumes Docker mantêm dados entre atualizações
- **CSV versionável**: Possibilidade de manter múltiplas versões
- **Estrutura simples**: Fácil backup manual de diretórios

### 12.3 Escalabilidade
- **Single-user design**: Otimizado para uso individual/local
- **Performance adequada**: Suporta turmas com até 50+ alunos
- **Recursos mínimos**: Baixo consumo de CPU/RAM

---

**Versão do Documento**: 2.0  
**Data de Atualização**: Janeiro 2025  
**Estado da Implementação**: ✅ 100% Completo

Esta especificação reflete fielmente a aplicação **Class Photo Booth** implementada, incluindo todas as funcionalidades, melhorias de UX/UI e otimizações técnicas desenvolvidas durante o processo de criação.