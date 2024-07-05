import {getUserDataFromAuthAPI} from "../../common/fetch_get_member_auth.js"
import {sentFetchWithoutBody} from "../../common/sent_fetch_get_response.js"

export async function checkSigned(){
  let state = await getUserDataFromAuthAPI()
   if(state){
    let userData = {};
    const username = state["name"];
    userData["username"] = username;
    const orderId = location.search.split("=")[1];
    console.log(orderId)
    userData["orderId"] = orderId;
    return userData;
    }else{
      window.location.replace("/") 
    }
}