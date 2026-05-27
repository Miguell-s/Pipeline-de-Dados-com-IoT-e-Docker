# Documentação Acadêmica - Pipeline de Dados com IoT e Docker

## 1. Contextualização do Projeto

A Internet das Coisas (IoT) tem revolucionado a forma como coletamos e analisamos dados em diversos setores, desde agricultura e monitoramento ambiental até gestão de edifícios inteligentes e sistemas industriais. Sensores IoT geram volumes massivos de dados em tempo real, criando a necessidade de pipelines de dados robustos e eficientes para processar, armazenar e extrair insights valiosos dessas informações.

Este projeto acadêmico explora a implementação de um pipeline de dados completo para monitoramento de temperatura utilizando dispositivos IoT. Através da combinação de tecnologias modernas como Python, Docker, PostgreSQL e Streamlit, demonstramos como transformar dados brutos de sensores em visualizações interativas e decisões baseadas em dados.

## 2. Explicação do Pipeline de Dados

O pipeline de dados implementado segue uma arquitetura de ponta a ponta composta por quatro etapas principais:

### 2.1 Ingestão de Dados
Os dados são coletados a partir de dispositivos IoT que medem temperatura em ambientes internos e externos. O dataset utilizado contém registros de leituras de temperatura com timestamp, identificador do dispositivo e localização (interno/externo).

### 2.2 Processamento e Limpeza
Os dados brutos passam por um processo de limpeza que inclui:
- Remoção de valores ausentes
- Conversão de tipos de dados (especialmente datas e horários)
- Validação de intervalos de temperatura plausíveis

### 2.3 Armazenamento
Os dados processados são armazenados em um banco de dados relacional PostgreSQL, containerizado via Docker para garantir portabilidade e consistência do ambiente. Utilizamos SQLAlchemy como ORM (Object-Relational Mapper) para facilitar a interação entre Python e o banco de dados.

### 2.4 Visualização e Análise
Um dashboard interativo desenvolvido com Streamlit e Plotly permite a exploração dos dados através de gráficos dinâmicos, facilitando a identificação de padrões, tendências e anomalias nas leituras de temperatura.

## 3. Configuração do Ambiente

### 3.1 Tecnologias e Versões
- **Python 3.8+**: Linguagem de programação principal
- **Docker 20.10+**: Plataforma de containerização
- **PostgreSQL 15**: Sistema de gerenciamento de banco de dados relacional
- **SQLAlchemy 2.0+**: ORM para Python
- **Pandas 2.0+**: Biblioteca para manipulação de dados
- **Streamlit 1.28+**: Framework para dashboards
- **Plotly 5.17+**: Biblioteca para visualizações gráficas

### 3.2 Ambiente Virtual Python
A utilização de um ambiente virtual é uma boa prática para isolar as dependências do projeto:
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Instalação de Dependências
Todas as dependências estão listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 4. Criação e Configuração do Docker

### 4.1 Docker Compose
O arquivo `docker-compose.yml` define o serviço PostgreSQL com as seguintes configurações:
- Imagem: postgres:15-alpine (versão leve e otimizada)
- Variáveis de ambiente: usuário, senha e nome do banco de dados
- Porta: 5432 (padrão PostgreSQL)
- Volume: Persistência de dados

### 4.2 Inicialização do Container
Para iniciar o serviço PostgreSQL:
```bash
docker-compose up -d
```

O parâmetro `-d` executa o container em segundo plano (detached mode).

### 4.3 Verificação do Status
Para verificar se o container está rodando corretamente:
```bash
docker-compose ps
```

## 5. Inserção de Dados no Banco de Dados

### 5.1 Modelo de Dados
A tabela `temperature_readings` é definida utilizando SQLAlchemy e contém os seguintes campos:
- `id`: Chave primária autoincremental
- `room_id`: Identificador do dispositivo/sala
- `noted_date`: Data e hora da leitura
- `temp`: Valor da temperatura em graus Celsius
- `out_or_in`: Indicador se a leitura foi interna ou externa

### 5.2 Script de Processamento
O script `process_data.py` realiza as seguintes operações:
1. Carrega o dataset CSV utilizando Pandas
2. Limpa os dados removendo valores nulos
3. Converte a coluna de data para o formato datetime
4. Inicializa o banco de dados e cria a tabela (se não existir)
5. Insere todos os registros no banco de dados

### 5.3 Execução do Script
```bash
cd src
python process_data.py
```

