class Book:

    def __init__(self, title, author, price, number_of_pages,
                 quantity, number_of_sales=0):
        self._title = ""
        self._author = ""
        self._price = 0.0
        self._number_of_pages = 1
        self._quantity = 0
        self._number_of_sales = 0

        self.title = title
        self.author = author
        self.price = price
        self.number_of_pages = number_of_pages
        self.quantity = quantity
        self.number_of_sales = number_of_sales

    def __del__(self):
        print(f"Книгу '{self._title}' видалено з пам'яті.")

    # Функції доступу (властивості)
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Назва книги не може бути порожньою.")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Автор книги не може бути порожнім.")
        self._author = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        self._price = float(value)

    @property
    def number_of_pages(self):
        return self._number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, value):
        if value <= 0:
            raise ValueError("Кількість сторінок має бути більшою за 0.")
        self._number_of_pages = int(value)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Кількість не може бути від'ємною.")
        self._quantity = int(value)

    @property
    def number_of_sales(self):
        return self._number_of_sales

    @number_of_sales.setter
    def number_of_sales(self, value):
        if value < 0:
            raise ValueError("Кількість продажів не може бути від'ємною.")
        self._number_of_sales = int(value)

    # Методи
    def sell(self, amount=1):
        if amount <= 0:
            raise ValueError("Кількість для купівлі має бути більшою за 0.")
        if amount > self._quantity:
            raise ValueError(
                f"Недостатньо примірників '{self._title}': "
                f"у наявності {self._quantity}, потрібно {amount}."
            )
        self._quantity -= amount
        self._number_of_sales += amount
        return amount * self._price

    def show_info(self):
        print(self)

    def __str__(self):
        return (
            f"{self._title:<28} | {self._author:<18} | "
            f"{self._price:>8.2f} грн | {self._number_of_pages:>4} стор. | "
            f"в наявності: {self._quantity:>3} | "
            f"продано: {self._number_of_sales:>3}"
        )


class BookShop:

    def __init__(self, name):
        self._name = name
        self._books = []

    def __del__(self):
        print(f"Книгарню '{self._name}' закрито.")

    def __len__(self):
        return len(self._books)

    # Функції доступу
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Назва книгарні не може бути порожньою.")
        self._name = value

    @property
    def books(self):
        return list(self._books)

    # Додавання та видалення
    def add_book(self, book):
        for item in self._books:
            if (item.title.lower() == book.title.lower()
                    and item.author.lower() == book.author.lower()):
                item.quantity += book.quantity
                print(f"Книга '{book.title}' вже є: кількість збільшено.")
                return
        self._books.append(book)
        print(f"Книгу '{book.title}' додано до магазину.")

    def remove_book(self, title):
        for item in self._books:
            if item.title.lower() == title.strip().lower():
                self._books.remove(item)
                print(f"Книгу '{item.title}' видалено з магазину.")
                return True
        print(f"Книгу '{title}' не знайдено.")
        return False

    def find_book(self, title):
        for item in self._books:
            if item.title.lower() == title.strip().lower():
                return item
        return None

    def buy_book(self, title, amount=1):
        book = self.find_book(title)
        if book is None:
            print(f"Книгу '{title}' не знайдено.")
            return None
        try:
            total = book.sell(amount)
        except ValueError as error:
            print(f"Помилка купівлі: {error}")
            return None
        print(f"Куплено {amount} шт. '{book.title}' на суму {total:.2f} грн.")
        return total

    # Топи
    def top_by_price(self, count=3):
        return sorted(self._books, key=lambda b: b.price, reverse=True)[:count]

    def top_by_sales(self, count=3):
        return sorted(
            self._books, key=lambda b: b.number_of_sales, reverse=True
        )[:count]

    # Виведення
    @staticmethod
    def _print_books(books):
        if not books:
            print("  (список порожній)")
            return
        for number, book in enumerate(books, start=1):
            print(f"{number:>2}. {book}")

    def show_books(self):
        print(f"\nАсортимент книгарні '{self._name}':")
        self._print_books(self._books)

    def show_top_by_price(self, count=3):
        print(f"\nТоп-{count} книжок за ціною:")
        self._print_books(self.top_by_price(count))

    def show_top_by_sales(self, count=3):
        print(f"\nТоп-{count} книжок за кількістю продажів:")
        self._print_books(self.top_by_sales(count))


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значення не може бути порожнім.")


