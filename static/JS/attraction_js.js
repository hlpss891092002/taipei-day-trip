const attractionArray = location.href.split("/");
const attractionID = location.href.split("/")[attractionArray.length-1];
const ImgSlideContainer = document.querySelector(".img-slideshow-container");
const slideshowSliceContainer = document.querySelector(".slideshow-slice-container");
const imgCountContainer = document.querySelector(".img-count-container");
const arrowLeft = document.querySelector(".arrow-left");
const arrowRight  = document.querySelector(".arrow-right");
const profileName = document.querySelector(".profile-name");
const profileCategoryMRT = document.querySelector(".profile-Category-MRT");
const infoDescription = document.querySelector(".info-description");
const infoAddressContent = document.querySelector(".info-address-content");
const infoTransportContent = document.querySelector(".info-transport-content");
const profileTimeContainer = document.querySelector(".profile-time-container");
const profilePrice = document.querySelector(".profile-price");
const imgCounts = imgCountContainer.childNodes;
const slices = slideshowSliceContainer.childNodes;
let imageNumber = null;
let sliceIndex = 0;
let preloadImgArray = []

console.log(attractionID);
fetchAttractionID(attractionID);

 //get page data
async function fetchAttractionID(id){
  try{
    url = `/api/attraction/${id}`;
    let response = await fetch(url);
    let data = await response.json();
    let attractionData = data["data"];
    console.log(attractionData);
    profileName.innerText = attractionData["name"];
    profileCategoryMRT.innerText = `${attractionData["category"]} at ${attractionData["mrt"]}`;
    infoDescription.innerText = attractionData["description"];
    infoAddressContent.innerText = attractionData["address"];
    infoTransportContent.innerText = attractionData["transport"];
    let imagesArray = attractionData["images"];
    imageNumber = imagesArray.length;
    for (url of imagesArray){
      let preloadImg = new Image()
      preloadImg.src = url
      preloadImgList.push(preloadImg)  
      number = imagesArray.indexOf(url);
      createImgCount(url, number);
    };
    imgCounts[sliceIndex].classList.add("selected");
    slices[sliceIndex].classList.add("active");
  }catch{
    console.log("fetch fail");
  }finally{
  };

};

//insert img count
function createImgCount (url, number){
  let imgSection = document.createElement("div");
  imgSection.className = "slideshow-slice";
  imgSection.classList.add("fade");
  imgSection.style.backgroundImage = `url(${url})`;
  slideshowSliceContainer.appendChild(imgSection);
  let imgCount = document.createElement("button");
  imgCount.className = `img-count`;
  imgCount.classList.add(number);
  imgCount.type = "button";
  imgCountContainer.append(imgCount);
};

profileTimeContainer.addEventListener("click",(e)=>{
  targetName = e.target.className;
  if(targetName === "option-btn"){
    optionBtnSelected= document.querySelector(".option-btn-selected");
    optionBtnSelected.className = "option-btn";
    e.target.className = "option-btn-selected";
    parentClassName = e.target.parentNode.className;
    if(parentClassName.includes("first")){
        profilePrice.innerText = "新台幣 2000元";
        console.log("switch to First");
    }else{
        profilePrice.innerText = "新台幣 2500元";
        console.log("switch to second");
    };
  };
});
arrowRight.addEventListener("click", (e)=>{
  try{
  if(sliceIndex === imageNumber - 1 ){
    imgCounts[sliceIndex].classList.remove("selected");
    slices[sliceIndex].classList.remove("active")
    sliceIndex = 0
    imgCounts[sliceIndex].classList.add("selected");
    slices[sliceIndex].classList.add("active")
  }else{
    console.log(sliceIndex)
    imgCounts[sliceIndex].classList.remove("selected");
    slices[sliceIndex].classList.remove("active")
    sliceIndex += 1
    imgCounts[sliceIndex].classList.add("selected");
    slices[sliceIndex].classList.add("active")   
  }
  }catch{
    console.log("arrowRight listener error ")
  }

  
})
arrowLeft.addEventListener("click", (e)=>{
  try{
    if(sliceIndex === 0 ){
    imgCounts[sliceIndex].classList.remove("selected");
    slices[sliceIndex].classList.remove("active")
    sliceIndex = imageNumber - 1
    imgCounts[sliceIndex].classList.add("selected");
    slices[sliceIndex].classList.add("active")
  }else{
    imgCounts[sliceIndex].classList.remove("selected");
    slices[sliceIndex].classList.remove("active")
    sliceIndex -= 1
    imgCounts[sliceIndex].classList.add("selected");
    slices[sliceIndex].classList.add("active")  
  }
  }catch{
    console.log("arrowLeft listener error")
  }
  
  
})
imgCountContainer.addEventListener("click", (e)=>{
  selectedCount = e.target
  targetClassName = selectedCount.classList[0]
  if(targetClassName === "img-count"){
    imgCounts[sliceIndex].classList.remove("selected")
    slices[sliceIndex].classList.remove("active")
    selectedCount.classList.add("selected")
    selectedNumber = parseInt(selectedCount.classList[1])
    sliceIndex = selectedNumber
    console.log(sliceIndex )
    slices[sliceIndex].classList.add("active")  
  }
  
})

