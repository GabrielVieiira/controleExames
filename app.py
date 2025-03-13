import streamlit as st

from controllers.exames_controller import ExameManager
from controllers.cargo_controller import CargoManager
from controllers.funcionario_controller import FuncionarioManager
from controllers.regional_controller import RegionalManager
from controllers.clinicas_controller import ClinicasManager
from controllers.empresas_controller import EmpresasManager

exameController = ExameManager()
cargoController = CargoManager()
FuncionarioController = FuncionarioManager()
regionalController = RegionalManager()
clinicaController = ClinicasManager()
empresasController = EmpresasManager()

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
        "Gerenciar Clínicas",
        "Gerenciar Empresas",
    ],
)

if aba == "Gerenciar Cargos":
    with st.expander("Cadastrar Cargos"):
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
            st.write(f"{cargo['id']} - {cargo['nome']}")

    with st.expander("Gerenciar Exames e Cargos"):
        st.header("🔗 Gerenciar Exames a Cargos")
        exames = exameController.listar_exames()
        cargo_selecionado = (
            st.selectbox(
                "Cargo",
                index=None,
                placeholder="Selecione o cargo",
                options=cargos,
                format_func=lambda x: x["nome"],
            )
            if cargos
            else None
        )
        exame_selecionado = (
            st.selectbox(
                "Exame",
                index=None,
                placeholder="Selecione o exame",
                options=exames,
                format_func=lambda x: x["nome"],
            )
            if exames
            else None
        )
        recorrencia = st.selectbox("Recorrência", tabela_recorrencia.keys())

        if cargo_selecionado:
            exames_cargo = cargoController.listar_exames_por_cargo(
                cargo_selecionado["id"]
            )
            st.subheader(f"📋 Exames para - {cargo_selecionado['nome']}")
            coluna_exame, coluna_recorrencia, coluna_botao = st.columns([1, 1, 1])
            with coluna_exame:
                st.write("Nome do Exame")
            with coluna_recorrencia:
                st.write(f"Recorrência")
            with coluna_botao:
                st.write("Ação")
            for exame_vinculado in exames_cargo:
                with coluna_exame:
                    st.write(exame_vinculado["exame_nome"])
                with coluna_recorrencia:
                    st.write(f"{exame_vinculado['recorrencia']} Meses")
                with coluna_botao:
                    if st.button("Desvincular", key=f"{exame_vinculado['id']}"):
                        try:
                            cargoController.desvincular_exame(exame_vinculado["id"])
                            st.success(
                                f"exame {exame_vinculado['exame_nome']} desvinculado"
                            )
                        except ValueError as e:
                            st.error(str(e))

        if st.button("Vincular Exame"):
            if cargo_selecionado and exame_selecionado:
                try:
                    cargoController.vincular_exame_cargo(
                        cargo_selecionado["id"],
                        exame_selecionado["id"],
                        tabela_recorrencia.get(recorrencia),
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
            st.write(f"{regional['id']} - {regional['nome']}")

elif aba == "Gerenciar Funcionários":
    with st.expander("Cadastrar Funcionários"):
        st.header("👨‍💼 Cadastro de Funcionários")
        with st.form(key="func_cadastro"):
            nome = st.text_input("Nome do Funcionário")
            cpf = st.number_input(
                "CPF", 
                format="%0.0f", 
                value=None
            )
            data_nascimento = st.date_input(
                "Data de Nascimento", value=None, format="DD/MM/YYYY"
            )
            matricula = st.number_input(
                "Matrícula", 
                format="%0.0f", 
                value=None
            )
            data_admissao = st.date_input(
                "Data de Admissão", 
                value=None, 
                format="DD/MM/YYYY"
            )

            cargos = cargoController.listar_cargos()
            cargo_selecionado = st.selectbox(
                "Cargo",
                options=cargos,
                index=None,
                format_func=lambda x: x["nome"],
                placeholder="Selecione um cargo",
            )

            regionais = regionalController.listar_regionais()
            regional_selecionada = st.selectbox(
                "Regional",
                options=regionais,
                index=None,
                format_func=lambda x: x["nome"],
                placeholder="Selecione uma regional",
            )
            empresas = empresaController.listar_empresas()
            empresa_selecionada = st.selectbox(
                "Empresa",
                options=empresas,
                index=None,
                format_func=lambda x: x["nome"],
                placeholder="Selecione uma empresa",
            )

            if st.form_submit_button("Cadastrar Funcionário"):
                if (
                    nome
                    and FuncionarioController.validar_cpf(str(cpf))
                    and data_nascimento
                    and matricula
                    and data_admissao
                    and cargo_selecionado
                    and regional_selecionada
                    and empresa_selecionada
                ):
                    try:
                        FuncionarioController.cadastrar_funcionario(
                            nome,
                            cpf,
                            data_nascimento.strftime("%Y-%m-%d"),
                            empresa_selecionada["id"],
                            matricula,
                            data_admissao.strftime("%Y-%m-%d"),
                            cargo_selecionado["id"],
                            regional_selecionada["id"],
                        )
                        st.success("Funcionário cadastrado com sucesso!")
                    except ValueError as e:
                        st.error(str(e))
                else:
                    st.warning("Por favor, verifique os campos!")

    with st.expander("Funcionários Cadastrados"):
        st.subheader("📋 Lista de Funcionários")
        funcionarios = FuncionarioController.listar_funcionarios()
        for func in funcionarios:
            st.write(
                f" - Matricula: {func['matricula']} - {func['nome']}, {func['data_admissao']}, Cargo: {func['cargo_nome']}, Regional: {func['regional']}"
            )

elif aba == "Gerenciar Exames":
    with st.expander("Cadastrar Exames"):
        exames = exameController.listar_exames()
        st.header("🩺 Cadastro de Exames")
        nome_exame = st.text_input("Nome do Exame")
        if st.button("Cadastrar Exame"):
            if nome_exame:
                try:
                    exameController.adicionar_exame(nome_exame)
                    st.success("Exame cadastrado com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Por favor, preencha o nome e o preço do exame!")

    with st.expander("Exames Cadastrados"):
        st.subheader("📋 Lista de Exames")
        for exame in exames:
            st.write(
                f"ID: {exame['id']} | Nome: {exame['nome']} | Situação: {exame['ativo']}"
            )

elif aba == "Gerenciar Clínicas":
    with st.expander("Cadastrar Clínicas"):
        clinicas = clinicaController.listar_clinicas()
        st.header("🏥 Cadastro de Clínicas")
        nome_nova_clinica = st.text_input("Nome da Clínica")
        if st.button("Cadastrar Clínica"):
            if nome_nova_clinica:
                try:
                    clinicaController.cadastrar_clinicas(nome_nova_clinica)
                    st.success("Clínica cadastrada com sucesso!")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Por favor, preencha o nome da clínica!")

    with st.expander("Vincular Exames"):
        exameController = ExameManager()
        exames = exameController.listar_exames()
        st.header("🩺 Vincular Exame")
        clinica_selecionada = (
            st.selectbox(
                "Selecione a Clínica",
                options=clinicas,
                format_func=lambda x: x["nome"],
            )
            if clinicas
            else None
        )

        exame_selecionado = (
            st.selectbox(
                "Selecione o Exame",
                options=exames,
                format_func=lambda x: x["nome"],
            )
            if exames
            else None
        )
        if exame_selecionado and clinica_selecionada:
            preco = st.number_input(
                "Preço do Exame", 
                min_value=0.0, 
                step=0.1
            )
            if st.button("Vincular Exame"):
                try:
                    clinicaController.vincular_exame_clinica(
                        exame_selecionado["id"], 
                        clinica_selecionada["id"], 
                        preco
                    )
                    st.success("Exame vinculado com sucesso!")
                except ValueError as e:
                    st.error(str(e))

    for clinica in clinicas:
        with st.expander(f"🏥 {clinica['nome']} - {clinica['ativo']}"):
            exames_clinica = clinicaController.listar_exames_por_clinica(clinica["id"])
            if exames_clinica:
                for exame in exames_clinica:
                    st.write(
                        f"🆔 **ID:** {exame['id']} | 📌 **Nome:** {exame['nome']} | 💰 **Preço:** R${exame['preco']:.2f}"
                    )
            else:
                st.write("⚠️ Nenhum exame vinculado.")

elif aba == "Gerenciar Empresas":
    with st.expander("Cadastrar Empresa"):
        with st.form(key="cadastro_empresa"):
            st.header("📌 Cadastro de Empresas")
            nome_empresa = st.text_input("Nome da Empresa")
            cnpj = st.number_input(
                "CNPJ", 
                min_value=0, 
                step=1, 
                format="%d", 
                value=None
            )
            rua = st.text_input("Rua")
            numero = st.number_input(
                "Número", 
                min_value=0, 
                step=1, 
                format="%d", 
                value=None
            )
            bairro = st.text_input("Bairro")
            municipio = st.text_input("Município")
            cep = st.number_input(
                "CEP", 
                min_value=0, 
                step=1, 
                format="%d", 
                value=None
            )
            uf = st.text_input("UF")
            telefone = st.number_input(
                "TELEFONE", 
                min_value=0, 
                step=1, 
                format="%d", 
                value=None
            )
            email = st.text_input("E-MAIL")

            if st.form_submit_button("Cadastrar empresa"):
                if nome_empresa and empresasController.validar_cnpj(str(cnpj)):
                    try:
                        empresasController.cadastrar_empresa(
                            nome_empresa,
                            cnpj,
                            rua,
                            numero,
                            bairro,
                            municipio,
                            cep,
                            estado,
                            telefone,
                            email,
                        )
                        st.success("Empresa cadastrada com sucesso!")
                    except ValueError as e:
                        st.error(str(e))
                else:
                    st.warning("Por favor, preencha oos campos necessários!")

    with st.expander("Empresas Cadastradas"):
        st.subheader("📋 Lista de Empresas")
        empresas = empresasController.listar_empresas()
        for empresa in empresas:
            st.write(f"{empresa['id']} - {empresa['nome']} - {empresa['cnpj']}")
