function openOrder(evt, orderTitle) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("order-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("order-tablinks");
    for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(orderTitle).style.display = "block";
    evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();


function showPopup(type, message) {
  const container = document.getElementById('popupContainer');
  const popup = document.createElement('div');
  popup.className = `main-popup ${type}` ;
  // popup.role = 'alert';
  popup.innerHTML = `
      <div class="me-2">${type === 'success' ? '✅' : '❌'}</div>
      <div>${message}</div>
     <button class="close-btn ms-auto" onclick="this.parentElement.remove()"><i class="bi bi-x-circle"></i></button>
  `;
  
  container.appendChild(popup);
  setTimeout(() => popup.remove(), 4000);
}


function populateOrderDetails(orderData, activeId) {
  const data = orderData.data;
  
  // Set Onclick Function 
  document.getElementById('btn-to-changed').setAttribute('onclick', `orderPrepared('${data.ahuf_order_id}','${data.created_at_formatted}' , '${data.order_amount}' , '${activeId}' ,'prepared',)`)
  document.getElementById('btn-to-changed-delivery').setAttribute('onclick', `orderPrepared('${data.ahuf_order_id}', '${data.created_at_formatted}', '${data.order_amount}', '${activeId}', 'out-for-delivery')`)
  document.getElementById('btn-to-changed-delivered').setAttribute('onclick', `orderPrepared('${data.ahuf_order_id}', '${data.created_at_formatted}', '${data.order_amount}', '${activeId}', 'delivered')`)
  document.querySelectorAll('.order-show-details-container.active').forEach(el => {
      el.classList.remove('active');
    });

  document.getElementById(`active-${activeId}`).classList.add('active')
  // Set order number and time
  document.querySelector('.order-info h5').textContent = data.ahuf_order_id;
  document.querySelector('.order-info p').textContent = data.created_at_formatted;

  // Set customer name
  document.querySelector('.user-name').textContent = data.address.full_name;

  // Set delivery address
  const fullAddress = `${data.address.street_address}, ${data.address.apartment}, ${data.address.city}`;
  document.querySelector('.user-dlvy-address + .d-flex span').textContent = fullAddress;

  // Set payment info
  document.querySelectorAll('.dlvy-time-details-show')[3].querySelector('span').textContent = "UPI Payment"; // Payment Method
  document.querySelectorAll('.dlvy-time-details-show')[4].querySelector('span').textContent = "Completed";    // Payment Status

//   Clear existing products
  document.querySelectorAll('.information-of-user-order.mt-2').forEach(el => el.remove());
  let products = ``
  data.cart.forEach((item) => {
    editedHtml = `
    <div class="information-of-user-order mt-2">
        <div class="information-of-user-order">
        <img src="${item.menu_item_details.imageUrl}" alt="image" class="order-product-image">
        <div class="order-info ms-1">
            <h5>${item.menu_item_details.name}</h5>
            <p>${item.quantity} items</p>
        </div>
        </div>
        <span class="user-name">₹ ${item.menu_item_details.discounted_price * item.quantity}</span>
    </div>
    `
    products += editedHtml
  })
  console.log(products)

  totalHtml = `
    <div class="information-of-user-order mt-2">
        <span class="user-name"><b>Total</b></span>
        <span class="user-name">₹${data.order_amount}</span>
    </div>
  `
  products+=totalHtml

  const proddetails = document.getElementById('prod-detail')
  proddetails.innerHTML += products
    if (['PREPARING'].includes(data.order_status)){
    const btn = document.getElementById('btn-to-changed');
    const delBtn = document.getElementById('btn-to-changed-delivery');
        const delBtned = document.getElementById('btn-to-changed-delivered');
        if (btn && delBtn && delBtned) {

            delBtned.disabled = false;  
            delBtned.classList.remove('btn-secondary');
            delBtned.classList.add('btn-success');
            delBtned.innerText = 'Delivered';

            btn.disabled = true;
            delBtn.disabled = false;                           
            btn.classList.add('btn-secondary');
            delBtn.classList.remove('btn-secondary');            
            btn.classList.remove('btn-success');  
            delBtn.classList.add('btn-success');         
            btn.innerText = 'Preparing';      
            delBtn.innerText = 'Out for Delivery';
        }    
    }
    else if (['OUT_FOR_DELIVERY'].includes(data.order_status)) {
    const btn = document.getElementById('btn-to-changed');
    const delBtn = document.getElementById('btn-to-changed-delivery');
        const delBtned = document.getElementById('btn-to-changed-delivered');
        if (btn && delBtn && delBtned) {
            delBtned.disabled = false;  
            delBtned.classList.remove('btn-secondary');
            delBtned.classList.add('btn-success');
            delBtned.innerText = 'Delivered';

            btn.disabled = true;
            delBtn.disabled = true;                           
            btn.classList.add('btn-secondary');
            delBtn.classList.add('btn-secondary');            
            btn.classList.remove('btn-success');  
            delBtn.classList.remove('btn-success');         
            btn.innerText = 'Prepared';      
            delBtn.innerText = 'Out for Delivery';
        }
    }else if (['DELIVERED'].includes(data.order_status)){
    const btn = document.getElementById('btn-to-changed');
    const delBtn = document.getElementById('btn-to-changed-delivery');
    const delBtned = document.getElementById('btn-to-changed-delivered');
        if (btn && delBtn && delBtned) {
            delBtned.disabled = true;  
            delBtned.classList.add('btn-secondary');
            delBtned.classList.remove('btn-success');
            delBtned.innerText = 'Delivered';

            btn.disabled = true;
            delBtn.disabled = true;                           
            btn.classList.add('btn-secondary');
            delBtn.classList.add('btn-secondary');            
            btn.classList.remove('btn-success');  
            delBtn.classList.remove('btn-success');         
            btn.innerText = 'Prepared';      
            delBtn.innerText = 'Out for Delivery';
        }

    }else {
    const btn = document.getElementById('btn-to-changed');
    const delBtn = document.getElementById('btn-to-changed-delivery');
    const delBtned = document.getElementById('btn-to-changed-delivered');
        if (btn && delBtn && delBtned) {
        delBtned.disabled = false;  
        delBtned.classList.remove('btn-secondary');
        delBtned.classList.add('btn-success');
        delBtned.innerText = 'Delivered';

        btn.disabled = false;
        delBtn.disabled = false;
        btn.classList.remove('btn-secondary');
        delBtn.classList.remove('btn-secondary');
        btn.classList.add('btn-success');
        delBtn.classList.add('btn-success')
        btn.innerText = 'Sart Preparing';
        delBtn.innerText = 'Out for Delivery'
    }
    }

}

function ordersdetials(order_id, activeId){


    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
    "ahuf_order_id": order_id
    });

    const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
    };

    fetch("http://127.0.0.1:8000/api/getOrders-by-id/", requestOptions)
    .then((response) => response.json())
    .then((result) => {

        if (result.success) {
        populateOrderDetails(result, activeId);
        } else {
        console.error("Error:", result.message);
        }


    })
    .catch((error) => console.error(error));
}





