
import {sentFetchWithBody} from "../../common/sent_fetch_get_response.js" 

export async function TPDsetup(data){
  TPDirect.setupSDK(151756, 'app_HsPP4zNAlS9HxOTrPux9PxespixJWvDUcVhsM0R5BzyASQWpxrjN9Rt83Xox', 'sandbox')
  let fields = {
      number: {
          // css selector
          element: '#card-number',
          placeholder: '**** **** **** ****'
      },
      expirationDate: {
          // DOM object
          element: document.getElementById('card-expiration-date'),
          placeholder: 'MM / YY'
      },
      ccv: {
          element: '#card-ccv',
          placeholder: 'ccv'
      }
  }

  TPDirect.card.setup({
      fields: fields,
      styles: {
          // Style all elements
          'input': {
              'color': 'gray'
          },
          // Styling ccv field
          'input.ccv': {
              // 'font-size': '16px'
          },
          // Styling expiration-date field
          'input.expiration-date': {
              // 'font-size': '16px'
          },
          // Styling card-number field
          'input.card-number': {
              // 'font-size': '16px'
          },
          // style focus state
          ':focus': {
              // 'color': 'black'
          },
          // style valid state
          '.valid': {
              'color': 'green'
          },
          // style invalid state
          '.invalid': {
              'color': 'red'
          },
          // Media queries
          // Note that these apply to the iframe, not the root window.
          '@media screen and (max-width: 400px)': {
              'input': {
                  'color': 'orange'
              }
          }
      },
      // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
      isMaskCreditCardNumber: true,
      maskCreditCardNumberRange: {
          beginIndex: 6,
          endIndex: 11
      }
  })
  const submitButton = document.getElementById("submit-button");

  async function payment(prime){
    const name = document.querySelector(".contact-name").value
    const email = document.querySelector(".contact-email").value
    const phone = document.querySelector(".contact-telephone").value
    const body ={}
    const {price, attraction, date, time} = data

    body["prime"] = prime
    body["order"] = {
        "price" : price,
        "trip" : {
            "attraction": attraction
        },
        "date" : date,
        "time" : time
    }
    body["contact"] = {
        "name" : name,
        "email": email,
        "phone": phone      
    }
    const orderData =  await sentFetchWithBody("post", body, "/api/orders");
    const order_id = orderData["data"]["number"];
    location.replace(`/thankyou?number=${order_id}`)
  }

  submitButton.addEventListener("click",(e)=>{
    e.preventDefault()
    // 取得 TapPay Fields 的 status
      const tappayStatus = TPDirect.card.getTappayFieldsStatus()
      // 確認是否可以 getPrime
      if (tappayStatus.canGetPrime === false) {
          alert('請輸入信用卡資訊')
          return
      }
      // Get prime
      
      TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }
        payment(result.card.prime)
      })
  })
      
  
  TPDirect.card.onUpdate(function (update) {
    update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        submitButton.removeAttribute('disabled')
    } else {
        // Disable submit Button to get prime.
        submitButton.setAttribute('disabled', true)
    }

    // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay','unknown']
    // if (update.cardType === 'visa') {
    //     // Handle card type visa.
    // }

    // number 欄位是錯誤的
    // if (update.status.number === 2) {
    //     setNumberFormGroupToError()
    // } else if (update.status.number === 0) {
    //     setNumberFormGroupToSuccess()
    // } else {
    //     setNumberFormGroupToNormal()
    // }

    // if (update.status.expiry === 2) {
    //     setNumberFormGroupToError()
    // } else if (update.status.expiry === 0) {
    //     setNumberFormGroupToSuccess()
    // } else {
    //     setNumberFormGroupToNormal()
    // }

    // if (update.status.ccv === 2) {
    //     setNumberFormGroupToError()
    // } else if (update.status.ccv === 0) {
    //     setNumberFormGroupToSuccess()
    // } else {
    //     setNumberFormGroupToNormal()
    // }
  })
  TPDirect.card.getTappayFieldsStatus()

  

}

