from models.model import DatabaseManager
from itertools import cycle

class EmpresasManager(DatabaseManager):
    def cadastrar_empresa(self, nome_empresa, cnpj, rua, numero, bairro, municipio, cep, estado, telefone, email):
        nome = nome_empresa.strip().upper()
        primeira_query = "SELECT id FROM empresas WHERE nome = ?"
        existe = self.fetch_one(primeira_query, (nome,))
        if existe:
            raise ValueError("Regional já cadastrada")
        segunda_query = "INSERT INTO empresas (nome, cnpj) VALUES (?, ?)"
        self.execute_query(segunda_query, (nome, cnpj,))

    def listar_empresas(self):
        query = "SELECT * FROM empresas"
        resposta = self.fetch_all(query)
        return [{"id": r[0], "nome": r[1], "cnpj": r[2]} for r in resposta]

    def validar_cnpj(self, cnpj_numeros: str) -> bool:
        # Implementar essa porra
        # Quando implementar, alterar a verificação se ja esta cadastrado para verificar o cnpj
        return True