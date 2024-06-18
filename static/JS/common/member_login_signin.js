const body = document.body;

export function appendMask() {
  const pageMask = document.createElement("div");
  pageMask.className = "page-mask";
  body.appendChild(pageMask);
  pageMask.style.display="block";
}

export  function appendMemberPage() {
  const memberPage = document.createElement("section");
  memberPage.className = "member_in_page";
  body.appendChild(memberPage);
}

export function insertSignUpPage() {
  const memberInPage = document.querySelector(".member_in_page");
  memberInPage.innerHTML = '<div class="decorator-bar"></div>'+
    '<div class="page-container">'+
       '<button class="member-close-btn"><img class="close" src="/static/img/icon_close.png" alt=""></button>'+
      '<p class="member-in-page-title">註冊會員帳號</p>'+
        '<div class="input-container">'+
          '<input id="name" class="member-input" type="text" name="name" placeholder="輸入姓名">'+
          '<input id="email" class="member-input" type="text" name="email" placeholder="輸入電子郵件">'+
          '<input id="password" class="member-input" type="password" name="password" placeholder="輸入密碼">'+
          '<input type="button" class="signup-submit submit-btn" value="註冊新帳戶">'+
          '<div class = "response-message"></div>'+
        '</div>'+
      '<div class="switch-line">'+
        '<div>已經有帳戶?</div>'+
        '<div class="switch-signin switch-btn">點此登入</div>'+
      '</div>'+
    '</div>';
};

export function insertSignInPage() {
  const memberInPage = document.querySelector(".member_in_page");
  memberInPage.innerHTML = '<div class="decorator-bar"></div>'+
    '<div class="page-container">'+
      '<button class="member-close-btn"><img class="close" src="/static/img/icon_close.png" alt=""></button>'+
      '<p class="member-in-page-title">登入會員帳號</p>'+
        '<div class="input-container">'+
          '<input id="email" class="member-input" type="text"  name="email" placeholder="輸入電子信箱">'+
          '<input id="password" class="member-input" type="password"  name="password" placeholder="輸入密碼">'+
          '<input type="button" class="signin-submit submit-btn" value="登入帳戶">'+
          '<div class = "response-message"></div>'+
        '</div>'+
      '<div class="switch-line">'+
        '<div>還沒有帳戶?</div>'+
        '<div class="switch-signup switch-btn">點此註冊</div>'+
      '</div>'+
    '</div>';
};

export function BtnEvent() {
  const memberInPage = document.querySelector(".member_in_page");
  memberInPage.addEventListener("click",(e)=>{  
    let content = e.target.classList;
    switch (true){
      case content.contains("switch-signup"):
        insertSignUpPage();
        break;
      case content.contains("switch-signin"):
        insertSignInPage();
        break;
      case content.contains("close"):
        closeMemberPage ();
        break;
      case content.contains("signin-submit"):
            signInMember();
        break;
      case content.contains("signup-submit"):
            signUpMember();
        break;
    };
  });
};

function closeMemberPage() {
  const pageMask = document.querySelector(".page-mask");
  const memberInPage = document.querySelector(".member_in_page");
  pageMask.remove();
  memberInPage.remove();
};

export function submitEvent(){
  const memberInPage = document.querySelector(".member_in_page");
  memberInPage.addEventListener("keydown",(e)=>{  
    const submitBtnClass = document.querySelector(".submit-btn").classList;
    if(e.key === "Enter"){
      switch (true){
        case submitBtnClass.contains("signin-submit"):
            signInMember();
          break;
        case submitBtnClass.contains("signup-submit"):
            signUpMember();
          break;
      };
    }
  });
};

async function signUpMember() {
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

async function signInMember() {
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

export function addMemberInPageListener(){
  const memberInBtn = document.querySelector("#member-in-btn")
  memberInBtn.addEventListener("click", (e)=>{
  let memberInBTNclassList = memberInBtn.classList
  if(memberInBTNclassList.contains("signed")){
      localStorage.removeItem("userState");
      location.reload();
    }else{
      appendMask();
      appendMemberPage();
      insertSignInPage();
      BtnEvent();
      submitEvent();
    };
  });
}
