# PERSONAL FINANCE TRACKER
#### Description: 
   The Personal Finance Tracker is a Python command-line tool that tracks income and expenses to assist users in managing their personal finances.  
    For people who wish to keep an eye on their financial well-being without the hassle of using sophisticated commercial financial software, this project offers a straightforward yet complete answer.

Project Overview: 
    Users of this application can keep track of their financial activities, 
    classify them, and produce informative reports about their spending habits and general financial situation.  
    All data is stored locally by the software in CSV format, 
    which makes it portable and simple to backup or examine using third-party programs like Google Sheets or Excel.

File Structure and Functionality
    project.py
    This is the primary program file that has all of the essential features. 
    A primary function and multiple auxiliary functions that manage different parts of the financial tracking system make up the file's structure:
        main(): offers users access to an interactive command-line interface with a menu system that lets them choose between functions. 
            Until the user decides to stop using it, this function keeps running.
        add_transaction(transaction_type): takes care of the integration of new financial transactions, whether they are expenses or income.  
            To guarantee data integrity, this function incorporates thorough input validation; it looks for positive sums, non-empty descriptions and categories, and smoothly handles a variety of incorrect situations.  
            Every transaction is automatically timestamp-ed and written to the CSV file by the function.
        calculate_balance(): calculates the user's net balance, total income, and total expenses by reading all of the transactions from the CSV file.  
            This function handles file access errors and produces a tuple of these three values.
        get_category_breakdown(): identifies areas for possible savings or budget adjustments by classifying transactions for both income and expenses, 
            giving users a better understanding of where their money is coming from and going.
        display_summary(): Presents a detailed financial overview to the user, including the balance calculation and category breakdown.  
            It also provides visual feedback regarding whether the user is working at a profit or loss.
        display_all_transactions(): gives users a comprehensive transaction history for examination and confirmation by displaying a prepared table of all recorded transactions.

   test_project.py
    With more than 15 test cases that cover all significant functions, this file includes a thorough test suite. 
    Python's unittest.mock module is used to test file operations without actually writing files while testing, and the tests are grouped into classes for improved structure.
    The test suite includes:
        Positive test cases: Testing normal operation with valid inputs
        Negative test cases: Testing error handling with invalid inputs
        Edge cases: Testing boundary scenarios like empty files and negative balances
        Mocking: Using mock objects to simulate file operations and user input for reliable, isolated testing
    
   requirements.txt
    Contains the single dependency required for this project:
        To run the test suite, use pytest.  
        In order to maintain minimal dependencies and guarantee wide compatibility, the project purposefully solely uses Python standard library modules.

  transactions.csv
    All financial data is automatically stored in this file, 
    which is created by the application and uses a straightforward CSV format with columns for Date, Type, Amount, Description, and Category to make the data portable and simply readable.

Design Decisions
    Several key design decisions were made during development:
    CSV Storage: I chose CSV over a database for simplicity and portability. CSV files can be easily opened in spreadsheet applications and don't require additional dependencies or setup.
    Command-Line Interface: Instead of a graphical user interface (GUI), I implemented a text-based menu system that is easy to use and doesn't require additional libraries, keeping the application lightweight and universally compatible.
    Input Validation: Comprehensive validation ensures data integrity by checking for positive amounts, non-empty strings, and easily handling various error conditions. 
    Modular Function Design: Each function has a single responsibility, making the code easier to test, maintain, and extend. Functions return meaningful values that are easy to test.
    Category System: By including categories for both income and expenses, the program becomes more helpful for financial planning by offering insightful information about spending trends and revenue sources.


This Personal Finance Tracker offers useful features for managing personal finances while showcasing sound programming techniques including error handling, data validation, modular architecture, and thorough testing.
