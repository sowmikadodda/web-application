

import os
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session, flash
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from pymongo import MongoClient, errors
from datetime import timedelta


# IMPORT SCRAPERS
from amazon import get_amazon_price
from flipkart import FlipkartPriceFetcher  # Your Flipkart class
from snapdeal import get_snapdeal_price    # ← NEW: Snapdeal helper
from meesho import scrape_meesho_lowest_price  # ← NEW: Meesho scraper


# ---------------- CONFIG ----------------
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('FLASK_SECRET_KEY', "super_secret_key")
app.permanent_session_lifetime = timedelta(days=7)


# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



# ---------------- MONGODB ----------------
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'myapp_db')


try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[MONGO_DBNAME]
    users_col = db['users']
except errors.ServerSelectionTimeoutError as e:
    raise RuntimeError(f"Could not connect to MongoDB at {MONGO_URI}. Error: {e}")



# ---------------- LOAD MODEL ----------------
model = MobileNetV2(weights='imagenet')



# ---------------- FLIPKART FETCHER (Global instance) ----------------
FLIPKART_API_KEY = os.environ.get(
    'FLIPKART_API_KEY',
    "0c64bffa3140c19ac328ccb2f02f10c6b7ec8fbfa9e6bd58fd6899a0a6279a2e"
)
flipkart_fetcher = FlipkartPriceFetcher(FLIPKART_API_KEY)



