export let  fetchAttractionAPI = async function(url) {
  const response = await fetch(url);
  const data = await response.json();
  const attractionData = data["data"];
  return attractionData;
}

