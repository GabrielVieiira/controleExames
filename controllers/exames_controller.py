from models.model import DatabaseManager

class ExameManager(DatabaseManager):
    def listar_exames_vencidos(self):
        return self.fetch_all("""
            SELECT funcionarios.nome, exames.nome, exames_realizados.data_realizacao, exames_realizados.validade
            FROM exames_realizados
            JOIN funcionarios ON exames_realizados.funcionario_id = funcionarios.id
            JOIN exames ON exames_realizados.exame_id = exames.id
            WHERE exames_realizados.validade < DATE('now')
        """)

    def listar_exames_a_vencer(self, dias=30):
        return self.fetch_all("""
            SELECT funcionarios.nome, exames.nome, exames_realizados.data_realizacao, exames_realizados.validade
            FROM exames_realizados
            JOIN funcionarios ON exames_realizados.funcionario_id = funcionarios.id
            JOIN exames ON exames_realizados.exame_id = exames.id
            WHERE exames_realizados.validade BETWEEN DATE('now') AND DATE('now', ? || ' days')
        """, (dias,))
    
    def registrar_exame_realizado(self, funcionario_id, exame_id, clinica_id, empresa_id, regional_id, data_realizacao, validade, valor_pago):
        query = """
            INSERT INTO exames_realizados (funcionario_id, exame_id, clinica_id, empresa_id, regional_id, data_realizacao, validade, valor_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (funcionario_id, exame_id, clinica_id, empresa_id, regional_id, data_realizacao, validade, valor_pago))

    def calcular_proximo_exame(self, cargo_id, exame_id, data_realizacao):
        query = """
            SELECT recorrencia FROM exames_necessarios_por_cargo
            WHERE exames_necessarios_por_cargo.cargo_id = ? AND exames_necessarios_por_cargo.exame_id = ?
        """
        resultado = self.fetch_all(query, (cargo_id, exame_id))
        if resultado:
            return resultado[0][0]
            # meses = resultado[0][0]
            # return data_realizacao + timedelta(days=meses * 30)
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