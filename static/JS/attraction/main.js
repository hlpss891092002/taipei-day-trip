import {insertInfoData} from "./info.js"
import {profile} from "./cover_section_profile.js"
import {insertSliceImage, sliceLeft, sliceRight, selectCount} from "./cover_section_slideshow.js"
import {appendMask, appendMemberPage, insertSignInPage, insertSignUpPage, BtnEvent, submitEvent, addMemberInPageListener, addListenerOnBooking} from "../common/member_sign_page.js"
import {fetchAttractionAPI} from "../common/fetch_api_location_path.js"
import {switchNavToSignedIn, switchNavToUnsigned}from "../common/nav_member_state.js"
import {getUserDataFromAuthAPI} from "../common/fetch_get_member_auth.js"
import {sentFetchWithBody} from "../common/sent_fetch_get_response.js"

const slideshowSliceContainer = document.querySelector(".slideshow-slice-container");
const profileTimeContainer = document.querySelector(".profile-time-container");
const profilePrice = document.querySelector(".profile-price");
const imgCountContainer = document.querySelector(".img-count-container");
const arrowLeft = document.querySelector(".arrow-left");
const arrowRight  = document.querySelector(".arrow-right");
const bookingBtn = document.querySelector(".booking-btn")
let pageId = null
let imageNumber = null

async function initialPage(){
  const url = `/api${window.location.pathname}`
  const attractionData = await fetchAttractionAPI(url)
  insertInfoData(attractionData)
  imageNumber = insertSliceImage(attractionData)
  profile.insertProfile(attractionData)
  let state = await getUserDataFromAuthAPI()
   if(state){
      switchNavToSignedIn()
    }else{
      switchNavToUnsigned() 
    }
}

window.addEventListener("load", ()=>{ 
    initialPage();
    addMemberInPageListener();
    addListenerOnBooking();
});

profileTimeContainer.addEventListener("click", (e)=>{
  let targetName = e.target.className;
  if(targetName === "option-btn"){
    let optionBtnSelected= document.querySelector(".option-btn-selected");
    optionBtnSelected.className = "option-btn";
    e.target.className = "option-btn-selected";
    let parentClassName = e.target.parentNode.className;
    if(parentClassName.includes("first")){
        profilePrice.innerText = "新台幣 2000 元";
    }else{
        profilePrice.innerText = "新台幣 2500 元";
    };
  };
});

arrowRight.addEventListener("click", (e)=>{
  sliceRight()
});

arrowLeft.addEventListener("click", (e)=>{
  sliceLeft()
});

imgCountContainer.addEventListener("click", (e)=>{
  let selectedCount = e.target
  selectCount(selectedCount)
});

bookingBtn.addEventListener("click",()=>{
  if (localStorage["userState"]){
    const today = new Date()
    const id = window.location.pathname.split("/")[2]
    const date = document.querySelector("#date-input").value
    const time = document.querySelector(".option-btn-selected").nextElementSibling.innerText === "上半天" ? "morning" : "afternoon"
    const price= parseInt(document.querySelector(".profile-price").innerText.split(" ")[1])
    if(date === ""){
      alert("請選擇日期")
    }else if(Date.parse(date) < Date.parse(today)){
      alert("請選擇今日以後的日期")  
    }else{
      sentBookingFetch(id, date, time, price)
    }
  }else{
      appendMask();
      appendMemberPage();
      insertSignInPage();
      BtnEvent();
      submitEvent();
  }

}) 

async function sentBookingFetch (id , date, time, price){
  let body ={
        "attractionId": `${id}`,
        "date": `${date}`,
        "time": `${time}`,
        "price": `${price}`
      }
  const response = await (await sentFetchWithBody("post", body, "/api/booking"))
  if(response["ok"]){
    location.assign("/booking")
  }
}



