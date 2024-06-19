export async function insertInfoData (attractionData){
  const infoDescription = document.querySelector(".info-description");
  const infoAddressContent = document.querySelector(".info-address-content");
  const infoTransportContent = document.querySelector(".info-transport-content");
  const{description, address, transport} = attractionData
  infoDescription.innerText = description;
  infoAddressContent.innerText =address;
  infoTransportContent.innerText = transport;
}

