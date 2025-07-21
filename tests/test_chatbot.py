import unittest
from unittest.mock import MagicMock, patch
import main

class TestChatbotCI(unittest.TestCase):
    
    def test_mock_connection(self):
        """Testa a função de conexão com um mock LLM"""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = "Mocked Response"
        
        result = main.testar_conexao_llm(mock_llm)
        self.assertTrue(result)
        mock_llm.invoke.assert_called_once_with("Qual é o seu nome?")
    
    def test_chatbot_configuration(self):
        """Testa a configuração do chatbot com mock LLM"""
        mock_llm = MagicMock()
        chain = main.configurar_chatbot(mock_llm)
        self.assertIsNotNone(chain)
    
    @patch('main.RunnablePassthrough')
    @patch('main.PromptTemplate')
    def test_full_chain(self, mock_prompt, mock_runnable):
        """Testa a criação da cadeia completa"""
        mock_llm = MagicMock()
        mock_prompt_instance = MagicMock()
        mock_prompt.return_value = mock_prompt_instance
        
        main.configurar_chatbot(mock_llm)
        
        # Verifica se os componentes foram chamados corretamente
        mock_prompt.assert_called_once()
        mock_runnable.assert_called_once()
    
    def test_ci_test_function(self):
        """Testa a função de teste de CI completa"""
        with patch('main.testar_conexao_llm', return_value=True), \
             patch('main.configurar_chatbot', return_value=MagicMock()):
            
            result = main.executar_teste_ci()
            self.assertTrue(result)
    
    def test_ci_test_failure(self):
        """Testa cenário de falha no teste de CI"""
        with patch('main.testar_conexao_llm', return_value=False):
            result = main.executar_teste_ci()
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()