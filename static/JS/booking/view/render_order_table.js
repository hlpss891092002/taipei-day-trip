import {sentFetchWithoutBody} from "../../common/sent_fetch_get_response.js"


function renderOrderDetail(username, orderData){
  const {name, address, status, time, price, number, date} = orderData
  console.log(status)
  const welcome = document.querySelector(".welcome")
  const orderContent =document.querySelector(".order-content")
  const orderNumber =document.createElement("div")
  orderNumber.className = "number"
  const notice =document.querySelector(".notice")
  const orderDetailContainer =document.createElement("div")
  orderDetailContainer.className = "order-detail-container"
  welcome.innerText = `親愛的${username}您已預定行程，您的訂單如下`
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
  let state = status === "PAID" ? "已付款" : "未付款"
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
  console.log(orderDetailContainer)
}


export async function getMemberOrder(username, member_id){
  let rawData = await sentFetchWithoutBody("get" ,`/api/ordersList/${member_id}`)
  const data = rawData["data"]
  let today = new Date

  for (let i = 0; i < data.length; i++){
    if (Date.parse(data[i]["date"]) > Date.parse(today) ){
      renderOrderDetail(username, data[i])
      console.log(i)
    }
  }
}
  