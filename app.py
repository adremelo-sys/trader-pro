import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Trader Pro - Calculadora", page_icon="📈", layout="wide")

# --- CSS PREMIUM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #334155;
    }
    .main-header h1 { color: white; margin: 0; font-size: 32px; letter-spacing: -1px; }
    .main-header p { color: #94a3b8; margin: 5px 0 0 0; font-size: 14px; }
    
    .stButton>button { 
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%); 
        color: white; font-weight: 800; width: 100%; height: 55px; 
        border-radius: 12px; border: none; font-size: 16px;
        letter-spacing: 1px; box-shadow: 0 4px 15px rgba(239,68,68,0.3);
    }
    .stButton>button:hover { transform: scale(1.02); background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%); }
    
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 12px;
    }
    div[data-testid="stMetric"] label { color: #94a3b8 !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- HEADER PROFISSIONAL ---
st.markdown("""
<div class="main-header">
    <h1>📈 TRADER PRO</h1>
    <p>CALCULADORA DE RISCO • PAYOFF • GERENCIAMENTO PROFISSIONAL</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎯 TRADE DO DIA", "📊 MEU MÊS"])

with tab1:
    col_form, col_result = st.columns([1.2, 1], gap="large")
    
    with col_form:
        st.markdown("### ⚙️ Configuração do Trade")
        tipo = st.selectbox("Direção do Trade", ["🟢 Compra (Long)", "🔴 Venda (Short)"])
        tipo_limpo = "compra" if "Compra" in tipo else "venda"
        
        c1, c2, c3 = st.columns(3)
        with c1: entrada = st.number_input("Preço Entrada", value=128000.00, step=10.0, format="%.2f")
        with c2: stop = st.number_input("Preço Stop", value=127800.00, step=10.0, format="%.2f")
        with c3: alvo = st.number_input("Preço Alvo", value=128400.00, step=10.0, format="%.2f")
        
        qtd = st.number_input("Quantidade de Contratos", value=2, min_value=1, step=1)
        calcular = st.button("CALCULAR TRADE AGORA 🚀")

    with col_result:
        if calcular:
            risco_pts = (entrada - stop) if tipo_limpo == "compra" else (stop - entrada)
            alvo_pts = (alvo - entrada) if tipo_limpo == "compra" else (entrada - alvo)
            valor_ponto = 0.20
            risco_reais = risco_pts * qtd * valor_ponto
            alvo_reais = alvo_pts * qtd * valor_ponto
            payoff = alvo_pts / risco_pts if risco_pts != 0 else 0
            
            st.markdown("### 📊 Resultado")
            m1, m2 = st.columns(2)
            m1.metric("RISCO", f"R$ {risco_reais:,.2f}", f"{risco_pts:.0f} pts", delta_color="inverse")
            m2.metric("ALVO", f"R$ {alvo_reais:,.2f}", f"{alvo_pts:.0f} pts")
            
            st.metric("PAYOFF / RISCO:RETORNO", f"{payoff:.2f}x")
            
            if payoff >= 2.5:
                st.success(f"✅ TRADE EXCELENTE! Payoff {payoff:.2f} - Pode operar com confiança")
                st.balloons()
            elif payoff >= 1.5:
                st.warning(f"⚠️ Payoff {payoff:.2f} - Trade bom, mas gerencie o risco")
            else:
                st.error(f"❌ Payoff {payoff:.2f} - NÃO RECOMENDADO. Risco maior que retorno!")
        else:
            st.info("👈 Configure seu trade ao lado e clique em CALCULAR para ver o resultado aqui.")

with tab2:
    st.markdown("### 📅 Seu Performance no Mês")
    st.caption("Edite seus trades abaixo e veja os gráficos atualizarem automaticamente.")

    dados_iniciais = pd.DataFrame({
        "Dia": [1, 2, 3, 4, 5, 6, 7, 8],
        "Resultado R$": [80, -40, 160, -40, 120, 80, -40, 200]
    })
    
    c_edit, c_stats = st.columns([1.2, 1], gap="large")
    
    with c_edit:
        st.markdown("**📝 Editar Resultados**")
        df_editado = st.data_editor(dados_iniciais, num_rows="dynamic", use_container_width=True, height=300)
    
    if not df_editado.empty:
        total_ganho = df_editado[df_editado["Resultado R$"] > 0]["Resultado R$"].sum()
        total_perda = df_editado[df_editado["Resultado R$"] < 0]["Resultado R$"].sum()
        saldo = df_editado["Resultado R$"].sum()
        qtd_wins = len(df_editado[df_editado["Resultado R$"] > 0])
        qtd_loss = len(df_editado[df_editado["Resultado R$"] < 0])
        taxa = (qtd_wins / len(df_editado) * 100) if len(df_editado) > 0 else 0
        
        with c_stats:
            st.markdown("**💰 Resumo**")
            cc1, cc2 = st.columns(2)
            cc1.metric("Saldo Total", f"R$ {saldo:,.2f}")
            cc2.metric("Taxa Acerto", f"{taxa:.0f}%")
            
            cc3, cc4 = st.columns(2)
            cc3.metric("Total Ganho", f"R$ {total_ganho:,.2f}")
            cc4.metric("Total Perda", f"R$ {total_perda:,.2f}")

            if saldo > 0:
                st.success(f"🔥 LUCRATIVO! {qtd_wins}W x {qtd_loss}L")
            else:
                st.error(f"⚠️ Em drawdown. Revise a estratégia.")

        st.divider()
        
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("**📊 Ganho/Perda por Dia**")
            df_editado["Cor"] = df_editado["Resultado R$"].apply(lambda x: "Ganho" if x > 0 else "Perda")
            st.bar_chart(df_editado, x="Dia", y="Resultado R$", color="Cor", use_container_width=True)
        
        with g2:
            st.markdown("**📈 Curva de Capital Acumulado**")
            df_editado["Acumulado"] = df_editado["Resultado R$"].cumsum()
            st.line_chart(df_editado, x="Dia", y="Acumulado", use_container_width=True)

st.markdown("---")
st.caption("© 2026 Trader Pro - Desenvolvido para traders profissionais")