function orderPrepared(orderId , createdAtFormatted, orderAmount, forloopCounter , status){

    console.log(orderId, status)

    let order_status = status === 'prepared' ? "PREPARING" : status === "delivered" ? 'DELIVERED' : "OUT_FOR_DELIVERY"

    
    

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
    "ahuf_order_id": orderId,
    "status": order_status
    });

    const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
    };

    fetch("http://127.0.0.1:8000/api/change-order-status/", requestOptions)
    .then((response) => response.json())
    .then((result) => {

        if (result.success) {
            console.log(order_status)
            // moving order one to other position
            if (order_status === "PREPARING"){
              const btn = document.getElementById('btn-to-changed');
              const delBtn = document.getElementById('btn-to-changed-delivery');
                  const delBtned = document.getElementById('btn-to-changed-delivered');
                  if (btn && delBtn && delBtned) {

                      delBtned.disabled = false;  
                      delBtned.classList.remove('btn-secondary');
                      delBtned.classList.add('btn-success');
                      delBtned.innerText = 'Delivered';

                      btn.disabled = true;
                      delBtn.disabled = false;                           
                      btn.classList.add('btn-secondary');
                      delBtn.classList.remove('btn-secondary');            
                      btn.classList.remove('btn-success');  
                      delBtn.classList.add('btn-success');         
                      btn.innerText = 'Preparing';      
                      delBtn.innerText = 'Out for Delivery';
                  }    
              }
              else if (order_status === 'OUT_FOR_DELIVERY') {
              const btn = document.getElementById('btn-to-changed');
              const delBtn = document.getElementById('btn-to-changed-delivery');
                  const delBtned = document.getElementById('btn-to-changed-delivered');
                  if (btn && delBtn && delBtned) {
                      delBtned.disabled = false;  
                      delBtned.classList.remove('btn-secondary');
                      delBtned.classList.add('btn-success');
                      delBtned.innerText = 'Delivered';

                      btn.disabled = true;
                      delBtn.disabled = true;                           
                      btn.classList.add('btn-secondary');
                      delBtn.classList.add('btn-secondary');            
                      btn.classList.remove('btn-success');  
                      delBtn.classList.remove('btn-success');         
                      btn.innerText = 'Prepared';      
                      delBtn.innerText = 'Out for Delivery';
                  }
              }else if (order_status === 'DELIVERED'){
              const btn = document.getElementById('btn-to-changed');
              const delBtn = document.getElementById('btn-to-changed-delivery');
              const delBtned = document.getElementById('btn-to-changed-delivered');
                  if (btn && delBtn && delBtned) {
                      delBtned.disabled = true;  
                      delBtned.classList.add('btn-secondary');
                      delBtned.classList.remove('btn-success');
                      delBtned.innerText = 'Delivered';

                      btn.disabled = true;
                      delBtn.disabled = true;                           
                      btn.classList.add('btn-secondary');
                      delBtn.classList.add('btn-secondary');            
                      btn.classList.remove('btn-success');  
                      delBtn.classList.remove('btn-success');         
                      btn.innerText = 'Prepared';      
                      delBtn.innerText = 'Out for Delivery';
                  }

              }
            moveToPrepared(orderId , createdAtFormatted, orderAmount, forloopCounter , status);
            // pop up sucess message
            showPopup('success', result.message);
        }else{
            showPopup('error', result.message);
        }

    })
    .catch((error) => console.error(error));
}


