from flask import Flask,flash, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.secret_key = 'random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class productDetail(db.Model):
    ProductId = db.Column(db.Integer, primary_key = True)
    ProductImage = db.Column(db.String(400),nullable= False)
    ProductName = db.Column(db.String(200),nullable = False)
    ProductRate = db.Column(db.Float,nullable = False)
    ProductDis =  db.Column(db.String(600),nullable = False)

    def __repr__(self):
        return 'Product '+ str(self.ProductId)

class userDetail(db.Model):
    UserId = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(50), nullable = False)
    UserEmail = db.Column(db.String(100), nullable = False)
    UserPassword = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return 'User '+ str(self.UserId)


@app.route('/')
def index():
    allProduct = productDetail.query.all()
    return render_template('home.html',datasend = allProduct  )

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/productsDetail/<int:Id>', methods = ['GET','POST'])
def productsD(Id):
    Product_Detail = productDetail.query.get_or_404(Id)
    return render_template('product-details.html', pd = Product_Detail)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/res',methods=['GET','POST'])
def log():
    error = None
    if request.method == 'POST':
        user_Name = request.form['name']
        user_Email = request.form['email']
        user_Password = request.form['password']
        userConformPassword = request.form['conformPass']
        print(user_Email, file=sys.stderr)
        if user_Name == userConformPassword:
            newUser = userDetail(UserName = user_Name, UserEmail = user_Email , UserPassword = user_Password)
            db.session.add(newUser)
            db.session.commit()
            error = user_Name+" in the house!!!"
            return render_template('login.html',error = error) 
        else:
            error = 'Password Does Not Match'
            return render_template('res.html',error = error) 
    else:
        print('Hello world!', file=sys.stderr)
        return render_template('res.html')

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == "POST":
        user_Email = request.form['email']
        user_Password = request.form['password']
        print('Hello world!>>>>>>>>>>>>>>>>>>>>', file=sys.stderr)
        login = userDetail.query.filter_by(UserEmail=user_Email, UserPassword=user_Password).first()
        if login is not None:
            return redirect("/")
        else:
            error = "Bro handel you shit"
            return render_template('login.html',error = error)
    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)