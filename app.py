from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sqlalchemy.exc import IntegrityError


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma 
ma = Marshmallow(app)


#Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self,name,description,price,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        
#Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')
        
# init Schema
product_schema = ProductSchema()
# for get all
products_schema = ProductSchema(many=True)

#Create a Product
@app.route('/product',methods=['POST'])
def add_product():
    try: 
        name = request.json['name']        
        description = request.json['description']        
        price = request.json['price']        
        qty = request.json['qty']   
        
        new_product = Product(name,description,price,qty)
        
        db.session.add(new_product)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return 'Error: Integrity constraint violated', 400
    return product_schema.jsonify(new_product)     

# Get all products
@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get Single Products 
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update the Products
@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']        
    description = request.json['description']        
    price = request.json['price']        
    qty = request.json['qty']   
    
    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    
    db.session.commit()
    
    return product_schema.jsonify(product)

# Delete the Products
@app.route('/product/<id>',methods=['DELETE'])
def delete_product(id):
    try: 
        product = Product.query.get(id)
        db.session.delete(product)
    except BaseException: 
        return "None"
    db.session.commit()
    return product_schema.jsonify(product)


#create database
with app.app_context():
    db.create_all()
#Run server
if __name__ == '__main__':
    app.run(debug=True)
