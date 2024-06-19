import {fetchAttractionAPI} from "../common/fetch_api_location_path.js"



const  insertProfile = async function (attractionData) {
  const profileName = document.querySelector(".profile-name");
  const profileCategoryMRT = document.querySelector(".profile-Category-MRT");
  const{name, category, mrt} =  attractionData;
  profileName.innerText = name;
  profileCategoryMRT.innerText = `${category} at ${mrt}`;
}

const  switchDaytime = function (){
  const profileTimeContainer = document.querySelector(".profile-time-container");
  const profilePrice = document.querySelector(".profile-price");
};

export const profile = {
  "insertProfile" :insertProfile
};
