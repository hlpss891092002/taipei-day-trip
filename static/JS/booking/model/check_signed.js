import {getUserDataFromAuthAPI} from "../../common/fetch_get_member_auth.js"
import {sentFetchWithoutBody} from "../../common/sent_fetch_get_response.js"

export async function checkSigned(){
  let state = await getUserDataFromAuthAPI()
   if(state){
    let bookingData = {};
    const username = state["name"];
    const id = state["id"];
    bookingData["username"] = username;
    bookingData["id"] = id;
    const data = await sentFetchWithoutBody("GET","/api/booking");
    bookingData["data"] = data["data"];
    return bookingData;
    }else{
      localStorage.clear()
      window.location.replace("/") 
    }
}