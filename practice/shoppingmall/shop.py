from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'hello1234'

users = [
    {'name': 'hi', 'id': 'hi', 'pw':'1234'}
]

items = [
    {'id': '1', 'name': 'apple', 'price': 1000},
    {'id': '2', 'name': 'banana', 'price': 2000},
    {'id': '3', 'name': 'cherry', 'price': 3000}
]

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    user = session.get('user')

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']

        user = None
        for u in users:
            if u['id'] == id and u['pw'] == pw:
                user = u
                break

        if user:
            session['user'] = user
            return redirect(url_for('index'))
        else:
            error = "Invalid ID or PW"
            return render_template('login.html', error=error)

    return render_template('login.html', user=user)

@app.route('/logout')
def logout():
    # 로그아웃 시 세션에서 유저 정보 제거
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/product')
def product():
    last_added = session.pop('last_added_item', None)

    return render_template('product.html', cart_items=items, last_added=last_added)

@app.route('/add-to-cart/<item_id>')
def add_to_cart(item_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if 'cart' not in session:
        session['cart'] = {}

    if item_id in session['cart']:
        session['cart'][item_id] += 1
    else:
        session['cart'][item_id] = 1

    added_item = next((i for i in items if i['id'] == item_id), None)
    if added_item:
        session['last_added_item'] = added_item['name']

    session.modified = True
    return redirect(url_for('product'))

@app.route('/cart')
def cart():
    cart_items = {}
    total_price = 0

    for item_id, quantity in session.get('cart', {}).items():
        item = next((i for i in items if i['id'] == item_id), None)
        cart_items[item_id] = {
            'name': item['name'],
            'quantity': quantity,
            'price': item['price']
        }
        total_price += item['price'] * quantity

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route("/remove-from-cart/<item_id>")
def remove_from_cart(item_id):

    cart = session.get("cart", {})

    # 상품 삭제
    if item_id in cart:
        del cart[item_id]

    session["cart"] = cart

    return redirect("/cart")

@app.route("/clear-cart")
def clear_cart():

    session["cart"] = {}

    return redirect("/cart")

if __name__ == "__main__":
    app.run(debug=True)
