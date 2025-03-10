import streamlit as st
import sqlite3
from datetime import datetime

# Função para conectar ao banco de dados
def get_connection():
    return sqlite3.connect("testSst.db")

# Função para adicionar cargo
def adicionar_cargo(nome):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cargos (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

# Função para listar cargos
def listar_cargos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cargos")
    cargos = cursor.fetchall()
    conn.close()
    return cargos

# Função para adicionar regional
def adicionar_regional(nome):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO regionais (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

# Função para listar regionais
def listar_regionais():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM regionais")
    regionais = cursor.fetchall()
    conn.close()
    return regionais

# Função para adicionar funcionário
def adicionar_funcionario(nome, data_admissao, cargo_id, regional_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO funcionarios (nome, data_admissao, cargo_id, regional_id) VALUES (?, ?, ?, ?)",
        (nome, data_admissao, cargo_id, regional_id),
    )
    conn.commit()
    conn.close()

# Função para listar funcionários
def listar_funcionarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        ''' SELECT 
                funcionarios.id, 
                funcionarios.nome, 
                funcionarios.data_admissao, 
                cargos.nome, 
                regionais.nome 
            FROM 
                funcionarios 
            LEFT JOIN 
                cargos ON funcionarios.cargo_id = cargos.id 
            LEFT JOIN 
                regionais ON funcionarios.regional_id = regionais.id '''
    )
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

# Função para adicionar exame
def adicionar_exame(nome, preco):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO exames (nome, preco) VALUES (?, ?)", (nome, preco))
    conn.commit()
    conn.close()

# Função para listar exames
def listar_exames():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exames")
    exames = cursor.fetchall()
    conn.close()
    return exames

# Função para vincular exame a um cargo
def vincular_exame_cargo(cargo_id, exame_id, recorrencia):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO exames_necessarios_por_cargo (cargo_id, exame_id, recorrencia) VALUES (?, ?, ?)",
        (cargo_id, exame_id, recorrencia),
    )
    conn.commit()
    conn.close()

def desvincular_exame_cargo(exames_necessarios_por_cargo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM exames_necessarios_por_cargo WHERE id = ?",
        (exames_necessarios_por_cargo_id,),
    )
    conn.commit()
    conn.close()

def atualizar_preco_exame(exame_id, novo_preco):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE exames SET preco = ? WHERE id = ?", (novo_preco, exame_id))
    conn.commit()
    conn.close()

# Função para listar exames por cargo
def listar_exames_por_cargo(cargo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        ''' SELECT
                exames_necessarios_por_cargo.id, 
                exames.id, 
                exames.nome, 
                exames.preco, 
                exames_necessarios_por_cargo.recorrencia 
            FROM 
                exames 
            INNER JOIN 
                exames_necessarios_por_cargo ON exames.id = exames_necessarios_por_cargo.exame_id 
            WHERE 
                exames_necessarios_por_cargo.cargo_id = ? ''',
        (cargo_id,),
    )
    exames = cursor.fetchall()
    conn.close()
    return exames

tabela_recorrencia = {
    "Renovação 6 meses": 6,
    "Renovação 12 meses": 12,
    "Renovação 24 meses": 24,
    "Não se aplica": 0,
}

# Criando a interface do Streamlit
st.title("🏥 Gerenciamento de Exames Ocupacionais")

# Menu de navegação
aba = st.sidebar.radio(
    "Navegação",
    [
        "Gerenciar Cargos",
        "Gerenciar Regionais",
        "Gerenciar Funcionários",
        "Gerenciar Exames",
    ],
)

