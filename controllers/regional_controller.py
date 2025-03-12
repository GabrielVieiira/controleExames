from models.model import DatabaseManager

class RegionalManager(DatabaseManager):
    def adicionar_regional(self, nome):
        nome = nome.strip().upper()
        primeira_query = "SELECT id FROM regionais WHERE nome = ?"
        existe = self.fetch_one(primeira_query, (nome,))
        if existe:
            raise ValueError("Regional já cadastrada")
        segunda_query = "INSERT INTO regionais (nome) VALUES (?)"
        self.execute_query(segunda_query, (nome,))

    def listar_regionais(self):
        query = "SELECT * FROM regionais"
        return self.fetch_all(query)