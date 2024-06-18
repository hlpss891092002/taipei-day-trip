import {appendMask, appendMemberPage, insertSignInPage, insertSignUpPage, BtnEvent, submitEvent, addMemberInPageListener} from "../common/member_login_signin.js"
import {switchNavToSignedIn, switchNavToUnsigned}from "../common/nav_member_state.js"
import {getUserDataFromAuthAPI} from "../common/fetch_get_member_auth.js"

const leftContainer = document.querySelector(".left-container");
const rightContainer = document.querySelector(".right-container");
const listContainer = document.querySelector(".list-container");
const attractionsDisplay = document.getElementById("attractions-display");
const searchBarInput = document.querySelector(".search-bar-input");
const searchBarBTN = document.querySelector(".search-bar-btn");


const ATTRACTIONSAPI = "/api/attractions";
const  MRTSAPI = "/api/mrts";
let attractions = null;
let MRTData = null;
let nextPage = null;
let keyword = null;
let loading = false;

async function fetchAttraction(url, page = 0, keyword = ""){
  try{
      loading =true
      const response = await fetch(`${url}?keyword=${keyword}&page=${page}`);
      let rawData = await response.json();
      attractions = await rawData["data"];
      nextPage = await rawData["nextPage"];
      renderSection(attractions);

  }catch{
    console.log("error in fetchAttraction");
  }finally{
    loading = false;
  };
};

async function fetchMRTs(url){
  try{
    const response = await fetch(`${url}`);
    let rawData = await response.json();
    let MRTData = await rawData["data"];
    renderMrtListBar(MRTData);
  }catch{
    console.log(console.log("error in fetchMRTS"));
  };
};

function createAttractionSection(attraction){
  let attractionSection  = document.createElement("div");
  attractionSection.className = `attraction-section`;
  let attractionPageUrl = document.createElement("a");
  let id = attraction["id"];
  attractionPageUrl.className = "l";
  attractionPageUrl.href = `/attraction/${attraction["id"]}`;
  let imageSection = document.createElement("div");
  imageSection.className = "img-section";
  imageSection.style.backgroundImage = `url(${attraction["images"][0]})`;
  let attractionName = document.createElement("div");
  attractionName.innerText = attraction["name"];
  let detail = document.createElement("div");
  detail.className =  "details";
  let MRT = document.createElement("span");
  MRT.className = "MRT";
  if(attraction["mrt"] !== "None"){
    MRT.innerText = attraction["mrt"];
  }else{
    MRT.innerText = "";
  };
  let attractionCategory = document.createElement("span");
  attractionCategory.className = "attraction-category";
  attractionCategory.innerText = attraction["category"];
  attractionSection.appendChild(attractionPageUrl)
  attractionPageUrl.appendChild(imageSection);
  imageSection.appendChild(attractionName);
  attractionSection.appendChild(detail);
  detail.appendChild(MRT);
  detail.appendChild(attractionCategory);
  attractionsDisplay.appendChild(attractionSection);
};

function renderSection(attractions){
  let attractionList = attractions;
  for (let attraction of attractionList){
    createAttractionSection(attraction);
  };
};

function renderMrtListBar(MRTData){
  let MRTList = MRTData;
  for (let MRT of MRTList){
    if (MRT !== null){
      let listBarItem = document.createElement("div");
      listBarItem.className = "list-bar-item";
      listBarItem.innerText = MRT;
      listContainer.appendChild(listBarItem);
      };
    };
  };
//load page identified token
async function initialPage(){
  fetchAttraction(ATTRACTIONSAPI);
  fetchMRTs(MRTSAPI);
  let state = await getUserDataFromAuthAPI()
   if(state){
      switchNavToSignedIn()
    }else{
      switchNavToUnsigned() 
    }

}

window.addEventListener("load", (e)=>{
    initialPage()
    addMemberInPageListener()
});

// MRT bar
leftContainer.addEventListener("click", (e)=>{
  let clientWidth = listContainer.clientWidth*0.9;
  let local = listContainer.scrollLeft;
  listContainer.scroll({
    left: local -= clientWidth,
    behavior: "smooth"
  });
});

rightContainer.addEventListener("click", (e)=>{
  let clientWidth = listContainer.clientWidth*0.9;
  let local = listContainer.scrollLeft;
  listContainer.scroll({
    left: local += clientWidth,
    behavior: "smooth"
  });
})

//search bar
searchBarInput.addEventListener("input", (e)=>{
  searchBarInput.style.color = "#000000";
})

searchBarBTN.addEventListener("click", (e)=>{
  let inputValue = searchBarInput.value;
  console.log(searchBarInput.value)
  if(inputValue === ""){
      e.preventDefault()
  }else{
    keyword = inputValue;
    nextPage = 0;
    console.log(keyword);
    attractionsDisplay.replaceChildren();
    fetchAttraction(ATTRACTIONSAPI, nextPage, keyword);
  };
});

//MRT list bar search 
listContainer.addEventListener("click", (e)=>{
  console.log(e.target.className);
  if(e.target.className === "list-bar-item"){
    let inputValue = searchBarInput.value;
    let KeywordMRT = e.target.innerText;
    if (inputValue != KeywordMRT){
      console.log(typeof(KeywordMRT));
      searchBarInput.value = KeywordMRT;
      nextPage = 0;
      keyword = KeywordMRT;
      attractionsDisplay.replaceChildren();
      fetchAttraction(ATTRACTIONSAPI, nextPage, keyword)
    };
  };
});

//scroll to bottom load more data
window.addEventListener("scroll",(e)=>{
  if(! loading){
    if (window.innerHeight + Math.ceil(window.scrollY) >= document.body.offsetHeight -300 ){
          if (keyword && nextPage !== null){
          fetchAttraction(ATTRACTIONSAPI, nextPage, keyword);
          }else if(nextPage !== null){
            fetchAttraction(ATTRACTIONSAPI, nextPage);
          }else{
            console.log("end of data");
          };
        }else{
          return
      }
  };
});









