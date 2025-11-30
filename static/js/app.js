const theme=document.querySelector("#theme-switch");
const body=document.querySelector("body");
let currmode="light";

//seeing the saved theme after reload
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
    currmode = "dark";
    body.classList.add("darktheme");
    body.classList.remove("light");
} else {
    currmode = "light";
    body.classList.add("light");
    body.classList.remove("darktheme");
}

theme.addEventListener("click", function (){
    if(currmode=="light"){
        currmode="dark";
        body.classList.add("darktheme");
        body.classList.remove("light");
        localStorage.setItem("theme","dark");
    }
    else{
        currmode="light";
        body.classList.add("light");
        body.classList.remove("darktheme");
        localStorage.setItem("theme","light");
    }
})

document.addEventListener("DOMContentLoaded",function(){
    const contact=document.querySelector(".contact");
    const options=document.querySelectorAll(".type-options");
    const inputtext=document.querySelector(".input-text");
    const inputurl=document.querySelector(".input-url")
    const inputemail=document.querySelector(".input-email")
    const form=document.querySelector(".form");
    const qrTypeInput=document.getElementById("selected-type")

    options.forEach(button => {
        button.addEventListener("click", function () {
            const type = this.getAttribute("data-type");
            qrTypeInput.value = type;

            options.forEach(btn => btn.classList.remove("active"));//for showing the selected button seperatedly
            this.classList.add("active");

            if (type=="contact_info"){
                contact.style.display="block";
                inputtext.style.display="none";
                inputurl.style.display="none";
                inputemail.style.display="none";
            }
            else if(type=="url"){
                contact.style.display="none";
                inputtext.style.display="none";
                inputurl.style.display="block";
                inputemail.style.display="none";
            }
            else if(type=="email"){
                contact.style.display="none";
                inputtext.style.display="none";
                inputurl.style.display="none";
                inputemail.style.display="block";
            }
            else{
                contact.style.display="none";
                inputtext.style.display="block";
                inputurl.style.display="none";
                inputemail.style.display="none";
            }
        });
    });
    /*options.forEach(radio =>{
        radio.addEventListener("change",function (){
            if(this.value=="contact_info"){
                contact.style.display="block";
                input.style.display="none";
            }
            else{
                contact.style.display="none";
                input.style.display="block";
            }
        })
    })*/

    form.addEventListener("submit",function (e){
        const selected=document.querySelector("input[name='type']:checked").value;

        if(selected=="text" || selected=="url"){
            const value=document.querySelector("input[name='data']").value.trim();
            if(value==""){
                alert("please enter the"+selected);
                e.preventDefault();
            }
        }
        if(selected=="contact_info"){
            const name=document.querySelector("input[name='name']").value.trim();
            const email=document.querySelector("input[name='email']").value.trim();
            const phone=document.querySelector("input[name='number']").value.trim();

            
            if (name=="" || email=="" || phone==""){
                alert("please enter the contact info");
                e.preventDefault();
            }
            else if(phone.length!=10){
                alert("length off the phone should be in 10 digits");
                e.preventDefault();
            }
        }
    })
})

/*const overlay=document.querySelector(".overlay");
document.addEventListener("mousemove", (e) => {
    const x=e.clientX;
    const y=e.clientY;
    
    let color = body.classList.contains("darktheme") ? "rgba(255,255,255,0.15)" : "rgba(0,0,0,0.15)";
    overlay.style.background= `radial-gradient(circle at ${x}px ${y}px, ${color}, transparent 80%)`;

})*/

const text="QR CODE GENERATOR";
const type=document.getElementById("typewriter");
let i=0;

function typeWriter() {
    if(i<text.length){
        type.innerHTML+=text.charAt(i);
        i++;
        setTimeout(typeWriter,100);
    }
}
typeWriter();

document.addEventListener("DOMContentLoaded",function(){
    const nav=document.querySelectorAll(".nav");
    const home=document.querySelector(".home");
    const code=document.querySelector(".layout");
    const decode=document.querySelector(".decode")

    let savedpage=localStorage.getItem("page")
    if(savedpage=="home"){
        home.style.display="block";
     
        code.style.display="none";
        decode.style.display="none";
    }
    else if(savedpage=="code"){
        home.style.display="none";
        code.style.display="flex";
        decode.style.display="none";
    }
    else if(savedpage=="decode"){
        home.style.display="none";
        code.style.display="none";
        decode.style.display="flex";
    }

    nav.forEach(button =>{
        button.addEventListener("click",function(){
            const type=this.getAttribute("type-page");
            if (type=="home"){
                home.style.display="block";
            
                code.style.display="none";
                decode.style.display="none";
                localStorage.setItem("page","home");
            }else if (type === "code") {
                home.style.display = "none";
                code.style.display="flex";
                decode.style.display="none";
                localStorage.setItem("page","code");
            }else if(type=="decode"){
                home.style.display="none";
                code.style.display="none";
                decode.style.display="flex";
                localStorage.setItem("page","decode");
            }
        })
    })
    document.querySelector('.logo').addEventListener('click', function(e) {
        e.preventDefault();
        
        home.style.display = "block";
        code.style.display = "none";
        decode.style.display = "none";
        localStorage.setItem("page", "home");
    });

    

        

})

