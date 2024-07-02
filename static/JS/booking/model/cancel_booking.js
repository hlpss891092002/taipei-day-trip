import {sentFetchWithoutBody} from "../../common/sent_fetch_get_response.js"

export async function deleteBooking(){
    const result = await sentFetchWithoutBody("delete", "/api/booking")
    return result["ok"]
} 

export async function setListenerDelete(){
  const cancelBooking = document.querySelector("#cancel-booking-icon")
  cancelBooking.addEventListener("click",(e)=>{
    if (deleteBooking()){
      location.reload()
    }

  })
}