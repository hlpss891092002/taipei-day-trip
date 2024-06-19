import {insertInfoData} from "./info.js"
import {profile} from "./cover_section_profile.js"
import {insertSliceImage, sliceLeft, sliceRight, selectCount} from "./cover_section_slideshow.js"
import {appendMask, appendMemberPage, insertSignInPage, insertSignUpPage, BtnEvent, submitEvent, addMemberInPageListener} from "../common/member_sign_page.js"
import {fetchAttractionAPI} from "../common/fetch_api_location_path.js"
import {switchNavToSignedIn, switchNavToUnsigned}from "../common/nav_member_state.js"
import {getUserDataFromAuthAPI} from "../common/fetch_get_member_auth.js"

const slideshowSliceContainer = document.querySelector(".slideshow-slice-container");
const profileTimeContainer = document.querySelector(".profile-time-container");
const profilePrice = document.querySelector(".profile-price");
const imgCountContainer = document.querySelector(".img-count-container");
const arrowLeft = document.querySelector(".arrow-left");
const arrowRight  = document.querySelector(".arrow-right");
const imgCounts = imgCountContainer.childNodes;
let slices = slideshowSliceContainer.childNodes;
const memberInBtn = document.querySelector("#member-in-btn")
let imageNumber = null
let sliceIndex = 0;

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
    initialPage()
    addMemberInPageListener()
    
});

profileTimeContainer.addEventListener("click", (e)=>{
  let targetName = e.target.className;
  if(targetName === "option-btn"){
    let optionBtnSelected= document.querySelector(".option-btn-selected");
    optionBtnSelected.className = "option-btn";
    e.target.className = "option-btn-selected";
    let parentClassName = e.target.parentNode.className;
    if(parentClassName.includes("first")){
        profilePrice.innerText = "新台幣 2000元";
    }else{
        profilePrice.innerText = "新台幣 2500元";
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



