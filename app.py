import streamlit as st
import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect("testSst.db")

def adicionar_cargo(nome):
    nome = nome.strip().upper()
    conn = get_connection()
    cursor = conn.cursor()
    existe = cursor.execute("SELECT id FROM cargos WHERE nome = ?", (nome,)).fetchone()
    if existe:
        raise ValueError("Cargo já cadastrado")
    cursor.execute("INSERT INTO cargos (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def listar_cargos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cargos")
    cargos = cursor.fetchall()
    conn.close()
    return cargos

def adicionar_regional(nome):
    nome = nome.strip().upper()
    conn = get_connection()
    cursor = conn.cursor()
    existe = cursor.execute("SELECT id FROM regionais WHERE nome = ?", (nome,)).fetchone()
    if existe:
        raise ValueError("Regional já cadastrada")
    cursor.execute("INSERT INTO regionais (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def listar_regionais():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM regionais")
    regionais = cursor.fetchall()
    conn.close()
    return regionais

def adicionar_funcionario(nome, matricula, data_admissao, cargo_id, regional_id):
    nome = nome.strip().upper()
    conn = get_connection()
    cursor = conn.cursor()
    existe = cursor.execute("SELECT id FROM funcionarios WHERE nome = ? and matricula = ?", (nome, matricula,)).fetchone()
    if existe:
        raise ValueError("Funcionário já cadastrado")
    print(existe)
    print(nome, matricula, data_admissao, cargo_id, regional_id)
    cursor.execute(
        "INSERT INTO funcionarios (nome, matricula, data_admissao, cargo_id, regional_id) VALUES (?, ?, ?, ?, ?)",
        (nome, matricula, data_admissao, cargo_id, regional_id,),
    )
    conn.commit()
    conn.close()

def listar_funcionarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        ''' SELECT 
                funcionarios.id,
                funcionarios.matricula, 
                funcionarios.nome, 
                funcionarios.data_admissao, 
                cargos.nome, 
                regionais.nome 
            FROM 
                funcionarios 
            LEFT JOIN 
                cargos ON funcionarios.cargo_id = cargos.id 
            LEFT JOIN 
                regionais ON funcionarios.regional_id = regionais.id
            WHERE
                funcionarios.ativo = True '''
    )
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

def adicionar_exame(nome, preco):
    nome = nome.strip().upper()
    conn = get_connection()
    cursor = conn.cursor()
    existe = cursor.execute("SELECT id FROM exames WHERE nome = ?", (nome,)).fetchone()
    if existe:
        raise ValueError("Exame já cadastrado")
    cursor.execute("INSERT INTO exames (nome, preco) VALUES (?, ?)", (nome, preco))
    conn.commit()
    conn.close()

def listar_exames():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exames")
    exames = cursor.fetchall()
    conn.close()
    return exames

def vincular_exame_cargo(cargo_id, exame_id, recorrencia):
    conn = get_connection()
    cursor = conn.cursor()
    vinculado = cursor.execute("SELECT id FROM exames_necessarios_por_cargo WHERE cargo_id = ? and exame_id = ?", (cargo_id,exame_id,)).fetchone()
    if vinculado:
        raise ValueError("Exame já vinculado a este cargo")
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

