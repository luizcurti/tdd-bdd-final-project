from flask import jsonify, request, abort
from service.models import Product
from service.common.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

@app.route("/products", methods=["GET"])
def list_products():
    """List all products or filter by optional parameters"""
    category = request.args.get("category")
    name = request.args.get("name")
    available = request.args.get("available")

    if category:
        products = Product.find_by_category(category)
    elif name:
        products = Product.find_by_name(name)
    elif available:
        products = Product.find_by_availability(available == "true")
    else:
        products = Product.all()

    return jsonify([product.serialize() for product in products]), HTTP_200_OK


@app.route("/products", methods=["POST"])
def create_product():
    """Create a new product"""
    data = request.get_json()
    product = Product()
    product.deserialize(data)
    product.create()
    return jsonify(product.serialize()), HTTP_201_CREATED


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Retrieve a product by ID"""
    product = Product.find(product_id)
    if not product:
        abort(HTTP_404_NOT_FOUND, f"Product with id {product_id} not found")
    return jsonify(product.serialize()), HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update an existing product"""
    product = Product.find(product_id)
    if not product:
        abort(HTTP_404_NOT_FOUND, f"Product with id {product_id} not found")

    data = request.get_json()
    product.deserialize(data)
    product.update()
    return jsonify(product.serialize()), HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product by ID"""
    product = Product.find(product_id)
    if not product:
        abort(HTTP_404_NOT_FOUND, f"Product with id {product_id} not found")

    product.delete()
    return "", HTTP_204_NO_CONTENT

