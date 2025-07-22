function openPopup(item_id) {

    const currentPath = window.location.pathname;
    const is_party = currentPath === '/party-catering/' ? true : false ;

    const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
    const tokens = cookieMatch ? cookieMatch[2] : null;
    const myHeaders = new Headers();
    
    if ( tokens){
        myHeaders.append("Authorization", `Bearer ${tokens}`);
    } 
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");
    const requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow"
  };


  let baseUrl = `http://127.0.0.1:8000/combo-data/?is_party_catering=${is_party}&item_id=${item_id}`
  fetch(baseUrl, requestOptions)
    .then((response) => response.json())
    .then((result) => {
        console.log("i am from popup", result)
        const ulcontainer = document.getElementById('combo-list-start')
        const button = ulcontainer.nextElementSibling;

        if (button && button.classList.contains("change-btn")) {
            button.setAttribute("onclick", `goToPlan('${result.data[0].id}' ,'${result.data[0].name.replace(/\s+/g, '')}web' , false ,false , ${is_party} , 'combo' , ${result.data[0].quantity})`);
        }

        ulcontainer.innerHTML = ''
        
        
        result.data[0].menu_items.forEach(el => {
            menuDetailHtml = `<li>${el.name} <img src="${el.imageUrl}"
              class="starter-section-img" /></li>`

        
        ulcontainer.innerHTML += menuDetailHtml
        });
    })
    .catch((error) => console.error(error));



    document.getElementById("popup").style.display = "flex";
    document.body.classList.add("popup-open");
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
    document.body.classList.remove("popup-open");
}

function goToPlan(menuId , id_name , shouldReload ,  is_view_cart , is_party_catering , item_type , quantity ) {
    new_quant = quantity+1
    console.log(new_quant)

    const addCartItem = document.getElementById('eventView')
    addCartItem.innerHTML = ''

    addCartItem.innerHTML = `<button class="back-btn" onclick="backToStarters()"><i class="bi bi-arrow-left-circle fs-5"></i></button>
         
          <div class="text-center">
          <label for="" class="form-label  mt-3"><b>Order Quantity</b></label>
          <div class="quantity-container rounded-3" style="width:100%;max-width: fit-content;margin: auto;">
            <button onclick="deQTY(event , '${id_name}')" class="quantity-btn-show">
              −
            </button>
            <input type="text" name="" value="${quantity}" class="quantity-input-value ${id_name}" />
            <button onclick="inQTY(event , '${id_name}')" class="quantity-btn-show">
              +
            </button>
          </div>
          </div>
         

        <button onclick="decreaseQty('${menuId}','${id_name}', ${shouldReload} , ${is_view_cart} , ${is_party_catering} , '${item_type}'); closePopup();" class="action-btn">Add to Cart</button>`

    if (item_type === "menu"){
        document.getElementById("popup").style.display = "flex";
        document.body.classList.add("popup-open");
    }
    document.getElementById("startersView").style.display = "none";
    document.getElementById("eventView").style.display = "block";
}

// Increase Quatity

function inQTY(event , id_name){
    event.preventDefault()
    const input = document.querySelector(`.${id_name}`)

    console.log(input)

    input.value = parseInt(input.value) + 1
}

function deQTY(event , id_name){
    event.preventDefault()
    const input = document.querySelector(`.${id_name}`)
    input.value = parseInt(input.value) - 1
}

function backToStarters() {
    document.getElementById("eventView").style.display = "none";
    document.getElementById("startersView").style.display = "block";
}

function openParty(evt, partyName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("party-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("party-tablinks");
    for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(partyName).style.display = "block";
    evt.currentTarget.className += " active";
}
const currentPathMain = window.location.pathname;
// Get the element with id="default-Open-tab" and click on it
if (currentPathMain === '/party-catering/'){
    document.getElementById("default-Open-tab").click();
}
// document.getElementById("default-Open-tab").click();