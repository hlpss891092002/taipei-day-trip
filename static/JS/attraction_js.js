const attractionArray = location.href.split("/")
const attractionID = location.href.split("/")[attractionArray.length-1]
const ImgSlideContainer = document.querySelector(".img-slideshow-container")
const profileName = document.querySelector(".profile-name")
const profileCategoryMRT = document.querySelector(".profile-Category-MRT")
const infoDescription = document.querySelector(".info-description")
const infoAddressContent = document.querySelector(".info-address-content")
const infoTransportContent = document.querySelector(".info-transport-content")
const profileTimeContainer = document.querySelector(".profile-time-container")
const profilePrice = document.querySelector(".profile-price")


console.log(attractionID)
fetchAttractionID(attractionID)

 //get page data
async function fetchAttractionID(id){
  try{
    url = `/api/attraction/${id}`
    let response = await fetch(url)
    let data = await response.json()
    let attractionData = data["data"]
    console.log(attractionData)
    profileName.innerText = attractionData["name"]
    profileCategoryMRT.innerText = `${attractionData["category"]} at ${attractionData["mrt"]}`
    infoDescription.innerText = attractionData["description"]
    infoAddressContent.innerText = attractionData["address"]
    infoTransportContent.innerText = attractionData["transport"]
  }catch{
    console.log("fetch fail")
  }finally{
  }
}

//insert img count
// function createImgCount (url){
// }

profileTimeContainer.addEventListener("click",(e)=>{
  targetName = e.target.className
  if(targetName === "option-btn"){
    optionBtnSelected= document.querySelector(".option-btn-selected")
    optionBtnSelected.className = "option-btn"
    e.target.className = "option-btn-selected"
    parentClassName = e.target.parentNode.className
    console.log(parentClassName)
    if(parentClassName.includes("first")){
        profilePrice.innerText = "新台幣 2000元"
        console.log("switch to First")
    }else{
        profilePrice.innerText = "新台幣 2500元"
        console.log("switch to second")
    }
    

  }
})