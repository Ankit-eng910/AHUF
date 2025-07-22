window.addEventListener('load', () => {
  const loader = document.getElementById("loader");
  const content = document.getElementById("main-content");
  const logoLoader = document.getElementById("mainLoader");

  // Show logo after scatter
  setTimeout(() => {
    logoLoader.classList.add("show");
  }, 200); // halfway through scatter

  // Hide loader, show content
  setTimeout(() => {
    loader.style.display = "none";
    content.style.display = "block";
  }, 100);
});


document.addEventListener('DOMContentLoaded', function () {
  const cards = document.querySelectorAll('.col-md-6 .adress-cards');

  cards.forEach(card => {
    card.addEventListener('click', function () {
      // Remove 'selected-address' from all cards
      cards.forEach(c => c.classList.remove('selected-address'));

      // Add it to the clicked card
      this.classList.add('selected-address');
    });
  });
});







let currentStep = 1;

function showStep(step) {
  document.querySelectorAll(".step-content").forEach(el => el.classList.remove("active"));
  document.getElementById("step" + step).classList.add("active");
  currentStep = step;

  for (let i = 1; i <= 2; i++) {
    const indicator = document.getElementById("stepIndicator" + i);
    if (i < step) {
      indicator.className = "rounded-circle bg-primary text-white mx-auto mb-2 step-indicator";
    } else if (i === step) {
      indicator.className = "rounded-circle bg-primary text-white mx-auto mb-2 step-indicator";
    } else {
      indicator.className = "rounded-circle bg-light text-dark mx-auto mb-2 step-indicator";
    }
  }

  // Reset view when coming to step 2
  if (step === 2) {
    document.getElementById("addressSelection").style.display = "block";
    document.getElementById("newAddressForm").style.display = "none";
    // document.getElementById("addressBackBtn").style.display = "block";
  }
}

function nextStep() {
  if (currentStep < 3) {
    showStep(currentStep + 1);
  }
}

function prevStep() {
  if (currentStep > 1) {
    showStep(currentStep - 1);
  }
}

function showNewAddressForm() {
  document.getElementById("addressSelection").style.display = "none";
  document.getElementById("newAddressForm").style.display = "block";
  document.getElementById("addressBackBtn").style.display = "none"; // Hide top back button
}

function backToAddressSelection() {
  document.getElementById("addressSelection").style.display = "block";
  document.getElementById("editAddressForm").style.display = "none";
  document.getElementById("newAddressForm").style.display = "none";

  document.getElementById("addressTopBackBtn").style.display = "none"; // Hide top back
  document.getElementById("addressBottomBackBtn").style.display = "block"; // Show bottom back
}

// function submitForm() {
//   alert("Proceeding to Payment Gateway...");
// }

function editSavedAddress(adId) {
  document.getElementById("addressSelection").style.display = "none";
  document.getElementById("newAddressForm").style.display = "none";
  document.getElementById("editAddressForm").style.display = "block";
  // document.getElementById("addressBackBtn").style.display = "none"; // hide top back button

  // Api fetching data

  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if (tokens) {
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }


  const requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow"
  };

  fetch(`http://127.0.0.1:8000/api/addresses/?id=${adId}`, requestOptions)
    .then((response) => response.json())
    .then((result) => {

      if (result.success) {
        document.getElementById("customer-name").value = result.data[0].full_name;
        document.getElementById("customer-contact").value = result.data[0].phone_number;
        document.getElementById("email-id").value = result.data[0].email;
        document.getElementById("customer-city").value = result.data[0].city;
        document.getElementById("customer-state").value = result.data[0].state_or_region;
        document.getElementById("full-address").value = result.data[0].street_address;
        document.getElementById("pin-code").value = result.data[0].postal_code;
        document.getElementById("apartment-address").value = result.data[0].apartment

        const upbtn = document.querySelector(".updatebtncheck")
        upbtn.setAttribute("onclick", `updateAddress(${adId})`);
      }


    })
    .catch((error) => console.error(error));

}
function showEditAddressForm() {
  document.getElementById("addressSelection").style.display = "none";
  document.getElementById("editAddressForm").style.display = "block";
  document.getElementById("newAddressForm").style.display = "none";

  document.getElementById("addressTopBackBtn").style.display = "block"; // Show top back
  document.getElementById("addressBottomBackBtn").style.display = "none"; // Hide bottom back
}