st.title("🏥 Gerenciamento de Exames Ocupacionais")

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
            if nome_cargo:
                try:
                    adicionar_cargo(nome_cargo)
                    st.success("Cargo cadastrado com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Por favor, preencha o nome do cargo!")
    with st.expander("Cargos Cadastrados"):
        st.subheader("📋 Lista de Cargos")
        cargos = listar_cargos()
        for cargo in cargos:
            st.write(f"{cargo[0]} - {cargo[1]}")

    with st.expander("Gerenciar Exames e Cargos"):
        st.header("🔗 Gerenciar Exames a Cargos")
        exames = listar_exames()
        cargo_id = (
            st.selectbox(
                "Cargo",index=None,placeholder="Selecione o cargo", options=cargos, format_func=lambda x: x[1]
            )
            if cargos
            else None
        )
        exame_id = (
            st.selectbox(
                "Exame", index=None, placeholder="Selecione o exame", options=exames, format_func=lambda x: x[1]
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
                try:
                    vincular_exame_cargo(
                        cargo_id[0], exame_id[0], tabela_recorrencia.get(recorrencia)
                    )
                    st.success("Exame vinculado com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Selecione um cargo e um exame para vincular.")

elif aba == "Gerenciar Regionais":
    with st.expander("Cadastrar Regional"):
        st.header("📌 Cadastro de Regionais")
        nome_regional = st.text_input("Nome da Regional")
        if st.button("Cadastrar Regional"):
            if nome_regional:
                try:
                    adicionar_regional(nome_regional)
                    st.success("Regional cadastrada com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Por favor, preencha o nome da regional!")

    with st.expander("Regionais Cadastradas"):
        st.subheader("📋 Lista de Regionais")
        regionais = listar_regionais()
        for regional in regionais:
            st.write(f"{regional[0]} - {regional[1]}")

elif aba == "Gerenciar Funcionários":
    with st.expander("Cadastrar Funcionários"):
        st.header("👨‍💼 Cadastro de Funcionários")
        with st.form(key='func_cadastro'):
            nome = st.text_input("Nome do Funcionário")
            matricula = st.number_input("Matrícula", format="%0.0f", value=None)
            data_admissao = st.date_input("Data de Admissão", value=None, format="DD/MM/YYYY")
            
            cargos = listar_cargos()
            cargo_id = st.selectbox("Cargo", 
                                    options=cargos, 
                                    index=None, 
                                    format_func=lambda x: x[1], 
                                    placeholder="Selecione um cargo"
                                    )

            regionais = listar_regionais()
            regional_id = st.selectbox("Regional", 
                                        options=regionais, 
                                        index=None, 
                                        format_func=lambda x: x[1], 
                                        placeholder="Selecione uma regional"
                                        )

            submit_button = st.form_submit_button("Cadastrar Funcionário")

            if submit_button:
                if nome and matricula and data_admissao and cargo_id and regional_id:
                    try:
                        adicionar_funcionario(
                            nome, matricula, data_admissao.strftime("%Y-%m-%d"), cargo_id[0], regional_id[0]
                        )
                        st.success("Funcionário cadastrado com sucesso!")
                    except ValueError as e:
                        st.error(str(e))
                else:
                    st.warning("Por favor, preencha todos os campos!")

    with st.expander("Funcionários Cadastrados"):
        st.subheader("📋 Lista de Funcionários")
        funcionarios = listar_funcionarios()
        for func in funcionarios:
            func_matricula = func[1]
            func_nome = func[2]
            func_data_admissao = func[3]
            func_cargo = func[4]
            func_regional = func[5]
            st.write(
                f" - Matricula: {func_matricula} - {func_nome}, {func_data_admissao}, Cargo: {func_cargo}, Regional: {func_regional}"
            )

elif aba == "Gerenciar Exames":
    exames = listar_exames()
    with st.expander("Cadastrar Exames"):
        st.header("🩺 Cadastro de Exames")
        nome_exame = st.text_input("Nome do Exame")
        preco_exame = st.number_input("Preço do Exame", min_value=0.0, step=0.1)
        if st.button("Cadastrar Exame"):
            if nome_exame and preco_exame:
                try:
                    adicionar_exame(nome_exame, preco_exame)
                    st.success("Exame cadastrado com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Por favor, preencha o nome e o preço do exame!")

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

    with st.expander("Exames Cadastrados"):
        st.subheader("📋 Lista de Exames")
        for exame in exames:
            st.write(f"{exame[0]} - {exame[1]}, Preço: R${exame[2]:.2f}")

