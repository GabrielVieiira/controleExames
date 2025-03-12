from models.model import DatabaseManager

class CargoManager(DatabaseManager):
    def adicionar_cargo(self,nome):
        nome = nome.strip().upper()
        primeira_query = "SELECT id FROM cargos WHERE nome = ?"
        existe = self.fetch_one(primeira_query, (nome,))
        if existe:
            raise ValueError("Cargo já cadastrado")
        segunda_query = "INSERT INTO cargos (nome) VALUES (?)"
        self.execute_query(segunda_query, (nome,))

    def listar_cargos(self):
        query = "SELECT * FROM cargos"
        return self.fetch_all(query)
    
    def vincular_exame_cargo(self, cargo_id, exame_id, recorrencia):
        primeira_query = "SELECT id FROM exames_necessarios_por_cargo WHERE cargo_id = ? and exame_id = ?"
        vinculado = self.fetch_one(primeira_query, (cargo_id,exame_id,))
        if vinculado:
            raise ValueError("Exame já vinculado a este cargo")
        segunda_query = "INSERT INTO exames_necessarios_por_cargo (cargo_id, exame_id, recorrencia) VALUES (?, ?, ?)"
        self.execute_query(segunda_query, (cargo_id, exame_id, recorrencia))

    def desvincular_exame_cargo(self, exames_necessarios_por_cargo_id):
        query = "DELETE FROM exames_necessarios_por_cargo WHERE id = ?"
        self.execute_query(query, (exames_necessarios_por_cargo_id,))

    def listar_exames_por_cargo(self, cargo_id):
        query = ''' 
                SELECT
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
                    exames_necessarios_por_cargo.cargo_id = ? '''
        return self.fetch_all(query, (cargo_id,))