# ---------------- HELPERS ----------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def classify_image(img_path):
    img = Image.open(img_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img = img.resize((224, 224))

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    decoded = decode_predictions(predictions, top=1)
    return decoded



def get_flipkart_price(product_name: str) -> dict:
    try:
        lowest = flipkart_fetcher.get_lowest_price(product_name)
        if lowest:
            return {
                "success": True,
                "price": f"₹{lowest['price']:,.0f}",
                "link": lowest['link'],
                "title": lowest['name'],
                "rating": "N/A",
                "reviews": "N/A",
                "delivery": "Check Flipkart",
                "image": ""
            }
        else:
            return {
                "success": False,
                "price": "No products found",
                "link": "",
                "title": product_name,
                "rating": "N/A",
                "reviews": "0",
                "delivery": "N/A",
                "image": ""
            }
    except Exception as e:
        return {
            "success": False,
            "price": f"Error: {str(e)}",
            "link": "",
            "title": product_name,
            "rating": "N/A",
            "reviews": "0",
            "delivery": "N/A",
            "image": ""
        }



def get_snapdeal_price_wrapped(product_name: str) -> dict:
    """
    Thin wrapper around snapdeal.get_snapdeal_price so its return
    structure matches what index.html expects (same keys as Amazon/Flipkart).
    """
    try:
        data = get_snapdeal_price(product_name)
        # If snapdeal.py already returns in the same format, this just passes it through.
        if not isinstance(data, dict):
            raise ValueError("Snapdeal scraper did not return a dict.")
        # Ensure all expected keys exist
        return {
            "success": bool(data.get("success", False)),
            "price": data.get("price", "No products found"),
            "link": data.get("link", ""),
            "title": data.get("title", product_name),
            "rating": data.get("rating", "N/A"),
            "reviews": data.get("reviews", "N/A"),
            "delivery": data.get("delivery", "Check Snapdeal"),
            "image": data.get("image", "")
        }
    except Exception as e:
        return {
            "success": False,
            "price": f"Error: {str(e)}",
            "link": "",
            "title": product_name,
            "rating": "N/A",
            "reviews": "0",
            "delivery": "N/A",
            "image": ""
        }


# ---------------- NEW: MEESHO HELPER ----------------
def get_meesho_price(product_name: str) -> dict:
    """
    Wrapper for Meesho scraper to match the same format as other scrapers.
    """
    try:
        lowest = scrape_meesho_lowest_price(product_name)
        if lowest:
            return {
                "success": True,
                "price": lowest['price'],
                "link": lowest['link'],
                "title": lowest['name'],
                "rating": lowest['rating'],
                "reviews": lowest['reviews'],
                "delivery": lowest['delivery'],
                "image": ""
            }
        else:
            return {
                "success": False,
                "price": "No products found",
                "link": "",
                "title": product_name,
                "rating": "N/A",
                "reviews": "0",
                "delivery": "N/A",
                "image": ""
            }
    except Exception as e:
        return {
            "success": False,
            "price": f"Error: {str(e)}",
            "link": "",
            "title": product_name,
            "rating": "N/A",
            "reviews": "0",
            "delivery": "N/A",
            "image": ""
        }



# ---------------- AUTH HELPERS ----------------
def login_required(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_mail'):
            flash("Please log in to access that page.", "warning")
            return redirect(url_for('login'))
        return fn(*args, **kwargs)

    return wrapper



# ---------------- ROUTES ----------------
@app.route('/')
def landing():
    if session.get('user_mail'):
        return redirect(url_for('index'))
    return render_template('landing.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    # POST: register user
    name = request.form.get('name', '').strip()
    mail = request.form.get('mail', '').strip().lower()
    age = request.form.get('age', '').strip()
    gender = request.form.get('gender', '').strip()
    address = request.form.get('address', '').strip()
    password = request.form.get('password', '')
    role = request.form.get('role', 'user').strip()

    if not all([name, mail, password]):
        return render_template(
            'signup.html',
            msg="❌ Name, email and password are required.",
            form=request.form
        )

    existing = users_col.find_one({'mail': mail})
    if existing:
        return render_template(
            'signup.html',
            msg="❌ An account with that email already exists.",
            form=request.form
        )

    hashed_pw = generate_password_hash(password)
    user_doc = {
    'name': name,
    'mail': mail,
    'age': age,
    'gender': gender,
    'address': address,
    'password': hashed_pw,
    'role': role   # ✅ ADDED
}

    users_col.insert_one(user_doc)

    session.permanent = True
    session['user_mail'] = mail
    session['user_name'] = name

    flash("✅ Signup successful. You are now logged in.", "success")
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    mail = request.form.get('mail', '').strip().lower()
    password = request.form.get('password', '')

    if not mail or not password:
        return render_template(
            'login.html',
            msg="❌ Provide both email and password.",
            form=request.form
        )

    user = users_col.find_one({'mail': mail})
    if not user or not check_password_hash(user.get('password', ''), password):
        return render_template(
            'login.html',
            msg="❌ Invalid email or password.",
            form=request.form
        )

    session.permanent = True
    session['user_mail'] = user['mail']
    session['user_name'] = user.get('name', '')

    flash("✅ Logged in successfully.", "success")

    # 🔑 ROLE-BASED REDIRECT
    if user.get('role') == 'admin':
        return redirect(url_for('admin_dashboard')
)
    else:
        return redirect(url_for('index'))



@app.route('/logout')
def logout():
    session.clear()
    flash("✅ You have been logged out.", "info")
    return redirect(url_for('landing'))



@app.route('/profile')
@login_required
def profile():
    mail = session.get('user_mail')
    user = users_col.find_one({'mail': mail}, {'_id': 0, 'password': 0})
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for('logout'))
    return render_template('profile.html', user=user)



@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    # Fetch logged-in user
    mail = session.get('user_mail')
    current_user = users_col.find_one({'mail': mail})

    # Allow only admin
    if not current_user or current_user.get('role') != 'admin':
        flash("❌ Admin access only.", "danger")
        return redirect(url_for('index'))

    # Fetch all users (exclude password & _id)
    users = list(
        users_col.find(
            {},
            {
                '_id': 0,
                'name': 1,
                'gender': 1,
                'address': 1,
                'role': 1,
                'age': 1,
                'mail': 1
            }
        )
    )

    return render_template('admin.html', users=users)




@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', msg="❌ No file uploaded")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', msg="❌ No image selected")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # 1) classify image
        try:
            prediction_data = classify_image(filepath)
            predicted_name = prediction_data[0][0][1].replace("_", " ")
        except Exception as e:
            return render_template(
                'index.html',
                msg=f"❌ Error in classification: {e}"
            )

        # 2) Amazon price
        try:
            amazon_data = get_amazon_price(predicted_name)
        except Exception as e:
            amazon_data = {
                "success": False,
                "price": f"❌ Error: {str(e)}",
                "link": "",
                "title": predicted_name,
                "rating": "N/A",
                "reviews": "0",
                "delivery": "N/A",
                "image": ""
            }

        # 3) Flipkart price
        try:
            flipkart_data = get_flipkart_price(predicted_name)
        except Exception as e:
            flipkart_data = {
                "success": False,
                "price": f"❌ Error: {str(e)}",
                "link": "",
                "title": predicted_name,
                "rating": "N/A",
                "reviews": "0",
                "delivery": "N/A",
                "image": ""
            }

        # 4) Snapdeal price
        try:
            snapdeal_data = get_snapdeal_price_wrapped(predicted_name)
        except Exception as e:
            snapdeal_data = {
                "success": False,
                "price": f"❌ Error: {str(e)}",
                "link": "",
                "title": predicted_name,
                "rating": "N/A",
                "reviews": "0",
                "delivery": "N/A",
                "image": ""
            }

        # 5) MEEsHO price (NEW!)
        try:
            meesho_data = get_meesho_price(predicted_name)
        except Exception as e:
            meesho_data = {
                "success": False,
                "price": f"❌ Error: {str(e)}",
                "link": "",
                "title": predicted_name,
                "rating": "N/A",
                "reviews": "0",
                "delivery": "N/A",
                "image": ""
            }

        return render_template(
            'index.html',
            prediction=predicted_name,
            amazon_data=amazon_data,
            flipkart_data=flipkart_data,
            snapdeal_data=snapdeal_data,
            meesho_data=meesho_data,  # ← NEW!
            img_path=filepath,
            msg=(
                "✅ Successfully analyzed image & fetched lowest prices from "
                "Amazon, Flipkart, Snapdeal, and MEEsHO!"
            )
        )

    return render_template(
        'index.html',
        msg="❌ Invalid file type. Allowed: png, jpg, jpeg, gif"
    )



if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )
=======
import os
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
from product_matcher_clean import ProductMatcher

