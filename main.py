import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import raw_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf 8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class Offer (db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer = db.relationship("Order", foreign_keys=[order_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


db. create_all()

for user_data in raw_data.users:
    new_user = User(
        id=user_data["id"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        age=user_data["age"],
        email=user_data["email"],
        role=user_data["role"],
        phone=user_data["phone"],
    )
    db. session. add(new_user)
    db. session.commit()


for order_data in raw_data.order:
    new_order = Order(
        id=order_data["id"],
        name=order_data["name"],
        description=order_data["description"],
        start_date=order_data["start_date"],
        end_date=order_data["end_date"],
        address=order_data["address"],
        price=order_data["price"],
        customer_id=order_data["customer_id"],
        executor_id=order_data["executor_id"],
    )
    db. session. add(new_order)
    db. session.commit()

for offer_data in raw_data.offers:
    new_offer = Offer(
        id=offer_data["id"],
        order_id=offer_data["order_id"],
        executor_id=offer_data["executor_id"],
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/users", methods=["POST", "GET"])
def all_users():
    if request.method == "GET":
        res = []
        for u in User.query.all():
            res. append(u.to_dict())

        return jsonify(res), 200, {'Content-Type': 'application/json; charset=utf-8'}

    elif request.method == "POST":
        new_user_new = json.loads(request.data)
        new_users = User(
            id=new_user_new["id"],
            first_name=new_user_new["first_name"],
            last_name=new_user_new["last_name"],
            age=new_user_new["age"],
            email=new_user_new["email"],
            role=new_user_new["role"],
            phone=new_user_new["phone"],
        )
        db.session.add(new_users)
        db.session.commit()
        return '', 201


@app.route("/users/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def user(uid: int):
    if request.method == "GET":
        return jsonify(User.query.get(uid).to_dict()), 200, {
            'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = User.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        new_user_new = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = new_user_new["first_name"]
        u.last_name = new_user_new["last_name"]
        u.age = new_user_new["age"]
        u.email = new_user_new["email"]
        u.role = new_user_new["role"]
        u.phone = new_user_new["phone"]

        db.session.add(u)
        db.session.commit()
        return '', 204


@app.route('/orders', methods=['GET', 'POST'])
def all_orders():
    if request.method == "GET":
        result = []
        for order in Order.query.all():
            result.append(order.to_dict())
        return jsonify(result)

    elif request.method == 'POST':
        order_data_new = json.loads(request.data)
        new_orders = Order(
            id=order_data_new["id"],
            name=order_data_new["name"],
            description=order_data_new["description"],
            start_date=order_data_new["start_date"],
            end_date=order_data_new["end_date"],
            address=order_data_new["address"],
            price=order_data_new["price"],
            customer_id=order_data_new["customer_id"],
            executor_id=order_data_new["executor_id"]
        )
        db. session.add(new_orders)
        db. session.commit()
        return "", 201


@app.route("/orders/<int:uid>", methods=["GET", "PUT", "DELETE"])
def get_order(uid: int):
    if request.method == 'GET':
        return jsonify(Order.query.get(uid).to_dict())

    elif request.method == 'PUT':
        order_data_new = json.loads(request.data)
        order = Order.query.get(uid)
        order.id = order_data_new['id']
        order.name = order_data_new["name"]
        order.description = order_data_new["description"]
        order.start_date = order_data_new['start_date']
        order.end_date = order_data_new['end_date']
        order.address = order_data_new['address']
        order.price = order_data_new['price']
        order.customer_id = order_data_new["customer_id"]
        order.executor_id = order_data_new["executor_id"]

        db.session.add(order)
        db. session.commit()
        return '', 204


@app.route('/offers', methods=['GET', 'POST'])
def all_offers():
    if request.method == "GET":
        result = []
        for offer in Offer.query.all():
            result.append(offer.to_dict())
        return jsonify(result)

    elif request.method == 'POST':
        offer_data_new = json.loads(request.data)
        new_offers = Offer(
            id=offer_data_new["id"],
            order_id=offer_data_new["order_id"],
            executor_id=offer_data_new["executor_id"]
        )
        db. session.add(new_offers)
        db. session.commit()
        return "", 201


@app.route("/offers/<int:uid>", methods=["GET", "PUT", "DELETE"])
def get_offer(uid: int):
    if request.method == 'GET':
        return jsonify(Offer.query.get(uid).to_dict())

    elif request.method == 'PUT':
        offer_data_new = json.loads(request.data)
        offer = Offer.query.get(uid)
        offer.id = offer_data_new['id']
        offer.order_id = offer_data_new["order_id"],
        offer.executor_id = offer_data_new["executor_id"]

        db.session.add(offer)
        db. session.commit()
        return '', 204


if __name__ == "__main__":
    app.run()