const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
const tokens = cookieMatch ? cookieMatch[2] : null;
// if (!tokens){
//     window.location.href = '/api/login-page/';
// }
document.addEventListener("DOMContentLoaded", function () {
  cardData();
  offerShow();
});

function cardData() {
  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if (tokens) {
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }
  // else {
  //     window.location.href = '/api/login-page/'
  //     return false
  // }
  // myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwMDM5MTEwLCJpYXQiOjE3NDg1MDMxMTAsImp0aSI6IjVjYmE0ZjRmYmJiZjQ3MTJhNWQ1ZmY4MDkwYjI3NTZmIiwidXNlcl9pZCI6M30.ZJ6qBEEHlTeDxliMWkmsK3MWbHs1kUb_B-oAC3U0OJk");
  myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");

  const requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow"
  };

  // fetch("https://ahufcafe.com/api/get-cart/", requestOptions)
  fetch("http://127.0.0.1:8000/api/get-cart/", requestOptions)
    .then((response) => response.json())
    .then((result) => {

      console.log(result)
      if (result.success) {
        if (result.data.length > 0) {
          const cartContainer = document.getElementById('card-data');
          result.data.forEach(item => {
            carthtml = `
                    <div class="view-cart-product-show-container mt-2">
                   
                    <div class="d-flex align-items-center">
                    <div onclick="removeItem(${item.menu_item_details.id},'${item.item_type}' , ${result.is_party_catering} , ${item.quantity} )" style="cursor:pointer;" >
                     <i  class="bi bi-trash3" style="color:var(--first-color); "></i>
                    </div>
                     <div class="ms-2"><img src="${item.menu_item_details.imageUrl}" alt="image"></div>
                      <div>
                        <h4>${item.menu_item_details.name}</h4>
                        <h5 class="price-number">&#8377;${item.menu_item_details.discounted_price} <span class="text-muted"
                            style="text-decoration: line-through;">&#8377;${item.menu_item_details.price}</span></h5>
                      </div>
                    </div>



                    <div class="quantity-container mt-3 rounded-3">
                      <button onclick="decreaseQty('${item.menu_item_details.id}','${item.menu_item_details.name.replace(/\s+/g, '')}web', true , true , ${result.is_party_catering} , '${item.item_type}' )" class="quantity-btn-show ">−</button>
                      <input type="text"  value="${item.quantity}" readonly class="quantity-input-value ${item.menu_item_details.name.replace(/\s+/g, '')}web" />
                      <button onclick="increaseQty('${item.menu_item_details.id}','${item.menu_item_details.name.replace(/\s+/g, '')}web', true , true , ${result.is_party_catering} , '${item.item_type}' )" class="quantity-btn-show">+</button>
                    </div>

                  </div>
                    `
            cartContainer.innerHTML += carthtml
          });


          const cartContainerTotal = document.getElementById('cart-total');
          if (result.is_party_catering){
            const now = new Date();
            const futureTime = new Date(now.getTime() + 5 * 60 * 60 * 1000); // +5 hours
            const todayStr = now.toISOString().slice(0, 10);
            const minTimeStr = futureTime.toTimeString().slice(0, 5); // "HH:MM"
            if (result.data[0].schedule_details !== null){

              const availableOccasions = ['Birthday', 'Small Gathering', 'Anniversary', 'Party', 'Corporate'];
              let optionsHtml = `<option value="">Occasion</option>`;
              availableOccasions.forEach(option => {
                const selected = option === result.data[0].schedule_details.occasion ? 'selected' : '';
                optionsHtml += `<option value="${option}" ${selected}>${option}</option>`;
              });
              document.getElementById('sheduled-data-form').innerHTML = `
              <h6 class="mt-3"><b>Schedule</b></h6>
              <form>
                <div  class="row">
                  <div class="col-md-12 mt-2">
                    <label class="input-label-show">Occasion</label>
                    <select v  class="input-box-view">
                       ${optionsHtml}
                    </select>
                  </div>
                    <div class="col-md-6 col-6 mt-2">
                    <label class="input-label-show">Date</label>
                    <input type="date" class="input-box-view" id="schedule-date" min="${todayStr}" value="${result.data[0].schedule_details.scheduled_date}" />
                  </div>
                    <div class="col-md-6 col-6 mt-2">
                    <label class="input-label-show">Time</label>
                    <input type="time" class="input-box-view" id="schedule-time"  min="${minTimeStr}" value="${result.data[0].schedule_details.scheduled_time}" />
                  </div>
                </div>
              </form>
            `
            }else{
            const nextData = document.getElementById('sheduled-data-form');
            nextData.innerHTML = `
              <h6 class="mt-3"><b>Schedule</b></h6>
              <form>
                <div  class="row">
                  <div class="col-md-12 mt-2">
                    <label class="input-label-show">Occasion</label>
                    <select class="input-box-view">
                      <option value="">Occasion</option>
                      <option value="Party">Birthday</option>
                      <option value="Party">Small Gathering</option>
                      <option value="Party">Anniversary</option>
                      <option value="Party">Birthday</option>
                      <option value="Party">Corporate</option>
                    </select>
                  </div>
                    <div class="col-md-6 col-6 mt-2">
                    <label class="input-label-show">Date</label>
                    <input type="date" class="input-box-view" id="schedule-date" min="${todayStr}" />
                  </div>
                    <div class="col-md-6 col-6 mt-2">
                    <label class="input-label-show">Time</label>
                    <input type="time" class="input-box-view" id="schedule-time"  min="${minTimeStr}" />
                  </div>
                </div>
              </form>
          `
            }
          document.querySelector('.btn.btn-primary.mt-4').setAttribute('onclick', 'getScheduleData(true)');

          const dateInput = document.getElementById('schedule-date');
          const timeInput = document.getElementById('schedule-time');

          dateInput.addEventListener('change', function () {
            const selectedDateStr = this.value;
            const today = new Date().toISOString().slice(0, 10);

            if (selectedDateStr === today) {
              const now = new Date();
              now.setHours(now.getHours() + 5);
              const minTime = now.toTimeString().slice(0, 5);
              timeInput.min = minTime;

              if (timeInput.value && timeInput.value < minTime) {
                timeInput.value = '';
              }
            } else {
              timeInput.removeAttribute('min');
            }
          });

          // Trigger once to apply the restriction on first load
          dateInput.dispatchEvent(new Event('change'));
          }else{
            document.querySelector('.btn.btn-primary.mt-4').setAttribute('onclick', 'getScheduleData(false)');
          }


          cartHtmlTotal = `
                    <div class="view-cart-invoice-cotainer mt-3">
                      <h5><b>Invoice</b></h5>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center">
                        <p><b>Subtotal</b></p>
                        <p>&#8377;${result.subtotal}</p>
                      </div>
                      <div class="d-flex justify-content-between align-items-center">
                        <p><b>Discount</b></p>
                        <p>${(parseInt(result.discount_percenrage))}% (Rs ${parseInt((result.subtotal) - result.total_payoff)})</p>
                        
                      </div>
                      <hr>
                      <div class="d-flex justify-content-between align-items-center">
                        <p><b>Total</b></p>
                        <p>&#8377;${result.total_payoff}</p>
                      </div>

                      
                    `

          cartContainerTotal.innerHTML += cartHtmlTotal
        }
        else {

          window.location.href = '/'
        }

      }
      const cartId = result.cart_id;
      sessionStorage.setItem('cart_id', cartId);

    })
    .catch((error) => console.error(error));
}


