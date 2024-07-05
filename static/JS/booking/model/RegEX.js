
export function listenContact(){
  const contactEmail = document.querySelector(".contact-email")
  const contactTelephone = document.querySelector(".contact-telephone")
  contactEmail.addEventListener("input",(e)=>{
    const reEmail = /[A-Za-z0-9]+@+[A-Za-z0-9]+\.+com/;
    if(!reEmail.test(contactEmail.value)){
      contactEmail.style.color = "	#AE0000"
    }else{
      contactEmail.style.color = "	#000000"
    }
  })
  contactTelephone.addEventListener("input",(e)=>{
    const reTelephone = /^09\d{8}$/;
    if(!reTelephone.test(contactTelephone.value)){
      contactTelephone.style.color = "#AE0000"
    }else{
      contactTelephone.style.color = "#000000"
    }
  })
}