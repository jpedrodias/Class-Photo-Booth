# 📸 Especificação de Requisitos – Class Photo Booth

## 1. Introdução

### 1.1 Objetivo
O objetivo da aplicação **Class Photo Booth** é permitir a captura de fotografias de alunos por turma, com base numa listagem fornecida por um ficheiro CSV. A aplicação facilita a gestão, visualização e exportação das fotografias de forma organizada.

### 1.2 Escopo
A aplicação será uma aplicação web, desenvolvida em **Python com Flask**, capaz de correr localmente num computador com Python instalado. Permitirá:

- Importar uma listagem de alunos a partir de um ficheiro CSV
- Selecionar a turma e tirar fotografias individualmente aos alunos
- Visualizar os thumbnails das fotos tiradas
- Fazer download de um ficheiro ZIP com todas as fotografias de uma turma

### 1.3 Público-Alvo
O sistema será utilizado por operadores ou professores responsáveis por tirar fotografias das turmas escolares. **Não é necessário login ou gestão de utilizadores.**

## 2. Requisitos Funcionais

### RF01 – Importação de Alunos
- A aplicação deve carregar os dados de um ficheiro CSV contendo os campos:
  - `turma`, `numero`, `processo`, `nome`

### RF02 – Seleção de Turma
- Após o carregamento, deve ser apresentada uma listagem das turmas disponíveis em forma de cartões clicáveis.
- Nesta mesma página, o utilizador pode escolher qual câmara usar para capturar as fotos.

### RF03 – Visualização da Pauta da Turma
- Ao selecionar uma turma, é apresentada a "pauta" da turma com todos os alunos.
- Alunos com foto tirada já exibem um thumbnail.

### RF04 – Captura de Fotografia
- Ao selecionar um aluno, abre uma interface de captura com:
  - Enquadramento ao vivo (preview da câmara)
  - Botão para tirar a foto
- A fotografia tirada:
  - É guardada numa pasta com o nome da turma: `/fotos/{turma}`
  - Nome do ficheiro é igual ao número do processo: `{processo}.jpg`
  - Uma miniatura (thumbnail) é criada em `/thumbs/{turma}`

### RF05 – Download das Fotografias
- Deve haver um botão **"Download ZIP"** na visualização da turma
- Ao clicar:
  - Gera um ficheiro `.zip` com todas as fotografias da turma
  - O zip pode ser criado em memória usando `BytesIO` ou salvo em `/zips/{turma}.zip`

## 3. Requisitos Não Funcionais

### RNF01 – Portabilidade
- A aplicação deve funcionar num laptop com Python instalado, sem necessidade de instalação de servidores externos.
- Qualquer dispositivo na mesma rede local deve conseguir aceder via IP do computador onde a aplicação está a correr.

### RNF02 – Simplicidade
- Não haverá sistema de autenticação, nem base de dados.
- Todo o armazenamento será em sistema de ficheiros local.

### RNF03 – Desempenho e Escalabilidade
- A aplicação não precisa suportar acesso simultâneo por múltiplos utilizadores.
- O foco é o uso local, simples e funcional.

## 4. Estrutura de Pastas
/fotos/{turma} → Fotografias capturadas
/thumbs/{turma} → Thumbnails das fotos
/zips/{turma}.zip → Arquivo ZIP com as fotos da turma

## 5. Fluxo do Utilizador

1. O operador inicia a aplicação e carrega o ficheiro CSV com os alunos.
2. A página principal apresenta cartões com as turmas identificadas no CSV.
3. Ao clicar numa turma, o operador vê a pauta da turma com espaço para thumbnails.
4. Ao clicar num aluno, é aberta a interface de fotografia.
5. Após a captura, volta para a pauta com o thumbnail visível.
6. Quando todas as fotos estiverem tiradas, o operador pode clicar em "Download ZIP" para obter todas as imagens daquela turma.

## 6. Tecnologias

- **Backend**: Python (Flask)
- **Frontend**: HTML/CSS/JS simples (poderá ser usada uma biblioteca leve como Bootstrap)
- **Câmara**: A ser selecionada na interface (pode usar OpenCV, `camera-index` via browser ou outra abordagem)

## 7. Considerações Finais

- O sistema deve ser simples e direto ao ponto, evitando complexidades desnecessárias.
- O objetivo é facilitar e agilizar a tarefa de tirar fotos de alunos e organizar essas imagens por turma.