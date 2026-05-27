# Pipeline de Dados com IoT e Docker

## Introdução

Este projeto acadêmico implementa um pipeline completo de dados para processamento, armazenamento e visualização de leituras de temperatura de dispositivos IoT. Utilizando tecnologias modernas como Python, Docker, PostgreSQL, SQLAlchemy e Streamlit, o projeto demonstra boas práticas de engenharia de dados e desenvolvimento de aplicações interativas.

## Objetivo

Criar um pipeline de dados end-to-end que:
1. Receba e processe dados de sensores IoT de temperatura
2. Armazene os dados em um banco de dados PostgreSQL
3. Crie views otimizadas para análise
4. Visualize os dados em um dashboard interativo com Streamlit

## Tecnologias Utilizadas

- **Python**: Linguagem principal para processamento de dados
- **Docker**: Containerização do banco de dados PostgreSQL
- **PostgreSQL**: Banco de dados relacional para armazenamento
- **SQLAlchemy**: ORM para interação com o banco de dados
- **Pandas**: Manipulação e análise de dados
- **Streamlit**: Framework para criação de dashboards interativos
- **Plotly**: Visualizações gráficas interativas
- **Git/GitHub**: Controle de versão e hospedagem do código

## Estrutura de Pastas

```
/iot-pipeline
│
├── /data                          # Pasta para datasets
│   └── IOT-temp.csv               # Dataset de leituras de temperatura
│
├── /src                           # Código fonte do projeto
│   ├── process_data.py            # Script para processamento e inserção de dados
│   ├── database.py                # Configuração do banco de dados e modelos
│   ├── create_views.sql           # Views SQL para análise
│   └── dashboard.py               # Dashboard Streamlit
│
├── /docs                          # Documentação
│   └── imagens_dashboard          # Capturas de tela do dashboard
│
├── requirements.txt               # Dependências do projeto
├── docker-compose.yml             # Configuração Docker para PostgreSQL
├── .gitignore                     # Arquivos ignorados pelo Git
└── README.md                      # Este arquivo
```

## Como Instalar

### 1. Pré-requisitos

Antes de começar, certifique-se de ter instalado:
- Python 3.8+
- Docker e Docker Compose
- Git

### 2. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/Pipeline-de-Dados-com-IoT-e-Docker.git
cd Pipeline-de-Dados-com-IoT-e-Docker
```

### 3. Criar ambiente virtual

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

## Como Executar

### Opção 1: Versão Simplificada (Sem Docker, Sem Banco de Dados)
Para visualizar o dashboard imediatamente, sem necessidade de configurar Docker ou PostgreSQL:

```bash
cd src
streamlit run dashboard_simplificado.py
```

O dashboard abrirá automaticamente no navegador em: `http://localhost:8501`

---

### Opção 2: Versão Completa (Com Docker e PostgreSQL)

#### 1. Subir o Docker com PostgreSQL

```bash
docker-compose up -d
```

Isso iniciará um container PostgreSQL com as seguintes configurações:
- Usuário: `iot_user`
- Senha: `iot_password`
- Banco de dados: `iot_db`
- Porta: `5432`

### 2. Processar e inserir dados no banco

```bash
cd src
python process_data.py
```

Este script irá:
- Ler o arquivo CSV
- Limpar e tratar os dados
- Criar a tabela no PostgreSQL
- Inserir todos os registros

### 3. Criar as views SQL

Conecte-se ao banco de dados e execute o script `create_views.sql`:

```bash
docker exec -i iot_postgres psql -U iot_user -d iot_db < src/create_views.sql
```

Ou usando um cliente PostgreSQL como pgAdmin, DBeaver ou psql:

```sql
-- Execute o conteúdo de src/create_views.sql
```

### 4. Executar o dashboard Streamlit

```bash
cd src
streamlit run dashboard.py
```

O dashboard estará disponível em: `http://localhost:8501`

## Views SQL

O projeto contém 3 views otimizadas para análise:

### 1. `avg_temp_por_dispositivo`
Média de temperatura, total de leituras, temperatura mínima e máxima por dispositivo IoT.

**Colunas:**
- `dispositivo`: ID do dispositivo/sala
- `total_leituras`: Número total de leituras
- `temperatura_media`: Temperatura média
- `temperatura_minima`: Temperatura mínima registrada
- `temperatura_maxima`: Temperatura máxima registrada

### 2. `leituras_por_hora`
Quantidade de leituras realizadas em cada hora do dia.

**Colunas:**
- `hora`: Hora do dia (0-23)
- `total_leituras`: Total de leituras naquela hora

### 3. `temp_max_min_por_dia`
Temperaturas máximas, mínimas e médias por dia.

**Colunas:**
- `data`: Data da leitura
- `temperatura_minima`: Temperatura mínima do dia
- `temperatura_maxima`: Temperatura máxima do dia
- `temperatura_media`: Temperatura média do dia

## Insights Obtidos

1. **Padrões de temperatura**: Identificação de horários com temperaturas mais elevadas
2. **Diferenças entre ambientes**: Comparativo entre temperaturas internas e externas
3. **Desempenho dos dispositivos**: Análise da frequência e qualidade das leituras por sensor
4. **Tendências temporais**: Variação de temperatura ao longo dos dias e semanas

## Comandos Git Utilizados

### Inicializar repositório
```bash
git init
```

### Adicionar arquivos
```bash
git add .
```

### Commit das alterações
```bash
git commit -m "Primeiro commit: Estrutura básica do projeto"
git commit -m "Adiciona script de processamento de dados"
git commit -m "Implementa dashboard Streamlit"
```

### Conectar ao GitHub
```bash
git remote add origin https://github.com/seu-usuario/Pipeline-de-Dados-com-IoT-e-Docker.git
```

### Enviar para o GitHub
```bash
git push -u origin main
```

### Atualizar repositório local
```bash
git pull origin main
```

## Capturas de Tela do Dashboard

*(Adicione suas capturas de tela na pasta `docs/imagens_dashboard/` e referencie-as aqui)*

Exemplo:
![Dashboard - Média por Dispositivo](docs/imagens_dashboard/avg_temp.png)
![Dashboard - Leituras por Hora](docs/imagens_dashboard/hourly.png)
![Dashboard - Temperaturas Diárias](docs/imagens_dashboard/daily.png)

## Possíveis Melhorias Futuras

1. **Ingestão em tempo real**: Implementar Kafka ou MQTT para receber dados de sensores em tempo real
2. **Alertas**: Adicionar sistema de notificações para temperaturas fora do intervalo normal
3. **Machine Learning**: Implementar modelos de previsão de temperatura
4. **Autenticação**: Adicionar sistema de login ao dashboard
5. **Escalabilidade**: Migrar para arquitetura cloud (AWS, GCP, Azure)
6. **Testes automatizados**: Adicionar testes unitários e de integração
7. **Monitoramento**: Implementar logging e monitoramento do pipeline

## Dataset

O dataset utilizado é o **Temperature Readings: IoT Devices** disponível no Kaggle:

https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

Para utilizar o dataset completo:
1. Acesse o link acima
2. Faça login no Kaggle
3. Baixe o arquivo `IOT-temp.csv`
4. Coloque-o na pasta `/data` do projeto

## Licença

Este projeto é para fins acadêmicos.

---

**Desenvolvido para fins educacionais**
