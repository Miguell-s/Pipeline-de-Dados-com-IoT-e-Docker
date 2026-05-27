import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Dashboard IoT - Temperatura (Simplificado)",
    page_icon="🌡️",
    layout="wide"
)

@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'IOT-temp.csv')
    df = pd.read_csv(data_path)
    df['noted_date'] = pd.to_datetime(df['noted_date'], format='%d-%m-%Y %H:%M')
    return df

st.title("🌡️ Dashboard IoT - Monitoramento de Temperatura (Simplificado)")
st.markdown("---")
st.info("Esta versão funciona diretamente com o arquivo CSV (não precisa de Docker ou banco de dados)!")

try:
    df = load_data()
    
    df_avg = df.groupby('room_id/id').agg(
        total_leituras=('temp', 'count'),
        temperatura_media=('temp', 'mean'),
        temperatura_minima=('temp', 'min'),
        temperatura_maxima=('temp', 'max')
    ).reset_index().rename(columns={'room_id/id': 'dispositivo'})
    
    df['hora'] = df['noted_date'].dt.hour
    df_hourly = df.groupby('hora').size().reset_index(name='total_leituras')
    
    df['data'] = df['noted_date'].dt.date
    df_daily = df.groupby('data').agg(
        temperatura_minima=('temp', 'min'),
        temperatura_maxima=('temp', 'max'),
        temperatura_media=('temp', 'mean')
    ).reset_index()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Dispositivos", len(df_avg))
    with col2:
        st.metric("Total de Leituras", len(df))
    with col3:
        st.metric("Temperatura Média Geral", f"{df['temp'].mean():.2f}°C")
    
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
    
    with st.expander("Ver todas as leituras (primeiras 100)"):
        st.dataframe(df.head(100))

except Exception as e:
    st.error(f"Erro: {e}")
    st.info("Certifique-se de que o arquivo data/IOT-temp.csv existe!")
