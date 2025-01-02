from behave import given
from service.models import db, Product
from service import app

@app.before_all
def setup():
    """Create the necessary tables before tests are run."""
    db.create_all()

@app.after_all
def teardown():
    """Clean up after tests are done."""
    db.session.remove()
    db.drop_all()

@given('the following products exist')
def step_impl(context):
    """Load the products into the database from the scenario's context table."""
    for row in context.table:
        product_data = {
            "name": row["Name"],
            "description": row["Description"],
            "price": float(row["Price"]),
            "available": row["Available"] == "True",  # Ensure boolean comparison
            "category": row["Category"]
        }
        
        product = Product(**product_data)
        db.session.add(product)
    db.session.commit()

