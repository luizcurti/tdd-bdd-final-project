import unittest
from service.models import db, Product
from service import app

class TestProductModel(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()

    def test_create_product(self):
        """Test creating a new product"""
        product_data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": 59.95,
            "available": True,
            "category": "Cloths"
        }
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, "Hat")
        self.assertEqual(product.description, "A red fedora")
        self.assertEqual(product.price, 59.95)
        self.assertEqual(product.available, True)
        self.assertEqual(product.category, "Cloths")

    def test_read_product(self):
        """Test reading a product by ID"""
        product_data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": 59.95,
            "available": True,
            "category": "Cloths"
        }
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        # Retrieve product by ID
        retrieved_product = Product.find(product.id)
        self.assertEqual(retrieved_product.name, "Hat")
        self.assertEqual(retrieved_product.description, "A red fedora")

    def test_update_product(self):
        """Test updating an existing product"""
        product_data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": 59.95,
            "available": True,
            "category": "Cloths"
        }
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        # Update product
        product.name = "Updated Hat"
        db.session.commit()

        updated_product = Product.find(product.id)
        self.assertEqual(updated_product.name, "Updated Hat")

    def test_delete_product(self):
        """Test deleting a product"""
        product_data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": 59.95,
            "available": True,
            "category": "Cloths"
        }
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        # Delete product
        Product.delete(product.id)

        # Check if product was deleted
        deleted_product = Product.find(product.id)
        self.assertIsNone(deleted_product)

    def test_list_all_products(self):
        """Test listing all products"""
        # Create multiple products
        product_data_1 = {
            "name": "Hat",
            "description": "A red fedora",
            "price": 59.95,
            "available": True,
            "category": "Cloths"
        }
        product_data_2 = {
            "name": "Shoes",
            "description": "Blue shoes",
            "price": 120.50,
            "available": False,
            "category": "Cloths"
        }

        product1 = Product(**product_data_1)
        product2 = Product(**product_data_2)

        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()

        # List all products
        products = Product.all()
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].name, "Hat")
        self.assertEqual(products[1].name, "Shoes")

    def test_find_product_by_category(self):
        """Test finding products by category"""
        product_data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": 59.95,
            "available": True,
            "category": "Cloths"
        }
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        products = Product.find_by_category("Cloths")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Hat")

    def test_find_product_by_availability(self):
        """Test finding products by availability"""
        product_data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": 59.95,
            "available": True,
            "category": "Cloths"
        }
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        products = Product.find_by_availability(True)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Hat")

    def test_find_product_by_name(self):
        """Test finding products by name"""
        product_data = {
            "name": "Hat",
            "description": "A red fedora",
            "price": 59.95,
            "available": True,
            "category": "Cloths"
        }
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        products = Product.find_by_name("Hat")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Hat")

    def test_find_non_existing_product(self):
        """Test finding a non-existing product by ID"""
        product = Product.find(999)
        self.assertIsNone(product)

if __name__ == "__main__":
    unittest.main()


