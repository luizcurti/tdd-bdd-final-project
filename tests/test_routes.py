import unittest
from service import app
from service.models import db, Product
from tests.factories import ProductFactory

BASE_URL = "/products"

class TestProductRoutes(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def _create_products(self, count=1):
        """Helper method to create products"""
        products = []
        for _ in range(count):
            product = ProductFactory()
            response = self.app.post(BASE_URL, json=product.serialize())
            self.assertEqual(response.status_code, 201)  # HTTP_201_CREATED
            products.append(response.get_json())
        return products

    def test_list_products(self):
        """Test listing all products"""
        self._create_products(5)
        response = self.app.get(BASE_URL)
        self.assertEqual(response.status_code, 200)  # HTTP_200_OK
        products = response.get_json()
        self.assertEqual(len(products), 5)

    def test_get_product(self):
        """Test retrieving a product by ID"""
        product = self._create_products(1)[0]
        response = self.app.get(f"{BASE_URL}/{product['id']}")
        self.assertEqual(response.status_code, 200)  # HTTP_200_OK
        data = response.get_json()
        self.assertEqual(data["name"], product["name"])

    def test_get_product_not_found(self):
        """Test retrieving a non-existent product"""
        response = self.app.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, 404)  # HTTP_404_NOT_FOUND

    def test_create_product(self):
        """Test creating a product"""
        product = ProductFactory()
        response = self.app.post(BASE_URL, json=product.serialize())
        self.assertEqual(response.status_code, 201)  # HTTP_201_CREATED
        data = response.get_json()
        self.assertEqual(data["name"], product.name)

    def test_update_product(self):
        """Test updating a product"""
        product = self._create_products(1)[0]
        updated_data = {"name": "Updated Name"}
        response = self.app.put(f"{BASE_URL}/{product['id']}", json=updated_data)
        self.assertEqual(response.status_code, 200)  # HTTP_200_OK
        data = response.get_json()
        self.assertEqual(data["name"], "Updated Name")

    def test_delete_product(self):
        """Test deleting a product"""
        product = self._create_products(1)[0]
        response = self.app.delete(f"{BASE_URL}/{product['id']}")
        self.assertEqual(response.status_code, 204)  # HTTP_204_NO_CONTENT

        # Verify deletion
        response = self.app.get(f"{BASE_URL}/{product['id']}")
        self.assertEqual(response.status_code, 404)  # HTTP_404_NOT_FOUND

    def test_filter_products_by_category(self):
        """Test filtering products by category"""
        self._create_products(3)
        response = self.app.get(f"{BASE_URL}?category=Cloths")
        self.assertEqual(response.status_code, 200)  # HTTP_200_OK

    def test_filter_products_by_name(self):
        """Test filtering products by name"""
        self._create_products(3)
        response = self.app.get(f"{BASE_URL}?name=Hat")
        self.assertEqual(response.status_code, 200)  # HTTP_200_OK

    def test_filter_products_by_availability(self):
        """Test filtering products by availability"""
        # Create products with different availability statuses
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
        product_data_3 = {
            "name": "Big Mac",
            "description": "1/4 lb burger",
            "price": 5.99,
            "available": True,
            "category": "Food"
        }

        self.app.post(BASE_URL, json=product_data_1)
        self.app.post(BASE_URL, json=product_data_2)
        self.app.post(BASE_URL, json=product_data_3)

        # Filter products by availability = True
        response = self.app.get(f"{BASE_URL}?available=true")
        self.assertEqual(response.status_code, 200)  # HTTP_200_OK
        products = response.get_json()
        self.assertEqual(len(products), 2)  # Only 2 products should be available

        # Filter products by availability = False
        response = self.app.get(f"{BASE_URL}?available=false")
        self.assertEqual(response.status_code, 200)  # HTTP_200_OK
        products = response.get_json()
        self.assertEqual(len(products), 1)  # Only 1 product should not be available

if __name__ == "__main__":
    unittest.main()