app = Flask(__name__)
app.secret_key = "ai_price_compare_2024_secure_flask_session_key_xyz789"

# ------------ Image Upload Setup ------------
ALLOWED_EXT = {"jpg", "jpeg", "png"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

UPLOAD_FOLDER = "static/products"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ------------ Product Matcher Setup ------------
product_matcher = None

def get_product_matcher():
    global product_matcher
    if product_matcher is None:
        product_matcher = ProductMatcher()
    return product_matcher

# ------------ Database Setup ------------
def connect_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    return conn

# ------------ Routes ------------

@app.route("/")
def index():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = connect_db()
        try:
            conn.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Account created successfully!", "success")
        except:
            return render_template("register.html", error="Username already exists!")

        conn.close()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session["username"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password!")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")
    return render_template("dashboard.html", username=session["username"])

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect("/login")
    return render_template("profile.html", username=session["username"])

@app.route("/home")
def home():
    if "username" not in session:
        return redirect("/login")
    return redirect("/dashboard")

# ------------ PRODUCT COMPARISON PROJECT ------------
@app.route("/project", methods=["GET", "POST"])
def project():
    if "username" not in session:
        return redirect("/login")

    uploaded = None
    product = None
    error = None
    best_deal = None

    if request.method == "POST":
        if "photo" not in request.files:
            error = "No file selected."
            return render_template("project.html", error=error)

        photo = request.files["photo"]

        if photo.filename == "":
            error = "Please choose an image."
            return render_template("project.html", error=error)

        if not allowed(photo.filename):
            error = "Only JPG, JPEG, PNG allowed!"
            return render_template("project.html", error=error)

        # Save file
        filename = secure_filename(photo.filename).lower().replace(" ", "_")
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        photo.save(save_path)

        # Path for browser
        uploaded = f"/static/products/{filename}"

        # Find matching product (always returns something now)
        print(f"🔍 Searching for filename: '{filename}'")
        matcher = get_product_matcher()
        print(f"📋 Available files: {list(matcher.products_db.keys())}")
        matcher = get_product_matcher()
        product = matcher.find_matching_product(filename)
        
        if product:
            # Get best price deal
            best_deal = matcher.get_best_price(product)
            print(f"✅ Product found: {product['name']}")
            if best_deal:
                print(f"💰 Best deal: {best_deal['store']} - {best_deal['price']}")
            else:
                print(f"🔍 Generic search created for: {product['name']}")

    return render_template("project.html", uploaded=uploaded, product=product, error=error, best_deal=best_deal)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ------------ API ENDPOINTS ------------

@app.route("/api/products", methods=["GET"])
def api_get_products():
    """API: Get all products in database"""
    try:
        products = []
        for filename, data in get_product_matcher().products_db.items():
            products.append({
                "filename": filename,
                "name": data["name"],
                "description": data["description"],
                "prices": {
                    "amazon": data["amazon"]["price"],
                    "flipkart": data["flipkart"]["price"]
                },
                "urls": {
                    "amazon": data["amazon"]["url"],
                    "flipkart": data["flipkart"]["url"]
                }
            })
        return jsonify({"success": True, "products": products})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/compare", methods=["POST"])
def api_compare_prices():
    """API: Compare prices for uploaded image"""
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image file provided"})
        
        image = request.files["image"]
        if image.filename == "":
            return jsonify({"success": False, "error": "No image selected"})
        
        if not allowed(image.filename):
            return jsonify({"success": False, "error": "Only JPG, JPEG, PNG allowed"})
        
        # Save image
        filename = secure_filename(image.filename).lower().replace(" ", "_")
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(save_path)
        
        # Find product
        print(f"🔍 API Searching for filename: '{filename}'")
        matcher = get_product_matcher()
        product = matcher.find_matching_product(filename)
        best_deal = matcher.get_best_price(product)
        
        response = {
            "success": True,
            "filename": filename,
            "image_url": f"/static/products/{filename}",
            "product": {
                "name": product["name"],
                "description": product["description"],
                "prices": {
                    "amazon": product["amazon"]["price"],
                    "flipkart": product["flipkart"]["price"]
                },
                "urls": {
                    "amazon": product["amazon"]["url"],
                    "flipkart": product["flipkart"]["url"]
                }
            }
        }
        
        if best_deal:
            response["best_deal"] = {
                "store": best_deal["store"],
                "price": best_deal["price"],
                "url": best_deal["url"],
                "savings": best_deal["savings"]
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/product/<filename>", methods=["GET"])
def api_get_product(filename):
    """API: Get specific product by filename"""
    try:
        matcher = get_product_matcher()
        product = matcher.find_matching_product(filename)
        if product:
            best_deal = matcher.get_best_price(product)
            response = {
                "success": True,
                "filename": filename,
                "product": {
                    "name": product["name"],
                    "description": product["description"],
                    "prices": {
                        "amazon": product["amazon"]["price"],
                        "flipkart": product["flipkart"]["price"]
                    },
                    "urls": {
                        "amazon": product["amazon"]["url"],
                        "flipkart": product["flipkart"]["url"]
                    }
                }
            }
            if best_deal:
                response["best_deal"] = {
                    "store": best_deal["store"],
                    "price": best_deal["price"],
                    "url": best_deal["url"],
                    "savings": best_deal["savings"]
                }
            return jsonify(response)
        else:
            return jsonify({"success": False, "error": "Product not found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/flipkart/<filename>", methods=["GET"])
def api_get_flipkart_product(filename):
    """API: Get Flipkart-specific product data"""
    try:
        product = product_matcher.find_matching_product(filename)
        if product:
            return jsonify({
                "success": True,
                "filename": filename,
                "flipkart": {
                    "name": product["name"],
                    "description": product["description"],
                    "price": product["flipkart"]["price"],
                    "url": product["flipkart"]["url"],
                    "store": "Flipkart"
                }
            })
        else:
            return jsonify({"success": False, "error": "Product not found on Flipkart"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/flipkart/search/<query>", methods=["GET"])
def api_flipkart_search(query):
    """API: Search products on Flipkart"""
    try:
        results = []
        for filename, data in product_matcher.products_db.items():
            if query.lower() in data["name"].lower() or query.lower() in data["description"].lower():
                results.append({
                    "filename": filename,
                    "name": data["name"],
                    "price": data["flipkart"]["price"],
                    "url": data["flipkart"]["url"]
                })
        return jsonify({"success": True, "flipkart_results": results, "query": query})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    print("🚀 Starting Price Comparison Application...")
    print("📱 Upload product images to compare prices!")
    print("💡 Add products to static/products/product_database.txt")
    print("\n🔗 API Endpoints:")
    print("   GET  /api/products - Get all products")
    print("   POST /api/compare - Upload image for price comparison")
    print("   GET  /api/product/<filename> - Get specific product")
    app.run(debug=True)

