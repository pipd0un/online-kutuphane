from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/rez/Masaüstü/kutuphane/kutuphane.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    kitaplar=Kitap.query.all()
    return render_template("index.html" , kitaplar=kitaplar)
@app.route("/add" , methods=["POST"])
def add_book():
    kitap_adi=request.form.get("kitap_adi")
    yazar=request.form.get("yazar")
    yayinevi=request.form.get("yayinevi")
    kategori=request.form.get("kategori")
    konum=request.form.get("konum")
    if "0547"==str(request.form.get("sifre")):
        kitap_ekle=Kitap(kitap_adi=kitap_adi,yazar=yazar,yayinevi=yayinevi,kategori=kategori,konum=konum)
        db.session.add(kitap_ekle)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

@app.route("/guncelle/<string:id>",methods=["GET"])
def guncelle(id=id):
    kitap=Kitap.query.filter_by(id=id).first()
    return render_template("guncelle.html",kitap=kitap)

@app.route("/update/<string:id>",methods=["POST","GET"])
def update(id):
    kitap=Kitap.query.filter_by(id=id).first()
    kitap.kitap_adi=request.form.get("kitap_adi")
    kitap.yazar=request.form.get("yazar")
    kitap.yayinevi=request.form.get("yayinevi")
    kitap.kategori=request.form.get("kategori")
    kitap.konum=request.form.get("konum")
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/sil/<string:id>",methods=["GET"])
def sil(id):
    kitap=Kitap.query.filter_by(id=id).first()
    db.session.delete(kitap)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/detay/<string:id>")
def detay(id):
    kitap=Kitap.query.filter_by(id=id).first()
    return render_template("detay.html",kitap=kitap)

class Kitap(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    kitap_adi=db.Column(db.String(80))
    yazar=db.Column(db.String(40))
    yayinevi=db.Column(db.String(20))
    kategori=db.Column(db.String(30))
    konum=db.Column(db.String(25))
    ozet=db.Column(db.Text)

    """
    id = db.Column(db.Integer, primary_key=True)
    kitap_adi = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)"""

if __name__=="__main__":
    app.run(debug=True)