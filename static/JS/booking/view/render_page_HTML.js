import {appendMask, appendMemberPage, insertSignInPage, insertSignUpPage, BtnEvent, submitEvent, addMemberInPageListener,addListenerOnBooking} from "../../common/member_sign_page.js"
import {checkSigned} from "../model/check_signed.js"
import {switchNavToSignedIn}from "../../common/nav_member_state.js"
import {deleteBooking, setListenerDelete} from "../model/cancel_booking.js"
import { TPDsetup,} from "../model/tappay_setup.js"
import {listenContact} from "../model/RegEX.js"
import {getMemberOrder} from "./render_order_table.js"

export function renderPageSignedHTML(){
  const bookingContainer = document.querySelector(".booking-container")
  bookingContainer.innerHTML = '<section class="booking-order">        <div class="booking-head-line">您好</div>        <div class="booking-content-container">      <img class="booking-content-image" src="/static/img/welcome_image.png" alt="">          <div class="booking-content-details">           <div  id="booking-header">台北一日遊：平安鐘</div>            <div class="booking-detail" >日期：<span class="booking-detail-content" id="booking-date"></span></div>            <div class="booking-detail" >時間：<span class="booking-detail-content"  id="booking-time"></span></div>            <div class="booking-detail" >費用：<span class="booking-detail-content" id="booking-cost"></span></div>            <div class="booking-detail" >地點：<span class="booking-detail-content" id="booking-address"></span></div>            <img id="cancel-booking-icon" src="/static/img/icon_delete.png" alt="trash-hban">          </div>        </div>      </section>      <div class="separator-container">        <hr class="separator" />      </div>      <section class="contact-information">  <div class="contact-container">      <div class="contact-header">您的聯絡資訊</div>        <div class="contact-input">          <label for="name">聯絡姓名：</label>          <input type="text" name="name" class="contact-name">        </div>        <div class="contact-input">          <label for="email">聯絡信箱：</label>          <input type="text" name="email" class="contact-email">        </div>        <div class="contact-input">          <label for="telephone">手機號碼：</label>          <input type="text" name="telephone" class="contact-telephone">        </div>        <div class="notice-line">請保持手機暢通，準時到達，導覽人員將用手機與您聯繫，務必留下正確的聯絡方式。</div>  <div>    </section>      <div class="separator-container">        <hr class="separator" />      </div>       <section class="pay-information"> <div class="pay-container">       <div class="pay-header">信用卡付款資訊</div>         <form> <div class="card-input">          <div for="card-number">卡片號碼：</div>         <div class="tpfield" id="card-number"></div>       </div>        <div class="card-input">          <div for="Expiration">過期時間：</div>          <div class="tpfield" id="card-expiration-date"></div>       </div>        <div class="card-input">          <div for="authorization-password">驗證密碼：</div>          <div class="tpfield" id="card-ccv"></div>        </div>  </form> </section> <div class="separator-container">        <hr class="separator" />      </div>   <section class="confirm-total"> <div class="confirm-container">   <div class="total-price">total price</div>    <button type="button" class="confirm-btn" id="submit-button">確認訂購並付款</button> </div>  </section>   '
}

export async function renderBookingData(bookingData){
  const {date, price, time, attraction} = bookingData
  const {address, image, name} = attraction
  const bookingContentImage = document.querySelector(".booking-content-image")
  const bookingHeader = document.querySelector("#booking-header")
  const bookingDate = document.querySelector("#booking-date")
  const bookingTime = document.querySelector("#booking-time")
  const bookingCost = document.querySelector("#booking-cost")
  const bookingAddress = document.querySelector("#booking-address")
  const totalPrice = document.querySelector(".total-price")
  bookingContentImage.src = image
  bookingHeader.innerText = `台北一日遊：${name}`
  bookingDate.innerText = date
  bookingTime.innerText = time
  bookingCost.innerText = price
  bookingAddress.innerText =address
  totalPrice.innerText = `總價：新台幣${price}`
}
export async function renderBookingWelcome(username){
  const bookingHeadLine = document.querySelector(".booking-head-line")
  bookingHeadLine.innerText = `您好，${username}，待預訂的行程如下：`
}

export function renderBookingMessage(){
  const bookingMessage = document.querySelector(".booking-message")
  bookingMessage.innerText = "目前沒有任何待預訂的行程"
}

export async function renderBookingPage(){
  let bookingData = await checkSigned()
  const{username, data, id} = bookingData
  if (data === null){
    renderBookingWelcome(username)
    renderBookingMessage()
    switchNavToSignedIn()
    addMemberInPageListener()
    addListenerOnBooking()
    getMemberOrder(username, id)
  }else{
    renderPageSignedHTML()
    renderBookingWelcome(username)
    renderBookingData(data)
    switchNavToSignedIn()
    addMemberInPageListener()
    addListenerOnBooking()
    setListenerDelete()
    listenContact()
    TPDsetup(data)
    getMemberOrder(username, id)
  }
}

