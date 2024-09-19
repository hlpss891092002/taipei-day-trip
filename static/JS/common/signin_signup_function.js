import{sentFetchWithBody} from "./sent_fetch_get_response.js"

export async function signUpMember() {
  try{
    const responseMessage = document.querySelector(".response-message")
    const name = document.querySelector("#name").value
    const email = document.querySelector("#email").value
    const password = document.querySelector("#password").value
    const reEmail = /[A-Za-z0-9]+@+[A-Za-z0-9]+\.+com/
    const rePassword = /(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$!%*?&]).{8,}/ 
    
    switch (true){
      case !email ||  !password || !name:
        responseMessage.classList.remove("success")
        responseMessage.innerText = "請填寫註冊資料"
        return
      case !reEmail.test(email) :
        responseMessage.innerText = "請輸入正確電子郵件"
        return
      case !rePassword.test(password) :
        responseMessage.innerText = "密碼必須包含數字、大小寫英文字母、及特殊符號(@$!%*?&)且長度大於8"
        return
      case email  &&  password && name && reEmail.test(email) :
       const body = {
        "name": `${name}`,
        "email": `${email}`,
        "password": `${password}`
      }
      let response = await sentFetchWithBody("post", body, "/api/user")
      let responseJSON = await response
      console.log(responseJSON)
      if (responseJSON["ok"]){
        responseMessage.classList.toggle("success")
        responseMessage.innerText = "註冊成功，請至登入頁面登入"
        document.querySelector("#name").value = "";
        document.querySelector("#email").value = "";
        document.querySelector("#password").value = "";
      }else{
        responseMessage.classList.remove("success")
        responseMessage.innerText = responseJSON["message"]
      }
    }

  }catch{
    console.log("loading signup popup page fail")
  }

};

export async function signInMember() {
  try{
    const responseMessage = document.querySelector(".response-message")
    const email = document.querySelector("#email").value
    const reEmail = /[A-Za-z0-9]+@+[A-Za-z0-9]+\.+com/
    console.log(reEmail.test(email))
    const password = document.querySelector("#password").value

    switch (true){
      case !email ||  !password:
        responseMessage.classList.remove("success")
        responseMessage.innerText = null
        return
      case !reEmail.test(email) :
        responseMessage.innerText = "請輸入正確電子郵件"
        return
      case email  &&  password && reEmail.test(email) :
        const body = {
          "email": `${email}`,
          "password": `${password}`
        }
        const response = await sentFetchWithBody("put", body, "/api/user/auth")
        const responseJSON = await response
        if (responseJSON["token"]){     
          localStorage.setItem("userState", `${responseJSON["token"]}`)
          responseMessage.classList.add("success")
          responseMessage.innerText = "登入成功，重新載入頁面"
          location.reload()
        }else{
          responseMessage.classList.remove("success")
          responseMessage.innerText = responseJSON["message"]
        }
    }
  }catch{
    console.log("loading signin popup page fail")
  }
  
};

