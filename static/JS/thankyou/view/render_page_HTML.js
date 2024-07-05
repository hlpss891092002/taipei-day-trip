import {appendMask, appendMemberPage, insertSignInPage, insertSignUpPage, BtnEvent, submitEvent, addMemberInPageListener,addListenerOnBooking} from "../../common/member_sign_page.js"
import {checkSigned} from "../model/check_signed.js"
import {switchNavToSignedIn} from "../../common/nav_member_state.js"
import {sentFetchWithoutBody} from "../../common/sent_fetch_get_response.js" 

function renderOrderDetail(username, orderData){
  const {data} = orderData
  const {number, price, trip, status} = data
  const { date, time, attraction} = trip
  const {name, image, address} = attraction
  console.log(status)
  const welcome = document.querySelector(".welcome")
  const orderContent =document.querySelector(".order-content")
  const orderNumber =document.querySelector(".number")
  const notice =document.querySelector(".notice")
  const orderDetailContainer =document.querySelector(".order-detail-container")
  welcome.innerText = `親愛的${username}感謝您的預定行程，您的訂單如下`
  orderNumber.innerText  = `訂單編號 : ${number}`
  let attractionInfo = document.createElement("div")
  attractionInfo.className = "attraction-info detail-column"
  let attractionTitle = document.createElement("div")
  attractionTitle.className = "title"
  attractionTitle.innerText = "行程資訊"
  let attractionContent = document.createElement("div")
  attractionContent.className = "content"
  let attractionAddress = document.createElement("address")
  attractionAddress.className = "attraction-address"
  attractionAddress.innerText = address
  let attractionName = document.createElement("div")
  attractionName.className = "attraction-name"
  attractionName.innerText = name
  attractionContent.appendChild(attractionName)
  attractionContent.appendChild(attractionAddress)
  attractionInfo.appendChild(attractionTitle)
  attractionInfo.appendChild(attractionContent)

  let timeInfo = document.createElement("div")
  timeInfo.className = "time-info detail-column"
  let timeTitle = document.createElement("div")
  timeTitle.innerText = "行程時間資訊"
  timeTitle.className = "title";
  let timeWord = time === "afternoon" ? "下半天" : "上半天"
  let timeContent = document.createElement("div")
  timeContent.className = "content"
  timeContent.innerText = `${date}${timeWord}`
  timeInfo.appendChild(timeTitle)
  timeInfo.appendChild(timeContent)

  let priceInfo = document.createElement("div")
  priceInfo.className = "price-info detail-column"
  let priceTitle = document.createElement("div")
  priceTitle.innerText = "行程價格"
  priceTitle.className = "title";
  let priceContent = document.createElement("div")
  priceContent.className = "content"
  priceContent.innerText = `新台幣${price}`
  priceInfo.appendChild(priceTitle)
  priceInfo.appendChild(priceContent)

  let payInfo = document.createElement("div")
  payInfo.className = "pay-info detail-column"
  let payTitle = document.createElement("div")
  payTitle.innerText = "付款狀態"
  payTitle.className = "title";
  let state = status === 1 ? "已付款" : "未付款"
  let payContent = document.createElement("div")
  payContent.className = "content"
  payContent.innerText = `${state}`
  payInfo.appendChild(payTitle)
  payInfo.appendChild(payContent)

  orderDetailContainer.appendChild(attractionInfo)
  orderDetailContainer.appendChild(timeInfo)
  orderDetailContainer.appendChild(priceInfo)
  orderDetailContainer.appendChild(payInfo)
  orderContent.appendChild(orderDetailContainer)
}

export async function renderOrderPage(){
  let userData = await checkSigned()
  const{username, orderId} = await userData
  const orderData = await sentFetchWithoutBody("GET", `/api/orders/${orderId}`)
  switchNavToSignedIn()
  addMemberInPageListener()
  addListenerOnBooking()
  renderOrderDetail(username, orderData)
}

