import streamlit as st

from controllers.exames_controller import ExameManager
from controllers.cargo_controller import CargoManager
from controllers.funcionario_controller import FuncionarioManager
from controllers.regional_controller import RegionalManager

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
        cargoController = CargoManager()
        exameController = ExameManager()
        st.header("📌 Cadastro de Cargos")
        nome_cargo = st.text_input("Nome do Cargo")
        if st.button("Cadastrar Cargo"):
            if nome_cargo:
                try:
                    cargoController.adicionar_cargo(nome_cargo)
                    st.success("Cargo cadastrado com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Por favor, preencha o nome do cargo!")
    with st.expander("Cargos Cadastrados"):
        st.subheader("📋 Lista de Cargos")
        cargos = cargoController.listar_cargos()
        for cargo in cargos:
            st.write(f"{cargo[0]} - {cargo[1]}")

    with st.expander("Gerenciar Exames e Cargos"):
        st.header("🔗 Gerenciar Exames a Cargos")
        exames = exameController.listar_exames()
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
            exames_cargo = cargoController.listar_exames_por_cargo(cargo_id[0])
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
                            cargoController.desvincular_exame_cargo(exame[0])
                            st.success(f'exame {exame[2]} desvinculado')
                        except:
                            st.error("Erro ao desvincular exame")    
                        
        if st.button("Vincular Exame"):
            if cargo_id and exame_id:
                try:
                    cargoController.vincular_exame_cargo(
                        cargo_id[0], exame_id[0], tabela_recorrencia.get(recorrencia)
                    )
                    st.success("Exame vinculado com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Selecione um cargo e um exame para vincular.")

elif aba == "Gerenciar Regionais":
    with st.expander("Cadastrar Regional"):
        regionalController = RegionalManager()
        st.header("📌 Cadastro de Regionais")
        nome_regional = st.text_input("Nome da Regional")
        if st.button("Cadastrar Regional"):
            if nome_regional:
                try:
                    regionalController.adicionar_regional(nome_regional)
                    st.success("Regional cadastrada com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Por favor, preencha o nome da regional!")

    with st.expander("Regionais Cadastradas"):
        st.subheader("📋 Lista de Regionais")
        regionais = regionalController.listar_regionais()
        for regional in regionais:
            st.write(f"{regional[0]} - {regional[1]}")

elif aba == "Gerenciar Funcionários":
    with st.expander("Cadastrar Funcionários"):
        cargoController = CargoManager()
        regionalController = RegionalManager()
        FuncionarioController = FuncionarioManager()
        st.header("👨‍💼 Cadastro de Funcionários")
        with st.form(key='func_cadastro'):
            nome = st.text_input("Nome do Funcionário")
            matricula = st.number_input("Matrícula", format="%0.0f", value=None)
            data_admissao = st.date_input("Data de Admissão", value=None, format="DD/MM/YYYY")
            
            cargos = cargoController.listar_cargos()
            cargo_id = st.selectbox("Cargo", 
                                    options=cargos, 
                                    index=None, 
                                    format_func=lambda x: x[1], 
                                    placeholder="Selecione um cargo"
                                    )

            regionais = regionalController.listar_regionais()
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
                        FuncionarioController.adicionar_funcionario(
                            nome, matricula, data_admissao.strftime("%Y-%m-%d"), cargo_id[0], regional_id[0]
                        )
                        st.success("Funcionário cadastrado com sucesso!")
                    except ValueError as e:
                        st.error(str(e))
                else:
                    st.warning("Por favor, preencha todos os campos!")

    with st.expander("Funcionários Cadastrados"):
        st.subheader("📋 Lista de Funcionários")
        funcionarios = FuncionarioController.listar_funcionarios()
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
    exameController = ExameManager()
    exames = exameController.listar_exames()
    with st.expander("Cadastrar Exames"):
        exameController = ExameManager()
        st.header("🩺 Cadastro de Exames")
        nome_exame = st.text_input("Nome do Exame")
        preco_exame = st.number_input("Preço do Exame", min_value=0.0, step=0.1)
        if st.button("Cadastrar Exame"):
            if nome_exame and preco_exame:
                try:
                    exameController.adicionar_exame(nome_exame, preco_exame)
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
                options=exames,
                format_func=lambda x: x[1],
            )
            if exames
            else None
        )
        if exame_id:
            novo_preco = st.number_input("Novo Preço do Exame", min_value=0.0, step=0.1)
            if st.button("Atualizar Preço"):
                exameController.atualizar_preco_exame(exame_id[0], novo_preco)
                st.success("Preço atualizado com sucesso!")

    with st.expander("Exames Cadastrados"):
        st.subheader("📋 Lista de Exames")
        for exame in exames:
            st.write(f"{exame[0]} - {exame[1]}, Preço: R${exame[2]:.2f}")

