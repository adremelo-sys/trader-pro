import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Trade Pro", page_icon="📈", layout="centered")

st.markdown("""
<style>
    .stButton>button { background-color: #ef4444; color: white; font-weight: bold; width: 100%; height: 50px; border-radius: 10px; }
    .stButton>button:hover { background-color: #dc2626; }
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎯 Trade do Dia", "📊 Estratégia do Mês"])

with tab1:
    st.title("Calcular Trade de Hoje")
    tipo = st.selectbox("Tipo", ["compra", "venda"])
    c1, c2, c3 = st.columns(3)
    with c1: entrada = st.number_input("Entrada", value=128000.00, step=10.0)
    with c2: stop = st.number_input("Stop", value=127800.00, step=10.0)
    with c3: alvo = st.number_input("Alvo", value=128400.00, step=10.0)
    qtd = st.number_input("Qtd Contratos", value=2, min_value=1)
    
    if st.button("CALCULAR TRADE"):
        risco_pts = (entrada - stop) if tipo == "compra" else (stop - entrada)
        alvo_pts = (alvo - entrada) if tipo == "compra" else (entrada - alvo)
        valor_ponto = 0.20
        risco_reais = risco_pts * qtd * valor_ponto
        alvo_reais = alvo_pts * qtd * valor_ponto
        payoff = alvo_pts / risco_pts if risco_pts != 0 else 0
        
        col1, col2 = st.columns(2)
        col1.metric("RISCO", f"R$ {risco_reais:,.2f}", f"{risco_pts:.0f} pts")
        col2.metric("ALVO", f"R$ {alvo_reais:,.2f}", f"{alvo_pts:.0f} pts")
        if payoff >= 2:
            st.success(f"Payoff {payoff:.2f} - EXCELENTE! Trade aprovado ✅")
        else:
            st.warning(f"Payoff {payoff:.2f} - Cuidado com esse trade")

with tab2:
    st.title("Resultado do Mês")
    st.caption("Veja sua evolução de perdas e ganhos")

    # Dados editáveis
    st.subheader("Seus Trades do Mês (edite aqui)")
    dados_iniciais = pd.DataFrame({
        "Dia": [1, 2, 3, 4, 5, 6, 7, 8],
        "Resultado R$": [80, -40, 160, -40, 120, 80, -40, 200]
    })
    
    df_editado = st.data_editor(dados_iniciais, num_rows="dynamic", use_container_width=True)
    
    if not df_editado.empty:
        # Cálculos
        total_ganho = df_editado[df_editado["Resultado R$"] > 0]["Resultado R$"].sum()
        total_perda = df_editado[df_editado["Resultado R$"] < 0]["Resultado R$"].sum()
        saldo = df_editado["Resultado R$"].sum()
        qtd_wins = len(df_editado[df_editado["Resultado R$"] > 0])
        qtd_loss = len(df_editado[df_editado["Resultado R$"] < 0])
        
        # Métricas
        c1, c2, c3 = st.columns(3)
        c1.metric("Saldo Total", f"R$ {saldo:,.2f}")
        c2.metric("Total Ganho", f"R$ {total_ganho:,.2f}")
        c3.metric("Total Perda", f"R$ {total_perda:,.2f}")

        # Gráfico 1: Barra Ganho x Perda por dia
        st.subheader("📊 Ganho e Perda por Dia")
        df_editado["Cor"] = df_editado["Resultado R$"].apply(lambda x: "Ganho" if x > 0 else "Perda")
        st.bar_chart(df_editado, x="Dia", y="Resultado R$", color="Cor", use_container_width=True)

        # Gráfico 2: Curva de Patrimônio
        st.subheader("📈 Curva de Patrimônio (Acumulado)")
        df_editado["Acumulado"] = df_editado["Resultado R$"].cumsum()
        st.line_chart(df_editado, x="Dia", y="Acumulado", use_container_width=True)

        # Gráfico 3: Pizza de acertos
        st.subheader("🎯 Taxa de Acerto")
        df_pizza = pd.DataFrame({
            "Resultado": ["Ganhos", "Perdas"],
            "Qtd": [qtd_wins, qtd_loss]
        })
        st.bar_chart(df_pizza, x="Resultado", y="Qtd", use_container_width=True)
        
        if saldo > 0:
            st.success(f"Você está LUCRATIVO! {qtd_wins} ganhos x {qtd_loss} perdas")
        else:
            st.error(f"Atenção ao risco! Ajuste seu payoff.")