def read_number(prompt, number_type=float, minimum=0):
    while True:
        try:
            value = number_type(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("Помилка: введіть число.")
            continue
        if value < minimum:
            print(f"Помилка: значення має бути не менше {minimum}.")
            continue
        return value


def input_book():
    title = read_text("Назва: ")
    author = read_text("Автор: ")
    price = read_number("Ціна: ")
    pages = read_number("Кількість сторінок: ", int, 1)
    quantity = read_number("Кількість примірників: ", int, 0)
    return Book(title, author, price, pages, quantity)


def menu(shop):
    """Інтерактивне меню: користувач сам додає і видаляє книги."""
    actions = (
        "\n1 - Показати всі книги\n"
        "2 - Додати книгу\n"
        "3 - Видалити книгу\n"
        "4 - Купити книгу\n"
        "5 - Топ за ціною\n"
        "6 - Топ за кількістю продажів\n"
        "0 - Вихід"
    )
    while True:
        print(actions)
        choice = input("Ваш вибір: ").strip()
        if choice == "1":
            shop.show_books()
        elif choice == "2":
            shop.add_book(input_book())
        elif choice == "3":
            shop.remove_book(read_text("Назва книги для видалення: "))
        elif choice == "4":
            title = read_text("Назва книги: ")
            amount = read_number("Скільки примірників: ", int, 1)
            shop.buy_book(title, amount)
        elif choice == "5":
            shop.show_top_by_price(read_number("Розмір топу: ", int, 1))
        elif choice == "6":
            shop.show_top_by_sales(read_number("Розмір топу: ", int, 1))
        elif choice == "0":
            break
        else:
            print("Невідомий пункт меню.")


def create_shop():
    shop = BookShop("Книгарня Є")
    shop.add_book(Book("Кобзар", "Тарас Шевченко", 250, 480, 10, 35))
    shop.add_book(Book("Intermezzo", "Михайло Коцюбинський", 180, 220, 5, 12))
    shop.add_book(Book("Захар Беркут", "Іван Франко", 210, 300, 8, 27))
    shop.add_book(Book("Лісова пісня", "Леся Українка", 150, 160, 12, 41))
    shop.add_book(Book("Тигролови", "Іван Багряний", 320, 410, 4, 19))
    return shop


def demo(shop):
    shop.add_book(Book("Кобзар", "Тарас Шевченко", 250, 480, 5))
    shop.show_books()

    print("\nКупівля книжок:")
    shop.buy_book("Лісова пісня", 3)
    shop.buy_book("Тигролови", 2)
    shop.buy_book("Тигролови", 10)
    shop.buy_book("Невідома книга")

    shop.show_top_by_price()
    shop.show_top_by_sales()

    print("\nВидалення книжок:")
    shop.remove_book("Intermezzo")
    shop.remove_book("Невідома книга")

    shop.show_books()
    print(f"\nКількість назв у магазині: {len(shop)}")

    print("\nДемонстрація функцій доступу:")
    book = shop.find_book("Кобзар")
    book.price = 275
    print(f"Нова ціна '{book.title}': {book.price:.2f} грн")
    book.show_info()

    print("\nДемонстрація деструктора:")
    del book


def main():
    shop = create_shop()
    print("1 - Автоматична демонстрація")
    print("2 - Інтерактивне меню (додавання/видалення вручну)")
    if input("Оберіть режим: ").strip() == "2":
        menu(shop)
    else:
        demo(shop)
    del shop


if __name__ == "__main__":
    main()