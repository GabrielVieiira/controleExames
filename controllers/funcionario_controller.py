from models.model import DatabaseManager

class FuncionarioManager(DatabaseManager):
    def adicionar_funcionario(self, nome, matricula, data_admissao, cargo_id, regional_id):
        nome = nome.strip().upper()
        primeira_query = "SELECT id FROM funcionarios WHERE nome = ? and matricula = ?"
        existe = self.fetch_one(primeira_query, (nome, matricula,))
        if existe:
            raise ValueError("Funcionário já cadastrado")
        segunda_query = "INSERT INTO funcionarios (nome, matricula, data_admissao, cargo_id, regional_id) VALUES (?, ?, ?, ?, ?)"
        self.execute_query(segunda_query,(nome, matricula, data_admissao, cargo_id, regional_id,))

    def listar_funcionarios(self):
        query = ''' 
                SELECT 
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
        return self.fetch_all(query)