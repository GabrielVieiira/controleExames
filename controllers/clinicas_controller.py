from models.model import DatabaseManager

class ClinicasManager(DatabaseManager):
    def cadastrar_clinicas(self, nome):
        nome = nome.strip().upper()
        primeira_query = "SELECT id FROM clinicas WHERE nome = ?"
        existe = self.fetch_one(primeira_query, (nome,))
        if existe:
            raise ValueError("Clinica já cadastrada")
        segunda_query = "INSERT INTO clinicas (nome) VALUES (?)"
        self.execute_query(segunda_query, (nome,))

    def listar_clinicas(self):
        query = "SELECT * FROM clinicas"
        resposta = self.fetch_all(query)
        return [{"id": r[0], "nome": r[1], "ativo": "Ativo" if r[2] == True else "Desativada"} for r in resposta]

    def vincular_exame_clinica(self, exame_id, clinica_id, preco):
        primeira_query = "SELECT id FROM exames_por_clinica WHERE exame_id = ? and clinica_id = ?"
        vinculado = self.fetch_one(primeira_query, (exame_id,clinica_id,))
        if vinculado:
            raise ValueError("Exame já vinculado a esta clinica")
        segunda_query = "INSERT INTO exames_por_clinica (clinica_id, exame_id, preco) VALUES (?, ?, ?)"
        self.execute_query(segunda_query, (clinica_id, exame_id, preco))