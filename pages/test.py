import streamlit as st
from datetime import datetime

from controllers.exames_controller import ExameManager
from controllers.funcionario_controller import FuncionarioManager
from controllers.cargo_controller import CargoManager
from controllers.clinicas_controller import ClinicasManager

exameController = ExameManager()
funcionarioController = FuncionarioManager()
cargoController = CargoManager()
clinicaController = ClinicasManager()


st.title("📅 Gestão de Exames")

aba = st.sidebar.radio("Navegação", ["Exames Vencidos", "Exames a Vencer", "Registrar Exame Realizado"])

if aba == "Exames Vencidos":
    st.header("❌ Exames Vencidos")
    exames_vencidos = exameController.listar_exames_vencidos()
    if exames_vencidos:
        st.table(exames_vencidos)
    else:
        st.info("Nenhum exame vencido encontrado.")

elif aba == "Exames a Vencer":
    st.header("⏳ Exames a Vencer")
    dias = st.slider("Período de vencimento (dias)", min_value=7, max_value=90, value=30)
    exames_a_vencer = exameController.listar_exames_a_vencer(dias)
    if exames_a_vencer:
        st.table(exames_a_vencer)
    else:
        st.info("Nenhum exame prestes a vencer.")

elif aba == "Registrar Exame Realizado":
    with st.expander("Cadastrar Exame Realizado"):
        st.header("📝 Cadastro de Exame Realizado") 

        funcionarios = funcionarioController.listar_funcionarios()
        funcionario_selecionado = st.selectbox(
            "Funcionário", 
            placeholder="Selecione o funcionário", 
            options=funcionarios, 
            format_func=lambda x: x['nome']
            )

        clinicas = clinicaController.listar_clinicas()
        clinica_responsavel = (
        st.selectbox(
            "Clínica Responsável",
            options=clinicas,
            format_func=lambda x: x["nome"],
        )
        if clinicas
        else None
        )

        exames_necessarios = cargoController.listar_exames_por_cargo(
            funcionario_selecionado['cargo_id']
            )
        exame_selecionado = st.selectbox(
            "Exame",
            index=None, 
            placeholder="Selecione o exame realizado", 
            options=exames_necessarios, 
            format_func=lambda x: x['exame_nome']
            )

        data_realizacao = st.date_input(
            "Data da realização", 
            datetime.today(), 
            format="DD/MM/YYYY"
            )

        if exame_selecionado:
            preco_exame = exameController.listar_preco_exame(
                exame_selecionado['exame_id'], 
                clinica_responsavel['id']
                )  
            if preco_exame:
                st.text_input(f"Valor do exame:", value=f"R$ {preco_exame:.2f}", disabled=True)

            recorrencia, data_proximo_exame = exameController.calcular_proximo_exame(
                funcionario_selecionado['cargo_id'], 
                exame_selecionado['exame_id'], 
                data_realizacao
                )
            st.selectbox(
                "Validade (meses):", 
                recorrencia, 
                disabled=True)
            st.date_input(
                "Próximo exame:", 
                data_proximo_exame, 
                format="DD/MM/YYYY", 
                disabled=True
                )

        if st.button("Cadastrar"):
            exameController.registrar_exame_realizado(
                funcionario_selecionado['id'], 
                exame_selecionado['exame_id'], 
                clinica_responsavel['id'],
                funcionario_selecionado['empresa_id'], 
                funcionario_selecionado['regional_id'],
                data_realizacao.strftime('%Y-%m-%d'), 
                data_proximo_exame.strftime('%Y-%m-%d'), 
                preco_exame
                )
            st.success("Exame registrado com sucesso!")

    with st.expander("Exames Realizados Pelo Funcionário"):
        st.header("📋 Exames Realizados")
        exames_realizados = exameController.listar_exames_realizados(
            funcionario_selecionado['id']
            )
        if exames_realizados:
            st.table(exames_realizados)
        else:
            st.info("Nenhum exame realizado por este funcionário.")