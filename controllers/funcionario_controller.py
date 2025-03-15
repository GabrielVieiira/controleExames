from models.model import DatabaseManager

class FuncionarioManager(DatabaseManager):
    def cadastrar_funcionario(self, nome, cpf, data_nascimento, id_empresa, matricula, data_admissao, cargo_id, regional_id):
        nome = nome.strip().upper()
        primeira_query = "SELECT id FROM funcionarios WHERE nome = ? and matricula = ?"
        existe = self.fetch_one(primeira_query, (nome, matricula,))
        if existe:
            raise ValueError("Funcionário já cadastrado")
        segunda_query = "INSERT INTO funcionarios (nome, cpf, data_nascimento, id_empresa, matricula, data_admissao, cargo_id, regional_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.execute_query(segunda_query,(nome, cpf, data_nascimento, id_empresa, matricula, data_admissao, cargo_id, regional_id,))

    def listar_funcionarios(self):
        query = ''' 
                SELECT 
                    funcionarios.id,
                    funcionarios.matricula, 
                    funcionarios.nome, 
                    funcionarios.data_admissao, 
                    cargos.nome, 
                    regionais.nome,
                    funcionarios.cargo_id,
                    funcionarios.regional_id,
                    funcionarios.id_empresa
                FROM 
                    funcionarios 
                LEFT JOIN 
                    cargos ON funcionarios.cargo_id = cargos.id 
                LEFT JOIN 
                    regionais ON funcionarios.regional_id = regionais.id
                WHERE
                    funcionarios.ativo = True '''
        resposta =  self.fetch_all(query)
        return [{"id": r[0], "matricula": r[1], "nome": r[2], "data_admissao": r[3], "cargo_nome": r[4], "regional_nome": r[5], "cargo_id": r[6], "regional_id": r[7], "empresa_id": r[8] } for r in resposta]



    def validar_cpf(self, cpf_numeros):
        cpf = [int(char) for char in cpf_numeros if char.isdigit()]

        if len(cpf) != 11:
            return False

        if cpf == cpf[::-1]:
            return False

        for i in range(9, 11):
            value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                return False
        return True