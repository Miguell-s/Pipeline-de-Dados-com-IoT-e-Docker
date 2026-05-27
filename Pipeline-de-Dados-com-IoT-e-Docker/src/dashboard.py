import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Dashboard IoT - Temperatura",
    page_icon="🌡️",
    layout="wide"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://iot_user:iot_password@localhost:5432/iot_db"
)

@st.cache_data(ttl=60)
def load_data_from_view(view_name):
    engine = create_engine(DATABASE_URL)
    query = text(f"SELECT * FROM {view_name}")
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

st.title("🌡️ Dashboard IoT - Monitoramento de Temperatura")
st.markdown("---")

try:
    df_avg = load_data_from_view("avg_temp_por_dispositivo")
    df_hourly = load_data_from_view("leituras_por_hora")
    df_daily = load_data_from_view("temp_max_min_por_dia")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Dispositivos", len(df_avg))
    with col2:
        st.metric("Total de Leituras", int(df_avg["total_leituras"].sum()))
    with col3:
        st.metric("Temperatura Média Geral", f"{df_avg['temperatura_media'].mean():.2f}°C")

    st.markdown("---")

    st.subheader("📊 Média de Temperatura por Dispositivo")
    fig_bar = px.bar(
        df_avg,
        x="dispositivo",
        y="temperatura_media",
        color="temperatura_media",
        color_continuous_scale="Viridis",
        title="Temperatura Média por Dispositivo IoT",
        labels={"dispositivo": "Dispositivo", "temperatura_media": "Temperatura Média (°C)"},
        height=500
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    st.subheader("⏰ Leituras por Hora do Dia")
    fig_line = px.line(
        df_hourly,
        x="hora",
        y="total_leituras",
        title="Quantidade de Leituras por Hora",
        labels={"hora": "Hora do Dia", "total_leituras": "Total de Leituras"},
        markers=True,
        color_discrete_sequence=["#1f77b4"]
    )
    fig_line.update_xaxes(tickmode="linear", dtick=1)
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    st.subheader("📈 Temperaturas Máximas e Mínimas por Dia")
    fig_daily = go.Figure()

    fig_daily.add_trace(go.Scatter(
        x=df_daily["data"],
        y=df_daily["temperatura_maxima"],
        name="Temperatura Máxima",
        line=dict(color="#e74c3c", width=2),
        mode="lines+markers"
    ))

    fig_daily.add_trace(go.Scatter(
        x=df_daily["data"],
        y=df_daily["temperatura_minima"],
        name="Temperatura Mínima",
        line=dict(color="#3498db", width=2),
        mode="lines+markers"
    ))

    fig_daily.update_layout(
        title="Temperaturas Máximas e Mínimas Diárias",
        xaxis_title="Data",
        yaxis_title="Temperatura (°C)",
        height=500,
        hovermode="x unified"
    )

    st.plotly_chart(fig_daily, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Detalhes dos Dados")
    with st.expander("Ver dados completos de média por dispositivo"):
        st.dataframe(df_avg)

except Exception as e:
    st.error(f"Erro ao conectar ao banco de dados: {e}")
    st.info("Certifique-se de que o Docker está rodando e o processamento dos dados foi executado.")
