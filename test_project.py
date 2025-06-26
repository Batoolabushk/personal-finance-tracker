import pytest
import os
import csv
from unittest.mock import patch, mock_open
from project import add_transaction, calculate_balance, get_category_breakdown


class TestAddTransaction:
    """Test cases for add_transaction function."""
    
    @patch('builtins.input', side_effect=['100.50', 'Salary', 'Job'])
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_add_transaction_income_new_file(self, mock_exists, mock_file, mock_input):
        """Test adding income transaction to new file."""
        result = add_transaction("income")
        assert result == True
        mock_file.assert_called_once()
    
    @patch('builtins.input', side_effect=['50.25', 'Groceries', 'Food'])
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_add_transaction_expense_existing_file(self, mock_exists, mock_file, mock_input):
        """Test adding expense transaction to existing file."""
        result = add_transaction("expense")
        assert result == True
        mock_file.assert_called_once()
    
    @patch('builtins.input', side_effect=['-100', 'Invalid', 'Test'])
    def test_add_transaction_negative_amount(self, mock_input):
        """Test adding transaction with negative amount."""
        result = add_transaction("income")
        assert result == False
    
    @patch('builtins.input', side_effect=['abc', 'Invalid', 'Test'])
    def test_add_transaction_invalid_amount(self, mock_input):
        """Test adding transaction with invalid amount."""
        result = add_transaction("expense")
        assert result == False
    
    @patch('builtins.input', side_effect=['100', '', 'Test'])
    def test_add_transaction_empty_description(self, mock_input):
        """Test adding transaction with empty description."""
        result = add_transaction("income")
        assert result == False
    
    @patch('builtins.input', side_effect=['100', 'Test', ''])
    def test_add_transaction_empty_category(self, mock_input):
        """Test adding transaction with empty category."""
        result = add_transaction("expense")
        assert result == False


class TestCalculateBalance:
    """Test cases for calculate_balance function."""
    
    @patch('os.path.exists', return_value=False)
    def test_calculate_balance_no_file(self, mock_exists):
        """Test balance calculation when no transactions file exists."""
        income, expenses, balance = calculate_balance()
        assert income == 0.0
        assert expenses == 0.0
        assert balance == 0.0
    
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Date,Type,Amount,Description,Category\n2024-01-01,income,1000.0,Salary,Job\n2024-01-02,expense,500.0,Rent,Housing\n2024-01-03,income,200.0,Freelance,Job\n')
    def test_calculate_balance_with_transactions(self, mock_file, mock_exists):
        """Test balance calculation with income and expense transactions."""
        income, expenses, balance = calculate_balance()
        assert income == 1200.0
        assert expenses == 500.0
        assert balance == 700.0
    
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Date,Type,Amount,Description,Category\n2024-01-01,income,500.0,Salary,Job\n2024-01-02,expense,800.0,Rent,Housing\n')
    def test_calculate_balance_negative_balance(self, mock_file, mock_exists):
        """Test balance calculation resulting in negative balance."""
        income, expenses, balance = calculate_balance()
        assert income == 500.0
        assert expenses == 800.0
        assert balance == -300.0
    
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Date,Type,Amount,Description,Category\n')
    def test_calculate_balance_empty_file(self, mock_file, mock_exists):
        """Test balance calculation with empty transactions file."""
        income, expenses, balance = calculate_balance()
        assert income == 0.0
        assert expenses == 0.0
        assert balance == 0.0


class TestGetCategoryBreakdown:
    """Test cases for get_category_breakdown function."""
    
    @patch('os.path.exists', return_value=False)
    def test_get_category_breakdown_no_file(self, mock_exists):
        """Test category breakdown when no transactions file exists."""
        breakdown = get_category_breakdown()
        expected = {"income": {}, "expense": {}}
        assert breakdown == expected
    
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Date,Type,Amount,Description,Category\n2024-01-01,income,1000.0,Salary,Job\n2024-01-02,expense,500.0,Rent,Housing\n2024-01-03,income,200.0,Freelance,Job\n2024-01-04,expense,100.0,Groceries,Food\n')
    def test_get_category_breakdown_with_transactions(self, mock_file, mock_exists):
        """Test category breakdown with multiple transactions."""
        breakdown = get_category_breakdown()
        
        expected = {
            "income": {"Job": 1200.0},
            "expense": {"Housing": 500.0, "Food": 100.0}
        }
        assert breakdown == expected
    
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Date,Type,Amount,Description,Category\n2024-01-01,income,500.0,Salary,Job\n2024-01-02,income,300.0,Bonus,Job\n2024-01-03,income,150.0,Freelance,Consulting\n')
    def test_get_category_breakdown_income_only(self, mock_file, mock_exists):
        """Test category breakdown with only income transactions."""
        breakdown = get_category_breakdown()
        
        expected = {
            "income": {"Job": 800.0, "Consulting": 150.0},
            "expense": {}
        }
        assert breakdown == expected
    
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Date,Type,Amount,Description,Category\n2024-01-01,expense,300.0,Rent,Housing\n2024-01-02,expense,200.0,Mortgage,Housing\n2024-01-03,expense,50.0,Gas,Transportation\n')
    def test_get_category_breakdown_expenses_only(self, mock_file, mock_exists):
        """Test category breakdown with only expense transactions."""
        breakdown = get_category_breakdown()
        
        expected = {
            "income": {},
            "expense": {"Housing": 500.0, "Transportation": 50.0}
        }
        assert breakdown == expected
    
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Date,Type,Amount,Description,Category\n')
    def test_get_category_breakdown_empty_file(self, mock_file, mock_exists):
        """Test category breakdown with empty transactions file."""
        breakdown = get_category_breakdown()
        expected = {"income": {}, "expense": {}}
        assert breakdown == expected


# Additional integration tests
class TestIntegration:
    """Integration tests for the finance tracker."""
    
    def test_transaction_workflow(self):
        """Test that transactions can be added and calculated correctly."""
        # This would be an integration test that could use temporary files
        # For now, we'll test the data flow between functions
        pass


if __name__ == "__main__":
    pytest.main([__file__])
