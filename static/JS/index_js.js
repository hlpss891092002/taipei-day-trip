const leftContainer = document.querySelector(".left-container")
const rightContainer = document.querySelector(".right-container")
const listContainer = document.querySelector(".list-container")
const attractionsDisplay = document.getElementById("attractions-display")
const searchBarInput = document.querySelector(".search-bar-input")
const searchBarBTN =document.querySelector(".search-bar-btn")
const ATTRACTIONSAPI = "/api/attractions";
const  MRTSAPI = "/api/mrts"
let attractions = null;
let MRTData = null;
let nextPage = null;
let keyword = null;

async function fetchAttraction(url, page = 0, keyword = null){
  try{
    if(keyword !== null && page !== null){ 
      const response = await fetch(`${url}?keyword=${keyword}&page=${page}`);
      rawData = await response.json();
      attractions = await rawData["data"];
      nextPage = await rawData["nextPage"];
      renderSection(attractions)
    }else if (keyword !== null){
      const response = await fetch(`${url}?keyword=${keyword}`);
      rawData = await response.json();
      attractions = await rawData["data"];
      nextPage = await rawData["nextPage"];
      renderSection(attractions)
    }else if (page !== null){
      const response = await fetch(`${url}?page=${page}`);
      rawData = await response.json();
      attractions = await rawData["data"];
      nextPage = await rawData["nextPage"];
      renderSection(attractions)
    }else{
      const response = await fetch(`${url}`);
      rawData = await response.json();
      attractions = await rawData["data"];
      nextPage = await rawData["nextPage"];
      renderSection(attractions)
    }
  }catch{
    console.log("error in fetchAttraction")
  }finally{
    console.log(console.log(attractions))
  }
}

async function fetchMRTs(url){
  try{
    const response = await fetch(`${url}`);
    rawData = await response.json()
    MRTData = await rawData["data"]
    renderMrtListBar(MRTData)
  }catch{
    console.log(console.log("error in fetchMRTS"))
  }
  
}

function createAttractionSection(attraction){
  let attractionSection  = document.createElement("div");
  attractionSection.className = "attraction-section";
  let imageSection = document.createElement("div");
  imageSection.className = "img-section";
  imageSection.style.backgroundImage = `url(${attraction["images"][0]})`;
  let attractionName = document.createElement("div");
  attractionName.innerText = attraction["name"];
  let detail = document.createElement("div");
  detail.className =  "details";
  let MRT = document.createElement("span");
  MRT.className = "MRT";
  MRT.innerText = attraction["mrt"];
  let attractionCategory = document.createElement("span");
  attractionCategory.className = "attraction-category";
  attractionCategory.innerText = attraction["category"];
  attractionSection.appendChild(imageSection);
  imageSection.appendChild(attractionName);
  attractionSection.appendChild(detail);
  detail.appendChild(MRT);
  detail.appendChild(attractionCategory);
  attractionsDisplay.appendChild(attractionSection);
}
function createListBarItem(MRT){
  
}

async function renderSection(attractions){
  let attractionList = await attractions
  for (attraction of attractionList){
    createAttractionSection(attraction)
  }
}

async function renderMrtListBar(MRTData){
  let MRTList = await MRTData
  for (MRT of MRTList){
    if (MRT !== null){
      let listBarItem = document.createElement("div")
      listBarItem.className = "list-bar-item"
      listBarItem.innerText = MRT
      listContainer.appendChild(listBarItem)
    }

  }
  
  }

fetchAttraction(ATTRACTIONSAPI)
fetchMRTs(MRTSAPI)

// MRT bar
leftContainer.addEventListener("click", (e)=>{
  let clientWidth = listContainer.clientWidth*0.9
  let local = listContainer.scrollLeft
  listContainer.scroll({
    left: local -= clientWidth,
    behavior: "smooth"
  })
})

rightContainer.addEventListener("click", (e)=>{
  let clientWidth = listContainer.clientWidth*0.9
  let local = listContainer.scrollLeft
  listContainer.scroll({
    left: local += clientWidth,
    behavior: "smooth"
  })
})

//search bar
searchBarInput.addEventListener("input", (e)=>{
  console.log(1)
  searchBarInput.style.color = "#000000"
})

searchBarBTN.addEventListener("click", (e)=>{
  // e.preventDefault()
  let inputValue = searchBarInput.value
  keyword = inputValue
  nextPage = 0
  console.log(keyword)
  attractionsDisplay.replaceChildren()
  fetchAttraction(ATTRACTIONSAPI, nextPage, keyword)
})

//MRT list bar search 
listContainer.addEventListener("click", (e)=>{
  console.log(e.target.className)
  if(e.target.className === "list-bar-item"){
    let inputValue = searchBarInput.value
    let KeywordMRT = e.target.innerText
    if (inputValue != KeywordMRT){
      console.log(typeof(KeywordMRT))
      searchBarInput.value = KeywordMRT
      nextPage = 0
      keyword = KeywordMRT
      attractionsDisplay.replaceChildren()
      fetchAttraction(ATTRACTIONSAPI, nextPage, keyword)
    }
    
    
  }
})

//scroll to bottom load more data
window.addEventListener("scroll",(e)=>{
  // console.log(document.body.offsetHeight)
  // console.log(window.scrollY)
  if (window.innerHeight + Math.ceil(window.scrollY+1) >= document.body.offsetHeight){
    if (keyword && nextPage !== null){
      fetchAttraction(ATTRACTIONSAPI, nextPage, keyword)
    }else if(nextPage !== null){
      fetchAttraction(ATTRACTIONSAPI, nextPage)
    }else{
      console.log("end of data")
    }
    
  }
})