// Cart item remove 

function removeItem(id,type,is_party,quantity){

  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if (tokens) {
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }else{
    showPopup('error',"Having some issue with your connection.")
    return false
  }

  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    "item_id": id,
    "item_type": type,
    "is_party_catering": is_party,
    "quantity": quantity
  });

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
  };

  console.log(raw)

  fetch("http://127.0.0.1:8000/api/remove-item/", requestOptions)
    .then((response) => response.json())
    .then((result) => {

      console.log(result)

      if (result.success) {
        location.reload();
      }else{
        showPopup('error', result.message)
      }

    })
    .catch((error) => console.error(error));


}

// Offer Copy Function ==============================================================================
function copyOfferCode(iconElement) {
  const container = iconElement.closest('.promo-code-text-container');
  const codeText = container.querySelector('.copy-text').innerText;

  navigator.clipboard.writeText(codeText)
    .then(() => {
      // Optionally show feedback (e.g. temporary text/icon change)
      iconElement.classList.remove("fa-copy");
      iconElement.classList.add("fa-check");
      setTimeout(() => {
        iconElement.classList.remove("fa-check");
        iconElement.classList.add("fa-copy");
      }, 1500);
    })
    .catch(err => {
      console.error("Copy failed: ", err);
      alert("Failed to copy code.");
    });
}

