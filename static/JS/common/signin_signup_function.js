export async function signUpMember() {
  try{
    const responseMessage = document.querySelector(".response-message")
    const name = document.querySelector("#name").value
    const email = document.querySelector("#email").value
    const password = document.querySelector("#password").value
    if(email && name && password){ 
      const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
      }
      const body = {
        "name": `${name}`,
        "email": `${email}`,
        "password": `${password}`
      }
      let response = await fetch("/api/user",{
        method:"POST",
        headers: headers,
        body: JSON.stringify(body)
      })

      let responseJSON = await response.json()
      if (responseJSON["ok"]){
        responseMessage.classList.toggle("success")
        responseMessage.innerText = "註冊成功，請至登入頁面登入"
      }else if (responseJSON["error"]){
        responseMessage.classList.remove("success")
        responseMessage.innerText = responseJSON["message"]
      }
    }else{
      responseMessage.classList.remove("success")
      responseMessage.innerText = "請確實填寫資料"
    }
  }catch{
    console.log("loading signup popup page fail")
  }

};

export async function signInMember() {
  try{
    const responseMessage = document.querySelector(".response-message")
    const email = document.querySelector("#email").value
    const password = document.querySelector("#password").value
    if(email && password){ 
      const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
      }
      const body = {
        "email": `${email}`,
        "password": `${password}`
      }
      let response = await fetch("/api/user/auth",{
        method:"PUT", 
        headers: headers,
        body: JSON.stringify(body)
      })

      let responseJSON = await response.json()
      if (responseJSON["token"]){     
        localStorage.setItem("userState", `${responseJSON["token"]}`)
        responseMessage.classList.add("success")
        responseMessage.innerText = "登入成功，重新載入頁面"
        location.reload()
      }else{
        responseMessage.classList.remove("success")
        responseMessage.innerText = responseJSON["message"]
      }
    }else{
      responseMessage.classList.remove("success")
      responseMessage.innerText = "請確實填寫資料"
    } 
  }catch{
    console.log("loading signin popup page fail")
  }
  
};
