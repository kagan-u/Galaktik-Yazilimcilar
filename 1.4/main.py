from flask import Flask, render_template, session, request, jsonify

app = Flask(__name__)
app.secret_key = 'yilbasi_dukkani_secret_key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sepetim')
def sepetim():
    return render_template('sepetim.html')

@app.route('/sanscarki')
def sanscarki():
    return render_template('sanscarki.html')

@app.route('/urunler')
def urunler():
    return render_template('urunler.html')

# allow old/explicit .html link to work from product pages
@app.route('/urunler.html')
def urunler_html():
    return render_template('urunler.html')

@app.route('/trend')
def trend():
    return render_template('trend.html')


# --- product detail routes for static product pages ---
@app.route('/urun_yilbasi_agaci')
@app.route('/urun_yilbasi_agaci.html')
def urun_yilbasi_agaci():
    return render_template('urun_yilbasi_agaci.html')

@app.route('/urun_kirmizi_kurdele')
@app.route('/urun_kirmizi_kurdele.html')
def urun_kirmizi_kurdele():
    return render_template('urun_kirmizi_kurdele.html') 

@app.route('/urun_altin_yildiz')
@app.route('/urun_altin_yildiz.html')
def urun_altin_yildiz():
    return render_template('urun_altin_yildiz.html')

@app.route('/urun_gumus_can')
@app.route('/urun_gumus_can.html')
def urun_gumus_can():
    return render_template('urun_gumus_can.html')

@app.route('/urun_yildiz_feneri')
@app.route('/urun_yildiz_feneri.html')
def urun_yildiz_feneri():
    return render_template('urun_yildiz_feneri.html')

@app.route('/urun_kardan_adam')
@app.route('/urun_kardan_adam.html')
def urun_kardan_adam():
    return render_template('urun_kardan_adam.html')

@app.route('/urun_yilbasi_corabi')
@app.route('/urun_yilbasi_corabi.html')
def urun_yilbasi_corabi():
    return render_template('urun_yilbasi_corabi.html')

@app.route('/urun_renkli_ampul_seti')
@app.route('/urun_renkli_ampul_seti.html')
def urun_renkli_ampul_seti():
    return render_template('urun_renkli_ampul_seti.html')


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    name = data['name']
    price = data['price']
    cart = session.get('cart', [])
    existing = next((item for item in cart if item['name'] == name), None)
    if existing:
        existing['quantity'] += 1
    else:
        cart.append({'name': name, 'price': price, 'quantity': 1})
    session['cart'] = cart
    return jsonify({'success': True})

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    name = data['name']
    cart = session.get('cart', [])
    cart = [item for item in cart if item['name'] != name]
    session['cart'] = cart
    return jsonify({'success': True})

@app.route('/increase_quantity', methods=['POST'])
def increase_quantity():
    data = request.get_json()
    name = data['name']
    cart = session.get('cart', [])
    existing = next((item for item in cart if item['name'] == name), None)
    if existing and existing['quantity'] < 30:
        existing['quantity'] += 1
    session['cart'] = cart
    return jsonify({'success': True})

@app.route('/decrease_quantity', methods=['POST'])
def decrease_quantity():
    data = request.get_json()
    name = data['name']
    cart = session.get('cart', [])
    existing = next((item for item in cart if item['name'] == name), None)
    if existing:
        existing['quantity'] -= 1
        if existing['quantity'] <= 0:
            cart = [item for item in cart if item['name'] != name]
    session['cart'] = cart
    return jsonify({'success': True})

@app.route('/get_cart')
def get_cart():
    cart = session.get('cart', [])
    return jsonify(cart)

@app.route('/iletisim', methods=['GET'])
@app.route('/contact', methods=['GET'])
def iletisim():
    return render_template('iletisim.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json(silent=True)
    if not data:
        data = request.form.to_dict()
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    message = (data.get('message') or '').strip()
    if not name or not message:
        return jsonify({'success': False, 'error': 'Ad ve mesaj gereklidir.'}), 400
    # Burada isterseniz mesajı veritabanına kaydedin veya e-posta gönderin
    print(f'Yeni iletişim mesajı: {name} <{email}> - {message}')
    return jsonify({'success': True, 'message': 'Mesajınız alındı. Teşekkürler.'})

@app.route('/product')
def product():
    return render_template('product.html')

# support legacy /product.html links (preserve query string)
@app.route('/product.html')
def product_html():
    # render the same template as /product; template can read request.args
    return render_template('product.html')

if __name__ == '__main__':
    app.run(debug=True)