// Showing offers Code ========================================================================================


function offerShow() {
  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if (tokens) {
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  } else {
    return false
  }
  myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");

  const requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow"
  };
  fetch("http://127.0.0.1:8000/api/offers/", requestOptions)
    .then((response) => response.json())
    .then((result) => {

      console.log(result.data)

      if (result.data.length > 0) {
        const offersdiv = document.getElementById("promo-code")
        result.data.forEach(item => {
          promohtml = `
              <div class="promo-code-text-container">
                <div class="text">${item.title} : ${item.code}<span class="copy-text">${item.code}</span></div>
                <i class="fa-solid fa-copy copy-icon-show copy-icon" onclick="copyOfferCode(this)" ></i>
              </div>
              `
          offersdiv.innerHTML += promohtml
        })
      } else {
        const offersdiv = document.getElementById("promo-code")
        offersdiv.innerHTML = ''
        promohtml = `
        <div class="coupon-main">
          <div class="coupon-wrapper">
            <div class="percent-icon top-right">%</div>
            <div class="percent-icon bottom-left">%</div>
            <div class="coupon-text">AHUF-NOT-AVAL</div>
          </div>

          <div class="cupon-message">Sorry, currently no coupon available</div>
        </div>`

        offersdiv.innerHTML += promohtml
      }

    })
    .catch((error) => console.error(error));

}

// schedul data fetch 
function getScheduleData(is_party) {

  if (is_party){
    const occasion = document.querySelector('#sheduled-data-form select').value.trim();
    const date = document.querySelector('#sheduled-data-form input[type="date"]').value.trim();
    const time = document.querySelector('#sheduled-data-form input[type="time"]').value.trim();
    console.log(occasion, date, time)

    if (!occasion) {
      showPopup('warning', "Please select an occasion.")
      return;
    }

    if (!date) {
      showPopup('warning', "Please select a date.")
      return;
    }

    if (!time) {
      showPopup('warning', "Please select a time.")
      return;
    }

    // If all values are filled, show them in console (or use as needed)
    console.log("Occasion:", occasion);
    console.log("Date:", date);
    console.log("Time:", time);

    const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
    const tokens = cookieMatch ? cookieMatch[2] : null;
    const myHeaders = new Headers();
    
    if ( tokens){
      myHeaders.append("Authorization", `Bearer ${tokens}`);
    }else{
      return false
    }
    myHeaders.append("Content-Type", "application/json");
    // myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgzNDIxOTY2LCJpYXQiOjE3NTE4ODU5NjYsImp0aSI6IjJhYjdiYzU4YzQ5NzRlZDE5ZmQzMDVhM2JjYmJjZDFhIiwidXNlcl9pZCI6MTB9.n3Y3dat1brT7djI90IW4aZ5cT5rgP55mo4hcTZKRPHs");

    const raw = JSON.stringify({
      "occasion": occasion,
      "scheduled_date": date,
      "scheduled_time": time
    });

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow"
    };

    fetch("http://127.0.0.1:8000/api/schedule-orders/", requestOptions)
      .then((response) => response.json())
      .then((result) => {

        console.log(result)
        if (result.success){
          nextStep()
        }else{
          showPopup('error', result.non_field_errors[0]) // Assuming showPopup is a function to display pop-up messages with i)
        }
      })
      .catch((error) => console.error(error));

    // alert(`Occasion: ${occasion}\nDate: ${date}\nTime: ${time}`);
  }else{
    nextStep()
  }
}


function applyCoupon() {

  console.log("hello i am there")

  const promoCode = document.querySelector('.input-box-view').value;
  if (promoCode == '' || promoCode == null) {
    console.alert('Sorry I dint found any thing.')
  }
  console.log(promoCode);


  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if (tokens) {
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  } else {
    return false
  }
  // myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");
  myHeaders.append("Content-Type", "application/json");
  const raw = JSON.stringify({
    "code": promoCode
  });
  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
  };

  fetch("http://127.0.0.1:8000/api/get-cart/", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      console.log(result)
      if (result.success) {
        window.location.reload()
      }
    })
    .catch((error) => console.error(error));


}



