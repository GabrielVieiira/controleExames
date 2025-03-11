import streamlit as st
import sqlite3
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_name="testSst.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=()):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_all(self, query, params=()):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

class ExameManager(DatabaseManager):
    def listar_exames_vencidos(self):
        return self.fetch_all("""
            SELECT funcionarios.nome, exames.nome, exames_realizados.data_realizacao, exames_realizados.validade
            FROM exames_realizados
            JOIN funcionarios ON exames_realizados.funcionario_id = funcionarios.id
            JOIN exames ON exames_realizados.exame_id = exames.id
            WHERE exames_realizados.validade < DATE('now')
        """)

    def listar_exames_a_vencer(self, dias=30):
        return self.fetch_all("""
            SELECT funcionarios.nome, exames.nome, exames_realizados.data_realizacao, exames_realizados.validade
            FROM exames_realizados
            JOIN funcionarios ON exames_realizados.funcionario_id = funcionarios.id
            JOIN exames ON exames_realizados.exame_id = exames.id
            WHERE exames_realizados.validade BETWEEN DATE('now') AND DATE('now', ? || ' days')
        """, (dias,))
    
    def registrar_exame_realizado(self, funcionario_id, exame_id, data_realizacao, validade):
        self.execute_query("""
            INSERT INTO exames_realizados (funcionario_id, exame_id, data_realizacao, validade)
            VALUES (?, ?, ?, ?)
        """, (funcionario_id, exame_id, data_realizacao, validade))

    def calcular_proximo_exame(self, funcionario_id, exame_id, data_realizacao):
        resultado = self.fetch_all("""
            SELECT recorrencia FROM exames_necessarios_por_cargo
            INNER JOIN funcionarios ON exames_necessarios_por_cargo.cargo_id = funcionarios.cargo_id
            WHERE funcionarios.id = ? AND exames_necessarios_por_cargo.exame_id = ?
        """, (funcionario_id, exame_id))
        if resultado:
            return resultado[0][0]
            # meses = resultado[0][0]
            # return data_realizacao + timedelta(days=meses * 30)
        return None

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