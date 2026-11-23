from flask import Flask, render_template, request, jsonify, redirect, url_for
import database as dbase
from product import Product

db = dbase.dbConnection()

app = Flask(__name__)

# Ruta principal (READ)
@app.route("/")
def home():
    products = db["products"]
    productsReceived = products.find()
    return render_template("index.html", products=productsReceived)

# Ruta para agregar productos (CREATE)
@app.route("/products", methods=["POST"])
def addProduct():
    products = db["products"]
    name = request.form["name"]
    price = request.form["price"]
    quantity = request.form["quantity"]

    if name and price and quantity:
        product = Product(name, price, quantity)
        products.insert_one(product.toDBCollection())
        return redirect(url_for("home"))
    else:
        return notFound()

# Ruta para eliminar productos (DELETE)
@app.route("/delete/<string:product_name>")
def delete(product_name):
    products = db["products"]
    products.delete_one({"name": product_name})
    return redirect(url_for("home"))

# Ruta para editar productos (UPDATE)
@app.route("/edit/<string:product_name>", methods=["POST"])
def edit(product_name):
    products = db["products"]
    name = request.form["name"]
    price = request.form["price"]
    quantity = request.form["quantity"]

    if name and price and quantity:
        products.update_one(
            {"name": product_name},
            {"$set": {"name": name, "price": price, "quantity": quantity}}
        )
        return redirect(url_for("home"))
    else:
        return notFound()

# Manejador de error 404
@app.errorhandler(404)
def notFound(error=None):
    message = {
        "message": "No encontrado " + request.url,
        "status": "404 Not Found"
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True, port=4000)