function addAddress() {
  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if (tokens) {
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  } else {
    return false
  }

  let name = document.getElementById('customerName').value.trim()
  let contact = document.getElementById('customerContact').value.trim()
  let email = document.getElementById('customerEmail').value.trim()
  let city = document.getElementById('customerCity').value
  let state = document.getElementById('customerState').value
  let pincode = document.getElementById('customerPincode').value.trim()
  let address = document.getElementById('customerAddress').value.trim()


  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    "full_name": document.getElementById('customerName').value.trim(),
    "phone_number": document.getElementById('customerContact').value.trim(),
    "street_address": document.getElementById('customerAddress').value.trim(),
    "apartment": document.getElementById('customerApartmentAddress').value.trim(),
    "city": document.getElementById('customerCity').value,
    "state_or_region": document.getElementById('customerState').value,
    "postal_code": document.getElementById('customerPincode').value.trim(),
    "email": document.getElementById('customerEmail').value.trim(),
    "country": "India",
    "is_default": true
  });

  console.log("Your entered Data Raw:", raw)

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
  };

  fetch("http://127.0.0.1:8000/api/addresses/", requestOptions)
    .then((response) => response.json())
    .then((result) => {

      if (result.success) {
        window.location.reload();
      }

    })
    .catch((error) => console.error(error));
}


function updateAddress(upid) {

  const customer_full_name = document.getElementById("customer-name").value
  const customer_phone_number = document.getElementById("customer-contact").value
  const customer_email = document.getElementById("email-id").value
  const customer_city = document.getElementById("customer-city").value
  const customer_state_or_region = document.getElementById("customer-state").value
  const customer_street_address = document.getElementById("full-address").value
  const customer_postal_code = document.getElementById("pin-code").value
  const customer_apartment = document.getElementById("apartment-address").value

  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if (tokens) {
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  } else {
    return false
  }
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    "full_name": customer_full_name,
    "phone_number": customer_phone_number,
    "email": customer_email,
    "street_address": customer_street_address,
    "apartment": customer_apartment,
    "city": customer_city,
    "state_or_region": customer_state_or_region,
    "postal_code": customer_postal_code,
    "country": "India",
    "is_default": true
  });

  const requestOptions = {
    method: "PUT",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
  };

  fetch(`http://127.0.0.1:8000/api/addresses/${upid}/update/`, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      console.log(result)
      if (result.success) {
        window.location.reload();
      }
    })
    .catch((error) => console.error(error));

}


function checkOutpay() {


  const selectedAddressDiv = document.querySelector('.card.selected-address');

  let addressId = null;

  if (selectedAddressDiv) {
    const iconTag = selectedAddressDiv.querySelector('i');
    if (iconTag) {
      const onclickValue = iconTag.getAttribute('onclick');
      const match = onclickValue && onclickValue.match(/editSavedAddress\((\d+)\)/);
      addressId = match ? match[1] : null;
    }
  }

  const cartId = sessionStorage.getItem('cart_id');

  console.log(addressId, cartId);

  if (!addressId) {
    showPopup('error', "No address selected Or you have not added any address please add it.");
    return false
  }
  else if (!addressId && !cartId) {
    showPopup('error', "Sorry Something went wrong");
    return false
  }
  else {
    const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
    const tokens = cookieMatch ? cookieMatch[2] : null;
    // setting to local storage for backup 
    if (!localStorage.getItem('backup_access_token')) {
      localStorage.setItem('backup_access_token', tokens);
    }
    
    const myHeaders = new Headers();
    if (tokens) {
      myHeaders.append("Authorization", `Bearer ${tokens}`);
    } else {
      return false
    }
    myHeaders.append("Content-Type", "application/json");

    const requestOptionsCart = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow"
    };

    fetch("http://127.0.0.1:8000/api/get-cart/", requestOptionsCart)
      .then((response) => response.json())
      .then((result) => {

        result

        const raw = JSON.stringify({
          "order_amount": result.total_payoff,
          "order_currency": "INR",
          "customer_details": {
            "customer_id": `cust_0${result.user_id}`,
            "customer_phone": `${result.user_number}`,
            "cart_id": parseInt(cartId),
            "address_id": parseInt(addressId)
          }
        });
        const requestOptions = {
          method: "POST",
          headers: myHeaders,
          body: raw,
          redirect: "follow"
        };
        fetch("http://127.0.0.1:8000/api/pay/?json=true", requestOptions)
          .then((response) => response.json())
          .then((result) => {

            console.log(result)
            window.location.href = result.payment_link
          })






      })
      .catch((error) => console.error(error));




  }
}
