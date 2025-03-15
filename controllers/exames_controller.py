from models.model import DatabaseManager
from datetime import timedelta, datetime

class ExameManager(DatabaseManager):
    def _formatar_data(self, data):
        return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
    
    def _formatar_valor(self, valor):
        return f"R$ {valor:.2f}"

    def listar_exames_vencidos(self):
        query = """
            SELECT 
                funcionarios.nome, 
                exames.nome, 
                exames_realizados.data_realizacao, 
                exames_realizados.validade
            FROM 
                exames_realizados
            JOIN 
                funcionarios ON exames_realizados.funcionario_id = funcionarios.id
            JOIN 
                exames ON exames_realizados.exame_id = exames.id
            WHERE 
                exames_realizados.validade < DATE('now')
        """
        resposta = self.fetch_all(query)
        return [{"Funcionário": r[0], "Exame": r[1], "Data de realização": self._formatar_data(r[2]), "Data do próximo exame": self._formatar_data(r[3])} for r in resposta]

    def listar_exames_a_vencer(self, dias=30):
        query = """
            SELECT 
                funcionarios.nome, 
                exames.nome, 
                exames_realizados.data_realizacao, 
                exames_realizados.validade
            FROM 
                exames_realizados
            JOIN 
                funcionarios ON exames_realizados.funcionario_id = funcionarios.id
            JOIN 
                exames ON exames_realizados.exame_id = exames.id
            WHERE 
                exames_realizados.validade BETWEEN DATE('now') AND DATE('now', ? || ' days')
        """
        resposta = self.fetch_all(query, (dias,))
        return [{"Funcionário": r[0], "Exame": r[1], "Data de realização": self._formatar_data(r[2]), "Data do próximo exame": self._formatar_data(r[3])} for r in resposta]
    
    def registrar_exame_realizado(self, funcionario_id, exame_id, clinica_id, empresa_id, regional_id, data_realizacao, validade, valor_pago):
        query = """
            INSERT INTO 
                exames_realizados(
                    funcionario_id, 
                    exame_id, clinica_id, 
                    empresa_id, regional_id, 
                    data_realizacao, validade, 
                    valor_pago
                    )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (funcionario_id, exame_id, clinica_id, empresa_id, regional_id, data_realizacao, validade, valor_pago))

    def listar_exames_realizados (self, funcionario_id):
        query = """
            SELECT 
                exames.nome,
                exames_realizados.data_realizacao,
                exames_realizados.validade,
                exames_realizados.valor_pago
            FROM 
                exames_realizados
            JOIN 
                exames ON exames_realizados.exame_id = exames.id
            WHERE 
                exames_realizados.funcionario_id = ?
        """
        resposta = self.fetch_all(query, (funcionario_id,))
        return [{"Exame": r[0], "Data de realização": self._formatar_data(r[1]), "Data do próximo exame": self._formatar_data(r[2]), "Valor": self._formatar_valor(r[3])} for r in resposta]   

    def calcular_proximo_exame(self, cargo_id, exame_id, data_realizacao):
        query = """
            SELECT 
                recorrencia 
            FROM 
                exames_necessarios_por_cargo
            WHERE 
                exames_necessarios_por_cargo.cargo_id = ? AND exames_necessarios_por_cargo.exame_id = ?
        """
        resultado = self.fetch_all(query, (cargo_id, exame_id))
        if resultado:
            recorrencia = resultado[0][0]
            data_proximo_exame = data_realizacao + timedelta(days=recorrencia * 30)
            return (recorrencia, data_proximo_exame)
        return None

    def adicionar_exame(self, nome):
        nome = nome.strip().upper()
        primeia_query = "SELECT id FROM exames WHERE nome = ?"
        existe = self.fetch_one(primeia_query, (nome,))
        if existe:
            raise ValueError("Exame já cadastrado")
        segunda_query = "INSERT INTO exames (nome) VALUES (?)"        
        self.execute_query(segunda_query, (nome,))

    def listar_exames(self):
        query = "SELECT * FROM exames"
        resposta = self.fetch_all(query)
        return [{"id": r[0], "nome": r[1], "ativo": "Ativo" if r[2] == True else "Desativado"} for r in resposta]

    def atualizar_preco_exame(self, exame_id, novo_preco):
        query = "UPDATE exames SET preco = ? WHERE id = ?"
        self.execute_query(query,(novo_preco, exame_id))

    def listar_preco_exame(self, exame_id, clinica_id):
        query = "SELECT preco FROM exames_por_clinica WHERE exame_id = ? and clinica_id = ?"
        resposta = self.fetch_one(query, (exame_id,clinica_id))
        if resposta:
            preco = resposta[0]
            return preco
        else:
            return None