function moveToPrepared(orderId, createdAtFormatted, orderAmount, forloopCounter, status) {
  const element = document.getElementById(`active-${forloopCounter}`);
  if (!element) return;

  // Remove it from In Progress
  element.remove();

  // Modify the content
  const newDiv = document.createElement('div');
  newDiv.id = `active-${forloopCounter}`;
  newDiv.className = 'order-show-details-container';
  newDiv.setAttribute('onclick', `ordersdetials('${orderId}','${forloopCounter}')`);
  if (status === 'prepared'){
    newDiv.innerHTML = `
      <div class="first-order-dtls">
        <h4 id="${forloopCounter}">${orderId}</h4>
        <p>${createdAtFormatted}</p>
      </div>
      <div class="prepared">Preparing</div>
      <h5 class="order-price-show">₹${orderAmount} <i class="bi bi-arrow-right-circle-fill" style="color:#ED8F37"></i></h5>
    `;
  }else if (status === 'out-for-delivery'){
    newDiv.innerHTML = `
      <div class="first-order-dtls">
        <h4 id="${forloopCounter}">${orderId}</h4>
        <p>${createdAtFormatted}</p>
      </div>
      <h5 class="order-price-show">₹${orderAmount} <i class="bi bi-arrow-right-circle-fill" style="color:#ED8F37"></i></h5>
    `;
  }
  document.getElementById(status).appendChild(newDiv);
}




document.addEventListener('DOMContentLoaded', function () {
  const firstH4 = document.querySelector('#order-in h4');
  const firstId = firstH4 ? firstH4.id : null;
  
  
  const defaultOrderId = document.getElementById(firstId).textContent.trim();
  
  ordersdetials(defaultOrderId , firstId );
});


// ====================OTP POPUP=======================
const modal = document.getElementById("pinModal");
    const inputs = document.querySelectorAll(".otp-input");

    inputs.forEach((input, index) => {
      input.addEventListener("input", () => {
        if (input.value.length === 1) {
          if (index < inputs.length - 1) {
            inputs[index + 1].focus();
          }
        }
        checkIfFilled();
      });

      input.addEventListener("keydown", (e) => {
        if (e.key === "Backspace" && input.value === "" && index > 0) {
          inputs[index - 1].focus();
        }
      });
    });

    function checkIfFilled() {
      const allFilled = Array.from(inputs).every(input => input.value !== "");
      if (allFilled) {
        modal.style.display = "none";
      }
    }
