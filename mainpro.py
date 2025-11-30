import qrcode

def get_user_input_text():
    text=input("enter your text:")
    return text

def get_user_input_url():
    url = input("Enter your URL:")
    if not url.startswith("http"):
        url = "http://" + url
    else:
        url = url
    return url

def get_contact_info():
    name=input("enter your name:")
    
    
    while True:
        email=input("enter your email:")
        phone=input("enter your phone number:")
        valid=True

        if not email.endswith(".com"):
            print("invalid email")
            valid=False
        if len(phone)!=10 or not phone.isdigit():
            print("invalid phone number")
            valid=False
        if valid:
            break
    
    contact=f"name:{name} \n email: {email} \n phone no: {phone}"

    return contact

def generate_qr(data):
    img=qrcode.make(data)
    return img

def handle_output(img):
    print("1. view only")
    print("2. save only")
    print("3. view and save")
    choice=input("enter your choice:")

    if choice=="1":
        img.show()
    elif choice=="2":
        filename=input("enter the file name u want to save(.png):")
        img.save(filename)
    elif choice=="3":
        img.show()
        filename=input("enter the file name u want to save(.png):")
        img.save(filename)
    else:
        print("invalid choice")

def main():
    while True:
        print("===QR code generator===")
        print("1. QR code from text")
        print("2. QR code from url")
        print("3. QR code from contact info")
        print("4. exit")
        choice = input("Enter your choice:")

        if choice == "1":
            data = get_user_input_text()
            image=generate_qr(data)
            handle_output(image)
        elif choice=="2":
            url=get_user_input_url()
            image=generate_qr(url)
            handle_output(image)
        elif choice=="3":
            contact=get_contact_info()
            image=generate_qr(contact)
            handle_output(image)
        elif choice=="4":
            print("Exiting the program")
            break
        else:
            print("invalid choice!!")
    
main()