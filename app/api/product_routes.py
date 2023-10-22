from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Product, Review
from app import db


product_routes = Blueprint('products', __name__)

# Retrieve a list of all products
@product_routes.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return {'products': [product.to_dict() for product in products]}


# Retrieve details for a specific product
@product_routes.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product.to_dict() if product else ('Product not found', 404)


# Add a new product (for authenticated users)
@product_routes.route('/', methods=['POST'])
@login_required
def add_product():
    data = request.get_json()

    new_product = Product(
        userId=current_user.id,
        productName=data['productName'],
        description=data['description'],
        price=data['price'],
        imgUrl=data['imgUrl'],
        category=data['category'],
        quantity=data['quantity']
    )

    db.session.add(new_product)
    db.session.commit()

    return new_product.to_dict()


# Update details of a specific product (for authenticated users)
@product_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return ('Product not found', 404)

    data = request.get_json()

    product.productName = data.get('productName', product.productName)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.imgUrl = data.get('imgUrl', product.imgUrl)
    product.category = data.get('category', product.category)
    product.quantity = data.get('quantity', product.quantity)

    db.session.commit()

    return product.to_dict()


# Delete a specific product (for authenticated users)
@product_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return ('Product not found', 404)

    db.session.delete(product)
    db.session.commit()

    return {'message': 'Product deleted'}

# Get all the products from a logged in user
@product_routes.route('/current', methods=['GET'])
@login_required
def get_user_products():
    user_id = current_user.id
    user_products = Product.query.filter_by(userId=user_id).all()

    return jsonify({'user_products': [product.to_dict() for product in user_products]})

# Retrieve reviews for a specific product
@product_routes.route('/<int:productId>/reviews', methods=['GET'])
def get_reviews(productId):
    reviews = Review.query.filter_by(productId=productId).all()
    return {'reviews': [review.to_dict() for review in reviews]}

@product_routes.route('/products/<int:productId>/reviews', methods=['POST'])
@login_required
def add_review(productId):
    data = request.get_json()

    new_review = Review(
        userId=current_user.id,
        productId=productId,
        description=data['description'],
        rating=data['rating'],
        dateCreated=db.func.now()
    )

    db.session.add(new_review)
    db.session.commit()

    return new_review.to_dict()