import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class Product:
    def __init__(self, product_id, name, price, stock, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.__stock = stock

    def get_stock(self):
        return self.__stock

    def reduce_stock(self, quantity):
        if quantity <= self.__stock:
            self.__stock -= quantity
            return True
        return False

    def increase_stock(self, quantity):
        self.__stock += quantity

    def show_info(self):
        return (
            str(self.product_id) + ". " +
            self.name +
            " | Fiyat: " + str(self.price) +
            " TL | Stok: " + str(self.__stock) +
            " | Kategori: " + self.category
        )


class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total(self):
        return self.product.price * self.quantity


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        if quantity <= 0:
            return "Adet 0'dan büyük olmalıdır."

        if quantity > product.get_stock():
            return "Yeterli stok yok."

        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                product.reduce_stock(quantity)
                return "Sepetteki ürün adedi güncellendi."

        self.items.append(CartItem(product, quantity))
        product.reduce_stock(quantity)
        return "Ürün sepete eklendi."

    def show_cart(self):
        print("\n--- SEPET ---")

        if len(self.items) == 0:
            print("Sepetiniz boş.")
            return

        for item in self.items:
            print(
                item.product.name + " - " +
                str(item.quantity) + " adet - " +
                str(item.get_total()) + " TL"
            )

        print("Toplam:", self.get_total_price(), "TL")

    def get_total_price(self):
        total = 0
        for item in self.items:
            total += item.get_total()
        return total

    def clear(self):
        self.items.clear()


class Store:
    def __init__(self, store_name):
        self.store_name = store_name
        self.products = []
        self.cart = Cart()

    def add_product(self, product):
        self.products.append(product)

    def show_products(self):
        print("\n--- ÜRÜN LİSTESİ ---")
        for product in self.products:
            print(product.show_info())

    def find_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def save_order(self, customer_name):
        if len(self.cart.items) == 0:
            print("Sepetiniz boş.")
            return

        order_rows = []

        for item in self.cart.items:
            row = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "customer_name": customer_name,
                "product_name": item.product.name,
                "category": item.product.category,
                "unit_price": item.product.price,
                "quantity": item.quantity,
                "total_price": item.get_total()
            }
            order_rows.append(row)

        new_df = pd.DataFrame(order_rows)

        try:
            old_df = pd.read_csv("orders.csv")
            final_df = pd.concat([old_df, new_df], ignore_index=True)
        except FileNotFoundError:
            final_df = new_df

        final_df.to_csv("orders.csv", index=False)
        self.cart.clear()
        print("Sipariş orders.csv dosyasına kaydedildi.")


def show_sales_report():
    try:
        df = pd.read_csv("orders.csv")
    except FileNotFoundError:
        print("orders.csv dosyası bulunamadı.")
        return

    print("\n--- İLK VERİLER ---")
    print(df.head())

    print("\n--- VERİ TEMİZLEME ---")
    df = df.dropna()

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")

    df = df.dropna()

    print("\n--- TOPLAM CİRO ---")
    print(df["total_price"].sum(), "TL")

    print("\n--- ÜRÜN BAZLI SATIŞ ---")
    product_summary = df.groupby("product_name")["quantity"].sum().sort_values(ascending=False)
    print(product_summary)

    print("\n--- KATEGORİ BAZLI CİRO ---")
    category_summary = df.groupby("category")["total_price"].sum().sort_values(ascending=False)
    print(category_summary)

    plt.figure(figsize=(8, 5))
    product_summary.plot(kind="bar")
    plt.title("En Çok Satılan Ürünler")
    plt.xlabel("Ürün")
    plt.ylabel("Satılan Adet")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    category_summary.plot(kind="bar")
    plt.title("Kategori Bazlı Ciro")
    plt.xlabel("Kategori")
    plt.ylabel("Ciro")
    plt.tight_layout()
    plt.show()


store = Store("BT Shop")
store.add_product(Product(1, "Laptop", 25000, 5, "Teknoloji"))
store.add_product(Product(2, "Mouse", 500, 10, "Teknoloji"))
store.add_product(Product(3, "Klavye", 1200, 8, "Teknoloji"))
store.add_product(Product(4, "Kulaklık", 2000, 6, "Ses"))
store.add_product(Product(5, "Defter", 100, 30, "Kırtasiye"))
store.add_product(Product(6, "Ofis Sandalyesi", 4500, 7, "Mobilya"))
store.add_product(Product(7, "Akıllı Saat", 3500, 9, "Teknoloji"))
store.add_product(Product(8, "Bluetooth Hoparlör", 1500, 6, "Ses"))

while True:
    print("\n===== GELİŞMİŞ E-TİCARET MENÜSÜ =====")
    print("1. Ürünleri Göster")
    print("2. Sepete Ürün Ekle")
    print("3. Sepeti Göster")
    print("4. Siparişi Tamamla")
    print("5. Satış Raporunu Göster")
    print("6. Çıkış")

    choice = input("Bir seçenek girin: ")

    try:
        if choice == "1":
            store.show_products()

        elif choice == "2":
            store.show_products()
            product_id = int(input("Ürün id girin: "))
            quantity = int(input("Adet girin: "))
            product = store.find_product(product_id)

            if product is None:
                print("Ürün bulunamadı.")
            else:
                result = store.cart.add_item(product, quantity)
                print(result)

        elif choice == "3":
            store.cart.show_cart()

        elif choice == "4":
            customer_name = input("Müşteri adını girin: ")
            store.save_order(customer_name)

        elif choice == "5":
            show_sales_report()

        elif choice == "6":
            print("Uygulamadan çıkılıyor...")
            break

        else:
            print("Geçersiz seçim.")

    except ValueError:
        print("Lütfen geçerli sayılar girin.")
    except Exception as error:
        print("Beklenmeyen hata:", error)
