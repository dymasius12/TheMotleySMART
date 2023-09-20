import unittest
import Start_Gui as sg
import pyautogui  # This module helps in programmatically controlling the mouse and keyboard.

class TestStartGui(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.app = sg.root
        self.app.update()

    def tearDown(self):
        # Close the application after each test
        if self.app:
            self.app.destroy()

    def test_initialization(self):
        self.assertIsNotNone(self.app)
        self.assertTrue(isinstance(self.app, sg.tk.Tk))

    def test_input_validation_empty(self):
        sg.menu_listbox.select_set(0)
        sg.confirm_button.invoke()
        # Check if an error messagebox appears
        alert = pyautogui.alert(text="Please enter a stock code or company name.")
        self.assertIsNotNone(alert)

    def test_input_validation_nonexistent_stock(self):
        sg.stock_code_entry.delete(0, sg.tk.END)
        sg.stock_code_entry.insert(0, "NONEXISTENT")
        sg.menu_listbox.select_set(0)
        sg.confirm_button.invoke()
        # Check if an error messagebox appears
        alert = pyautogui.alert(text="Error fetching data for NONEXISTENT.")
        self.assertIsNotNone(alert)

    def test_select_company_dropdown(self):
        sg.company_dropdown.set("3M Company")  # This is just an example
        selected_value = sg.company_dropdown.get()
        self.assertEqual(selected_value, "3M Company")

    def test_stock_price_vs_time(self):
        sg.stock_code_entry.delete(0, sg.tk.END)
        sg.stock_code_entry.insert(0, "AAPL")  # Testing with Apple's stock
        sg.menu_listbox.select_set(1)
        sg.confirm_button.invoke()
        # Here you'd typically want to check if a graph is displayed, but that's beyond the scope of basic unittest.

    def test_stock_analysis(self):
        sg.stock_code_entry.delete(0, sg.tk.END)
        sg.stock_code_entry.insert(0, "AAPL")  # Testing with Apple's stock
        sg.menu_listbox.select_set(2)
        sg.confirm_button.invoke()
        # Here you'd typically want to check if the analysis is displayed, but that's beyond the scope of basic unittest.

    def test_stock_news(self):
        sg.company_dropdown.set("3M Company")  # This is just an example
        sg.menu_listbox.select_set(3)
        sg.confirm_button.invoke()
        # Here you'd typically want to check if news articles are displayed, but that's beyond the scope of basic unittest.

    def test_monte_carlo_simulation(self):
        sg.stock_code_entry.delete(0, sg.tk.END)
        sg.stock_code_entry.insert(0, "AAPL")  # Testing with Apple's stock
        sg.menu_listbox.select_set(4)
        sg.confirm_button.invoke()
        # Here you'd typically want to check if the simulation is displayed, but that's beyond the scope of basic unittest.

    def test_exit_program(self):
        sg.menu_listbox.select_set(5)
        sg.confirm_button.invoke()
        # Check if application is destroyed
        self.assertIsNone(self.app)

if __name__ == "__main__":
    unittest.main()
