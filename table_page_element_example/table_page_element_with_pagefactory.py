from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By
import time
from selenium import webdriver


class TableElementPF(PageFactory):
    def __init__(self, driver, table_id):
        self.driver = driver
        self.locators = {"element": ("ID", table_id)}

    def get_headers(self) -> list[str]:
        """Возвращает список заголовков таблицы."""
        header_elements = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return [header.text for header in header_elements]

    def get_row_data(self, row_index: int) -> list[str]:
        """Возвращает данные конкретной строки по её индексу (начиная с 0)."""
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return [cell.text for cell in cells]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        """Возвращает значение конкретной ячейки."""
        # TODDO: 1) как переписать используя вызов get_row_data ?
        value = self.get_row_data(row_index)
        return value[column_index]


if __name__ == "__main__":
    # Инициализация драйвера
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    try:
        # Открытие страницы
        driver.get("https://the-internet.herokuapp.com/tables")

        # Инициализация таблицы как Page Element через её локатор
        # table1_locator = (By.ID, "table1")
        table = TableElementPF(driver, "table1")
        # table2_locator = (By.ID, "table2")
        table2 = TableElementPF(driver, "table2")

        # Сбор данных для демонстрации
        headers = table.get_headers()
        first_row = table.get_row_data(0)
        specific_cell = table.get_cell_value(row_index=2, column_index=3)  # Строка 3, Колонка 4 (Due)
        headers_table_2 = table2.get_headers()
        first_row_table_2 = table2.get_row_data(0)
        specific_cell_table_2 = table2.get_cell_value(row_index=3, column_index=3)

        # Вывод результатов в консоль
        print("Заголовки таблицы:", headers)
        print("Первая строка данных:", first_row)
        print(f"Значение в строке 3, колонке 'Due': {specific_cell}")
        print("Первая строка данных во второй таблице:", first_row_table_2)
        print(f"Значение в строке 4, колонке 'Due': {specific_cell_table_2}")
        # Простые проверки (Assertions)
        assert "Last Name" in headers, "Заголовок 'Last Name' не найден"
        assert "Smith" in first_row, "Фамилия 'Smith' должна быть в первой строке"
        assert specific_cell == "$100.00", f"Ожидалось $100.00, но получено {specific_cell}"
        assert specific_cell_table_2 == "$50.00"
        assert "Smith" in first_row_table_2
        assert headers == headers_table_2
        assert first_row == first_row_table_2

        print("\n✅ Тест успешно пройден!")
        time.sleep(5)

    finally:
        driver.quit()
