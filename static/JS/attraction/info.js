import {fetchAttractionAPI} from "../common/fetch_api_location_path.js"

export async function insertInfoData (){
  const infoDescription = document.querySelector(".info-description");
  const infoAddressContent = document.querySelector(".info-address-content");
  const infoTransportContent = document.querySelector(".info-transport-content");
  const url = `/api${window.location.pathname}`
  const attractionData = await fetchAttractionAPI(url)
  const{description, address, transport} = attractionData
  infoDescription.innerText = description;
  infoAddressContent.innerText =address;
  infoTransportContent.innerText = transport;
}

