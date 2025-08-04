"""
Módulo para interface de usuário da aplicação.
...
"""

import logging
from datetime import datetime
from typing import Tuple, Optional, List, Dict, Any

# ... (outros métodos da classe continuam iguais) ...

class InterfaceUsuario:
    # ... (exibir_cabecalho, validar_data, etc. continuam aqui) ...
    @staticmethod
    def exibir_cabecalho():
        """
        Exibe o cabeçalho da aplicação.
        """
        print("=" * 70)
        print("    APLICAÇÃO PARA AUTOMAÇÃO DE ORDENS DE PRODUÇÃO")
        print("                    Sistema Sankhya")
        print("=" * 70)
        print()
    
    @staticmethod
    def validar_data(data_str: str) -> bool:
        """
        Valida se a string de data está no formato DD/MM/YYYY.
        
        Args:
            data_str (str): String da data a ser validada
            
        Returns:
            bool: True se a data é válida, False caso contrário
        """
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_numero_positivo(numero_str: str) -> bool:
        """
        Valida se a string representa um número positivo.
        
        Args:
            numero_str (str): String do número a ser validada
            
        Returns:
            bool: True se é um número positivo, False caso contrário
        """
        try:
            numero = int(numero_str)
            return numero > 0
        except ValueError:
            return False
    
    @staticmethod
    def solicitar_data_planejamento() -> str:
        """
        Solicita ao usuário a data do planejamento.
        
        Returns:
            str: Data do planejamento no formato DD/MM/YYYY
        """
        while True:
            print("📅 Data do Planejamento:")
            print("   Digite a data específica para a qual a produção será programada.")
            print("   Formato: DD/MM/YYYY (ex: 21/07/2025)")
            print()
            
            data = input("   Data: ").strip()
            
            if InterfaceUsuario.validar_data(data):
                return data
            else:
                print("   ❌ Data inválida! Use o formato DD/MM/YYYY.")
                print()
    
    @staticmethod
    def solicitar_braco_producao() -> int:
        """
        Solicita ao usuário o número do braço de produção.
        
        Returns:
            int: Número do braço de produção
        """
        while True:
            print("🏭 Braço de Produção:")
            print("   Digite o número do braço que será programado.")
            print("   Exemplo: 1, 2, 3, etc.")
            print()
            
            braco = input("   Braço: ").strip()
            
            if InterfaceUsuario.validar_numero_positivo(braco):
                return int(braco)
            else:
                print("   ❌ Número inválido! Digite um número positivo.")
                print()
    
    @staticmethod
    def solicitar_range_rodadas() -> Tuple[int, int]:
        """
        Solicita ao usuário o range de rodadas a serem processadas.
        
        Returns:
            Tuple[int, int]: (rodada_inicial, rodada_final)
        """
        while True:
            print("🔄 Range de Rodadas:")
            print("   Digite a rodada inicial e final a serem processadas.")
            print("   Exemplo: rodada inicial = 1, rodada final = 5")
            print()
            
            rodada_inicial = input("   Rodada inicial: ").strip()
            
            if not InterfaceUsuario.validar_numero_positivo(rodada_inicial):
                print("   ❌ Rodada inicial inválida! Digite um número positivo.")
                print()
                continue
            
            rodada_final = input("   Rodada final: ").strip()
            
            if not InterfaceUsuario.validar_numero_positivo(rodada_final):
                print("   ❌ Rodada final inválida! Digite um número positivo.")
                print()
                continue
            
            rodada_inicial_int = int(rodada_inicial)
            rodada_final_int = int(rodada_final)
            
            if rodada_inicial_int <= rodada_final_int:
                return rodada_inicial_int, rodada_final_int
            else:
                print("   ❌ A rodada inicial deve ser menor ou igual à rodada final.")
                print()

    @staticmethod
    def coletar_parametros() -> Optional[Tuple[str, int, int, int]]:
        """
        Coleta todos os parâmetros necessários do usuário.
        """
        InterfaceUsuario.exibir_cabecalho()
        
        data_planejamento = InterfaceUsuario.solicitar_data_planejamento()
        print()
        braco = InterfaceUsuario.solicitar_braco_producao()
        print()
        rodada_inicial, rodada_final = InterfaceUsuario.solicitar_range_rodadas()
        print()
        
        print("📋 Resumo dos Parâmetros:")
        print(f"   Data do Planejamento: {data_planejamento}")
        print(f"   Braço de Produção: {braco}")
        print(f"   Range de Rodadas: {rodada_inicial} a {rodada_final}")
        print()
        
        confirmacao = input("   Confirma os parâmetros? (s/n): ").strip().lower()
        
        if confirmacao in ['s', 'sim', 'y', 'yes']:
            return data_planejamento, braco, rodada_inicial, rodada_final
        else:
            print("   Operação cancelada pelo usuário.")
            return None # Retorna None se o usuário cancelar

    @staticmethod
    def exibir_progresso(mensagem: str, tipo: str = "info"):
        """Exibe mensagem de progresso formatada."""
        icones = {"info": "ℹ️", "sucesso": "✅", "erro": "❌", "aviso": "⚠️"}
        icone = icones.get(tipo, "ℹ️")
        print(f"{icone} {mensagem}")
    
    # --- MÉTODO ATUALIZADO ---
    @staticmethod
    def exibir_resumo_final(total_ops_criadas: int, total_falhas: int, 
                          ops_sucesso: List[Dict[str, Any]],
                          detalhes_falhas: List[Dict[str, Any]]):
        """
        Exibe o resumo final da execução, incluindo listas de sucesso e falha.
        """
        print()
        print("=" * 70)
        print("                    RESUMO FINAL DA EXECUÇÃO")
        print("=" * 70)
        print(f"✅ Total de Ordens de Produção criadas: {total_ops_criadas}")
        print(f"❌ Total de falhas no processamento: {total_falhas}")
        print()

        # Mostra a lista de OPs criadas com sucesso
        if ops_sucesso:
            print("--- Ordens de Produção Criadas com Sucesso ---")
            print(f"{'NUPLAN':<15} | {'Ordem de Produção (IDIPROC)':<30}")
            print("-" * 50)
            for item in ops_sucesso:
                print(f"{item['nuplan']:<15} | {item['idiproc']:<30}")
            print()

        # Mostra a lista de falhas detalhadas
        if detalhes_falhas:
            print("--- Detalhes das Falhas ---")
            for falha in detalhes_falhas:
                print(f"  - NUPLAN: {falha.get('nuplan', 'N/A')}, Erro: {falha.get('erro', 'Desconhecido')}")
        
        print("=" * 70)
        print("Processo finalizado.")
        print()

    # ... (aguardar_enter e confirmar_continuacao continuam iguais) ...
    @staticmethod
    def aguardar_enter():
        """
        Aguarda o usuário pressionar Enter para continuar.
        """
        input("Pressione Enter para continuar...")
    
    @staticmethod
    def confirmar_continuacao(mensagem: str) -> bool:
        """
        Solicita confirmação do usuário para continuar.
        
        Args:
            mensagem (str): Mensagem de confirmação
            
        Returns:
            bool: True se o usuário confirmou, False caso contrário
        """
        print(f"⚠️  {mensagem}")
        resposta = input("   Deseja continuar? (s/n): ").strip().lower()
        return resposta in ['s', 'sim', 'y', 'yes']