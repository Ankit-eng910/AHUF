
window.addEventListener('DOMContentLoaded', function () {
    document.body.classList.add('page-loaded');
  });

  // Detect if back/forward navigation happened
  window.addEventListener('pageshow', function (event) {
    const navType = performance.getEntriesByType("navigation")[0].type;

    if (event.persisted || navType === "back_forward") {
      // Fade out first
      document.body.classList.remove('page-loaded');

      // Wait for fade out transition, then reload
      setTimeout(function () {
        location.reload();
      }, 200); // match with CSS transition duration
    }
  });



document.addEventListener("DOMContentLoaded", function () {

    // Nav color based on urls
    const navLinks = document.querySelectorAll(".custom-sidebar-link");
    const currentPath = window.location.pathname //.split("/").pop();

    console.log(currentPath)

    navLinks.forEach(link => {
      const linkPath = link.getAttribute("href");

      console.log('I am link path',linkPath)
      if (linkPath === currentPath) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });






  });


function savedAddress(){

}











//   =======================================================

function logoutUser(){
  document.cookie = "access_token=; path=/; max-age=0; secure; samesite=Lax";
  window.location.href = '/api/login-page/'
}


function addAdress(event){
  event.preventDefault()

  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if ( tokens){
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }else{
    return false
  }

  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    "full_name": document.getElementById('customerName').value.trim(),
    "phone_number": document.getElementById('customerContact').value.trim(),
    "street_address": document.getElementById('customerAddress').value.trim(),
    "apartment": document.getElementById('customerApartmentAddress').value.trim(),
    "city": document.getElementById('customerCity').value,
    "state_or_region": document.getElementById('customerState').value,
    "postal_code": document.getElementById('customerPincode').value.trim(),
    "email" : document.getElementById('customerEmail').value.trim(),
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
      
      if (result.success){
        window.location.reload();
      }

    })
    .catch((error) => console.error(error));
}

function opensaveaddress(){
  document.querySelector('.save-address-add-form').style.display = 'block'
}

function editAddress(adId){
  document.querySelector('.edit-address-form').style.display = 'block';

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
      if (result.success){
          // const editAdd = document.querySelector('.edit-address-form')

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
  

};



function cancelAddress(){
  document.querySelector('.edit-address-form').style.display = 'none';
  document.querySelector('.save-address-add-form').style.display = 'none'
};



function updateAddress(upid){

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
  if ( tokens){
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }else{
    return false
  }
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    "full_name": customer_full_name, 
    "phone_number":  customer_phone_number,
    "email" : customer_email,
    "street_address":  customer_street_address,
    "apartment": customer_apartment ,
    "city":  customer_city,
    "state_or_region":  customer_state_or_region,
    "postal_code":  customer_postal_code,
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
      if (result.success){
        window.location.reload();
      }
    })
    .catch((error) => console.error(error));

}

// ==================Add Address=============================
  function toggleAddressForm() {
    const container = document.getElementById('addressFormContainer');
    container.style.display = container.style.display === 'none' ? 'block' : 'none';
  }
// ====================Track Order =============================
document.addEventListener('DOMContentLoaded', () => {
      const steps = document.querySelectorAll('.timeline-step');
      const progressMarker = document.getElementById('progressMarker');
      const isDesktop = window.innerWidth >= 768;
      if (isDesktop) {
        progressMarker.style.width = '0%';
        progressMarker.style.height = '8px';
      } else {
        progressMarker.style.height = steps[0].offsetTop + 25 + 'px';
        progressMarker.style.width = '8px';
      }
    });