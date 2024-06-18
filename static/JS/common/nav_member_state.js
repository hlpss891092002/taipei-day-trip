export function switchNavToSignedIn(){
  const memberBtn = document.querySelector("#member-in-btn")
  memberBtn.innerHTML = "登出系統"
  memberBtn.classList.toggle("signed")
}

export function switchNavToUnsigned(){
  const memberBtn = document.querySelector("#member-in-btn")
  memberBtn.innerHTML = "登入/註冊"
  memberBtn.classList.remove("signed")
}

