import streamlit as st
from datetime import datetime, timedelta

from controllers.exames_controller import ExameManager

db_exame = ExameManager()

st.title("📅 Gestão de Exames")

aba = st.sidebar.radio("Navegação", ["Exames Vencidos", "Exames a Vencer", "Registrar Exame Realizado"])

if aba == "Exames Vencidos":
    st.header("❌ Exames Vencidos")
    exames_vencidos = db_exame.listar_exames_vencidos()
    if exames_vencidos:
        st.table(exames_vencidos)
    else:
        st.info("Nenhum exame vencido encontrado.")

elif aba == "Exames a Vencer":
    st.header("⏳ Exames a Vencer")
    dias = st.slider("Período de vencimento (dias)", min_value=7, max_value=90, value=30)
    exames_a_vencer = db_exame.listar_exames_a_vencer(dias)
    if exames_a_vencer:
        st.table(exames_a_vencer)
    else:
        st.info("Nenhum exame prestes a vencer.")

elif aba == "Registrar Exame Realizado":
    with st.expander("Cadastrar Exame Realizado"):
        st.header("📝 Cadastro de Exame Realizado")   
        funcionarios = db_exame.fetch_all("SELECT id, nome FROM funcionarios")
        funcionario_id = st.selectbox("Funcionário", placeholder="Selecione o funcionário", options=funcionarios, format_func=lambda x: x[1])
        exames = db_exame.fetch_all("""
        SELECT exames.id, exames.nome FROM exames
        INNER JOIN exames_necessarios_por_cargo ON exames.id = exames_necessarios_por_cargo.exame_id
        INNER JOIN funcionarios ON exames_necessarios_por_cargo.cargo_id = funcionarios.cargo_id
        WHERE funcionarios.id = ?
        """, (funcionario_id[0],))
        exame_id = st.selectbox("Exame",index=None, placeholder="Selecione o exame realizado", options=exames, format_func=lambda x: x[1])
        data_realizacao = st.date_input("Data da realização", datetime.today(), format="DD/MM/YYYY")
        if exame_id:
            data_proximo_exame = db_exame.calcular_proximo_exame(funcionario_id[0], exame_id[0], data_realizacao)
            meses_validade = st.selectbox("Validade (meses)", data_proximo_exame, disabled=True)
            validade = data_realizacao + timedelta(days=meses_validade * 30)

        if st.button("Cadastrar"):
            db_exame.registrar_exame_realizado(funcionario_id[0], exame_id[0], data_realizacao.strftime('%Y-%m-%d'), validade.strftime('%Y-%m-%d'))
            st.success("Exame registrado com sucesso!")

    with st.expander("Exames Realizados Pelo Funcionário"):
        st.header("📋 Exames Realizados")
        exames_realizados = db_exame.fetch_all("""
            SELECT exames.nome, exames_realizados.data_realizacao, exames_realizados.validade
            FROM exames_realizados
            JOIN exames ON exames_realizados.exame_id = exames.id
            WHERE exames_realizados.funcionario_id = ?
        """, (funcionario_id[0],))
        if exames_realizados:
            st.table(exames_realizados)
        else:
            st.info("Nenhum exame realizado por este funcionário.")