## 6. Views SQL para Análise

Para otimizar as consultas e facilitar a análise, foram criadas três views materializadas:

### 6.1 View 1: `avg_temp_por_dispositivo`
Esta view calcula estatísticas agregadas por dispositivo, incluindo:
- Total de leituras
- Temperatura média
- Temperatura mínima
- Temperatura máxima

Utilidade: Permite comparar o desempenho e as medições entre diferentes dispositivos IoT.

### 6.2 View 2: `leituras_por_hora`
Esta view agrupa as leituras por hora do dia, contando quantas medições foram realizadas em cada intervalo horário.

Utilidade: Identifica padrões de atividade dos sensores e horários de pico de medições.

### 6.3 View 3: `temp_max_min_por_dia`
Esta view calcula as temperaturas máxima, mínima e média para cada dia do período de coleta.

Utilidade: Permite analisar tendências de temperatura ao longo do tempo e identificar dias com variações extremas.

## 7. Dashboard Interativo com Streamlit

O dashboard desenvolvido com Streamlit oferece uma interface intuitiva para exploração dos dados:

### 7.1 Layout e Componentes
- **Título e Métricas Principais**: Cards com total de dispositivos, total de leituras e temperatura média geral
- **Gráfico de Barras**: Média de temperatura por dispositivo
- **Gráfico de Linhas**: Leituras por hora do dia
- **Gráfico Interativo**: Temperaturas máximas e mínimas por dia
- **Seção de Dados**: Visualização da tabela completa com opção de expansão

### 7.2 Tecnologias de Visualização
- **Streamlit**: Framework para criação rápida de aplicações web de dados
- **Plotly Express**: Biblioteca para gráficos interativos e responsivos
- **Cache**: Mecanismo de cache para otimizar o desempenho das consultas

### 7.3 Execução do Dashboard
```bash
cd src
streamlit run dashboard.py
```

O dashboard fica disponível em `http://localhost:8501`.

## 8. Insights e Resultados

A análise dos dados permite extrair diversos insights valiosos:

1. **Padrões Diários**: Identificação de horários com temperaturas mais elevadas (normalmente entre 12h e 16h) e mais baixas (madrugada).
2. **Diferenças Ambientais**: Comparativo entre temperaturas internas e externas, mostrando como o ambiente interno é mais estável.
3. **Desempenho dos Dispositivos**: Análise da frequência de leituras por sensor, identificando dispositivos com maior ou menor atividade.
4. **Tendências Temporais**: Variação de temperatura ao longo dos dias e semanas, possibilitando a identificação de padrões semanais ou mensais.
5. **Detecção de Anomalias**: Identificação de leituras de temperatura fora do intervalo normal, que podem indicar falhas nos sensores ou eventos excepcionais.

## 9. Aplicações Reais em IoT

Este projeto tem aplicações práticas em diversos cenários do mundo real:

### 9.1 Edifícios Inteligentes
Monitoramento de temperatura em ambientes corporativos para otimização do consumo de energia com ar-condicionado e aquecimento.

### 9.2 Agricultura de Precisão
Monitoramento de temperatura em estufas e plantações para garantir condições ideais de cultivo e prever pragas ou doenças.

### 9.3 Saúde e Cuidados com Idosos
Monitoramento de temperatura em residências de idosos para detectar condições perigosas (como temperaturas muito elevadas ou baixas).

### 9.4 Logística e Cadeia de Frio
Monitoramento de temperatura durante o transporte de produtos perecíveis (alimentos, medicamentos) para garantir a qualidade e segurança.

### 9.5 Data Centers
Monitoramento contínuo de temperatura em data centers para prevenir superaquecimento de servidores e equipamentos.

## 10. Conclusão

Este projeto acadêmico demonstrou com sucesso a implementação de um pipeline de dados completo para IoT, integrando diversas tecnologias modernas em uma solução coesa e funcional. Através deste trabalho, foi possível:

- Aplicar conceitos de engenharia de dados na prática
- Utilizar containerização com Docker para garantir consistência ambiental
- Implementar um banco de dados relacional com PostgreSQL
- Desenvolver visualizações interativas com Streamlit e Plotly
- Extrair insights valiosos de dados de sensores IoT

O conhecimento adquirido neste projeto pode ser estendido para aplicações mais complexas, incluindo ingestão de dados em tempo real, machine learning para previsão de temperatura e integração com serviços em nuvem.

---

**Documentação elaborada para fins acadêmicos**