if aba == "Gerenciar Cargos":
    with st.expander("Cadastrar Cargos"):
        st.header("📌 Cadastro de Cargos")
        nome_cargo = st.text_input("Nome do Cargo")
        if st.button("Cadastrar Cargo"):
            adicionar_cargo(nome_cargo)
            st.success("Cargo cadastrado com sucesso!")

        st.subheader("📋 Lista de Cargos")
        cargos = listar_cargos()
        for cargo in cargos:
            st.write(f"{cargo[0]} - {cargo[1]}")

    with st.expander("Gerenciar Exames e Cargos"):
        st.header("🔗 Gerenciar Exames a Cargos")
        exames = listar_exames()
        cargo_id = (
            st.selectbox(
                "Cargo", options=[(c[0], c[1]) for c in cargos], format_func=lambda x: x[1]
            )
            if cargos
            else None
        )
        exame_id = (
            st.selectbox(
                "Exame", options=[(e[0], e[1]) for e in exames], format_func=lambda x: x[1]
            )
            if exames
            else None
        )
        recorrencia = st.selectbox("Recorrência", tabela_recorrencia.keys())
        if cargo_id:
            exames_cargo = listar_exames_por_cargo(cargo_id[0])
            st.subheader(f"📋 Exames para - {cargo_id[1]}")
            coluna_exame, coluna_preco, coluna_recorrencia, coluna_botao = st.columns([1, 1, 1, 1])
            with coluna_exame:
                st.write("Nome do Exame")
            with coluna_preco:
                st.write(f"Preço")
            with coluna_recorrencia:
                st.write(f"Recorrência")
            with coluna_botao:
                st.write("Ação")
            for exame in exames_cargo:
                with coluna_exame:
                    st.write(exame[2], key=f'{exame[0]}')
                with coluna_preco:
                    st.write(f"R${exame[3]:.2f}")
                with coluna_recorrencia:
                    st.write(f"{exame[4]} Meses")
                with coluna_botao:
                    if st.button("Desvincular", key=f'{exame[0]}'):
                        try:
                            desvincular_exame_cargo(exame[0])
                            st.success(f'exame {exame[2]} desvinculado')
                        except:
                            st.error("Erro ao desvincular exame")    
                        
        if st.button("Vincular Exame"):
            if cargo_id and exame_id:
                vincular_exame_cargo(
                    cargo_id[0], exame_id[0], tabela_recorrencia.get(recorrencia)
                )
                st.success("Exame vinculado com sucesso!")
            else:
                st.warning("Selecione um cargo e um exame para vincular.")

elif aba == "Gerenciar Regionais":
    with st.expander("Cadastrar Regional"):
        st.header("📌 Cadastro de Regionais")
        nome_regional = st.text_input("Nome da Regional")
        if st.button("Cadastrar Regional"):
            adicionar_regional(nome_regional)
            st.success("Regional cadastrada com sucesso!")
    with st.expander("Listar Regionais"):
        st.subheader("📋 Lista de Regionais")
        regionais = listar_regionais()
        for regional in regionais:
            st.write(f"{regional[0]} - {regional[1]}")

elif aba == "Gerenciar Funcionários":
    with st.expander("Cadastrar Funcionários"):
        st.header("👨‍💼 Cadastro de Funcionários")
        nome = st.text_input("Nome do Funcionário")
        data_admissao = st.date_input(
            "Data de Admissão", datetime.today(), format="DD/MM/YYYY"
        )
        cargos = listar_cargos()
        cargo_id = (
            st.selectbox(
                "Cargo", options=[(c[0], c[1]) for c in cargos], format_func=lambda x: x[1]
            )
            if cargos
            else None
        )
        regionais = listar_regionais()
        regional_id = (
            st.selectbox(
                "Regional",
                options=[(r[0], r[1]) for r in regionais],
                format_func=lambda x: x[1],
            )
            if regionais
            else None
        )
        if st.button("Cadastrar Funcionário"):
            if cargo_id and regional_id:
                adicionar_funcionario(
                    nome, data_admissao.strftime("%Y-%m-%d"), cargo_id[0], regional_id[0]
                )
                st.success("Funcionário cadastrado com sucesso!")
            else:
                st.warning(
                    "Cadastre um cargo e uma regional antes de adicionar funcionários."
                )
    with st.expander("Listar Funcionários"):
        st.subheader("📋 Lista de Funcionários")
        funcionarios = listar_funcionarios()
        for func in funcionarios:
            st.write(
                f"{func[0]} - {func[1]}, {func[2]}, Cargo: {func[3]}, Regional: {func[4]}"
            )

elif aba == "Gerenciar Exames":
    exames = listar_exames()
    with st.expander("Cadastrar Exames"):
        st.header("🩺 Cadastro de Exames")
        nome_exame = st.text_input("Nome do Exame")
        preco_exame = st.number_input("Preço do Exame", min_value=0.0, step=0.1)
        if st.button("Cadastrar Exame"):
            adicionar_exame(nome_exame, preco_exame)
            st.success("Exame cadastrado com sucesso!")

    with st.expander("Editar Exames"):
        st.header("🩺 Editar Exame")
        exame_id = (
            st.selectbox(
                "Selecione o Exame",
                options=[(e[0], e[1]) for e in exames],
                format_func=lambda x: x[1],
            )
            if exames
            else None
        )
        if exame_id:
            novo_preco = st.number_input("Novo Preço do Exame", min_value=0.0, step=0.1)
            if st.button("Atualizar Preço"):
                atualizar_preco_exame(exame_id[0], novo_preco)
                st.success("Preço atualizado com sucesso!")

    with st.expander("Listar Exames"):
        st.subheader("📋 Lista de Exames")
        for exame in exames:
            st.write(f"{exame[0]} - {exame[1]}, Preço: R${exame[2]:.2f}")

