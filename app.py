#comments for your understanding of the code

from flask import Flask, flash, redirect, render_template, request, url_for #flask is for deployment of a website
import qrcode #for generating qr code
import qrcode.constants
from qrcode.image.styledpil import StyledPilImage #custom styling
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, RoundedModuleDrawer, CircleModuleDrawer
) # for qr shape 
from qrcode.image.styles.colormasks import SolidFillColorMask
import os #for saving the file
from werkzeug.utils import secure_filename 
import cv2
from werkzeug.security import generate_password_hash, check_password_hash #for password hashing
from model import db, user, QRcodes #importing the database and models
from config import Config #importing the config file
from flask_login import LoginManager,login_user, logout_user,login_required,current_user
import uuid #for unique file name for each qr saved 


def hex_to_rgb(value): #to change hex to rgb in colors
    value=value.lstrip("#")
    lv=len(value)
    return tuple(int(value[i:i+lv//3],16) for i in range(0,lv,lv//3)) # convert hex to rgb return it as a tuple it will divide into 3 r,g,b

app=Flask(__name__) # create a new instance of the Flask class
app.config.from_object(Config)   # Load settings from config.py

db.init_app(app)

login=LoginManager()
login.init_app(app)
login.login_view="login"

#login_manager user_loader
@login.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


# Create tables once
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html') #to render the index.html file

#qr making
@app.route('/generate', methods=['POST']) #to handle the POST request

def generate():
    qr_type=request.form.get('type') #to get type from forms

    if qr_type=="text":
        data=request.form['data']
    elif qr_type=="url":
        data=request.form['data']
        if not data.startswith("http"):
            data="http://"+data
        else:
            data=data
    elif qr_type=="contact_info":
        name=request.form['name']
        phone=request.form['number']
        email=request.form['email']

        contact=f"name: {name}\n phone: {phone} \n email: {email}"

        data=contact
    elif qr_type=="email":
        data=request.form['data']
    
    style=request.form.get('style') #qr styles
    fg_color=request.form.get('fg-color') or '#000000'
    bg_color=request.form.get('bg-color') or '#ffffff'
    print(fg_color)
    fg_color_hex=hex_to_rgb(fg_color)
    bg_color_hex=hex_to_rgb(bg_color)

    if style=="circle":
        module_drawer= CircleModuleDrawer()
    elif style=="rounded":
        module_drawer= RoundedModuleDrawer()
    else:
        module_drawer= SquareModuleDrawer()

    logo_path=None
    
    if 'logo' in request.files:
        logo_file=request.files['logo'] #getting the file from the form
        filename=secure_filename(logo_file.filename) #to get a safe version of the filename before saving it.
        if logo_file and logo_file.filename!="":
            upload_folder='static/uploads'
            os.makedirs(upload_folder,exist_ok=True)
            logo_path=os.path.join(upload_folder,filename)
            logo_file.save(logo_path)
    

    qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    ) # qr size and border size

    qr.add_data(data) #add data to qr code
    qr.make(fit=True) #make qr code

    img=qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        color_mask=SolidFillColorMask(back_color=bg_color_hex, front_color=fg_color_hex),
        embeded_image_path=logo_path
    ) # add color and shape 

    #image_factory = how we want to make the image 
    #module_drawer = shape of pixels
    #color_mask = colors
    #embeded_image_path = put a logo at the center

    filename=f"{uuid.uuid4().hex}.png"  #generate unique name
    file_path=os.path.join('static/qrs',filename)

    img.save(file_path) # save qr image

    if current_user.is_authenticated:
        new_qr = QRcodes(
            data=data,
            image_path=file_path,
            user_id=current_user.id
        )
        db.session.add(new_qr)
        db.session.commit()

    return render_template("index.html", qr_image='/'+file_path)

#qr decoding
@app.route('/decode',methods=['GET','POST'])
def decodeing():
    decode_data=[]
    if request.method=='POST':
        qr_file=request.files['input-qr']
        if qr_file and qr_file.filename!="":
            qr_path=os.path.join('static/uploads_input',qr_file.filename) #save temp in upload_input folder
            os.makedirs('static/uploads_input',exist_ok=True)
            qr_file.save(qr_path)

            img=cv2.imread(qr_path) 
            decode=cv2.QRCodeDetector() 
            data,array,_=decode.detectAndDecode(img) 
            if array is not None:
                decode_data.append(data)
            
   
    return render_template('index.html', decode_data=decode_data)# to show the data in the webpage

#Read image file from disk -> Try to detect QR -> If found, decode data -> Store decoded text



#for login
@app.route("/login", methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        user_obj=user.query.filter_by(username=username).first()  #gives the first match

        if user_obj and check_password_hash(user_obj.password,password): #to change hash to orginal password
            login_user(user_obj)
            flash("Login successfully!!!")
            return redirect(url_for('dashboard'))
        else:
            flash("invalid username or password!!!")

    return render_template("login.html")

#for logout
@app.route("/logout")
def logout():
    logout_user()
    flash("Logout successfully!!!")
    return render_template("login.html")




#for signup

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        existing=user.query.filter_by(username=username).first()
        if existing:
            return render_template("signup.html",message="user already exists")

        #password hashing
        hashed=generate_password_hash(password)

        #adding in database
        new_user=user(username=username,password=hashed)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')
    return render_template("signup.html")


#for cuurent user
@app.route("/dashboard")
@login_required #to protect
def dashboard():
    qrs=QRcodes.query.filter_by(user_id=current_user.id).all() # to display all the qr for the user
    return render_template("dashboard.html",user=current_user,qrs=qrs)


#for deleting the qr in dashboard
@app.route('/delete_qr/<int:id>',methods=['POST'])
def delete_qr(id):
    qr=QRcodes.query.get_or_404(id) #to get the qr and checks whether it is there not 


    if qr.user_id != current_user.id: #if not user then
        flash("You are not authorised!")
        return redirect(url_for('dashboard'))

    if os.path.exists(qr.image_path): #
        os.remove(qr.image_path)

    db.session.delete(qr)
    db.session.commit()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=False)

