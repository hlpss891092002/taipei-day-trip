import {fetchAttractionAPI} from "../common/fetch_api_location_path.js"

const ImgSlideContainer = document.querySelector(".img-slideshow-container");
const slideshowSliceContainer = document.querySelector(".slideshow-slice-container");
const imgCountContainer = document.querySelector(".img-count-container");
const imgCounts = imgCountContainer.childNodes;
const slices = slideshowSliceContainer.childNodes;
let imageNumber = null
let sliceIndex = 0;
let preloadImgArray = []

 export async function insertSliceImage(attractionData){
  const {images} = attractionData;
  let imagesArray = images;
  imageNumber = imagesArray.length;
  for (let imageUrl of imagesArray) {
      let preloadImg = new Image();
      preloadImg.src = imageUrl;
      preloadImgArray.push(preloadImg);
      let number = imagesArray.indexOf(imageUrl);
      createImgCount(imageUrl, number);
    };
  imgCounts[sliceIndex].classList.add("selected");
  slices[sliceIndex].classList.add("active");
  return imageNumber
}
function createImgCount(url, number){
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

export function sliceLeft(){
  imgCounts[sliceIndex].classList.remove("selected")
  slices[sliceIndex].classList.remove("active")
  sliceIndex = (imageNumber + sliceIndex - 1) % imageNumber
  imgCounts[sliceIndex].classList.add("selected")
  slices[sliceIndex].classList.add("active")
}

export function sliceRight(){
  imgCounts[sliceIndex].classList.remove("selected")
  slices[sliceIndex].classList.remove("active")
  sliceIndex = (imageNumber + sliceIndex + 1) % imageNumber
  imgCounts[sliceIndex].classList.add("selected")
  slices[sliceIndex].classList.add("active")
}

export function selectCount(count){
  if(count.classList[0] === "img-count"){
    if(!count.classList[2]){
      let countOrder = count.classList[1]
      imgCounts[sliceIndex].classList.remove("selected")
      slices[sliceIndex].classList.remove("active")
      sliceIndex = countOrder
      count.classList.add("selected")
      slices[countOrder].classList.add("active")
    }  
  }
}
