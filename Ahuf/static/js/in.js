



// ---------------------------Menu Items API-------------------------------------



function seachedMenuItems(event){
  event.preventDefault()

  // Getting seach value
  const searchInputElement = document.getElementById("searchInput");
  if (window.matchMedia("(max-width: 992px)").matches) {
    
    document.querySelector(".close-menu").click();
  }
 
  const searchInput = searchInputElement.value;
  searchInputElement.value = "";
  


  // Desabling the subcategories and adding new seached Menu
  const tabContainer = document.getElementById("subcategory-tabs");
  const unorderedList = document.getElementById("our-menu-container");

  tabContainer.innerHTML = '';  // Clear existing tabs
  unorderedList.innerHTML = ""; // Clear existing items

  const newlist = document.createElement("li");
  const newLink = document.createElement("a");

  newLink.className = "dropdown-item";
  newLink.href = "#";
  newLink.textContent = "Searhed Menu";
  
  newlist.appendChild(newLink);
  unorderedList.appendChild(newlist);

  const btn = document.createElement("button")
  btn.className = "tablinks";
  btn.textContent = "Searhed Menu";
  btn.id = "defaultOpen";
  tabContainer.appendChild(btn);


  // Removing Existing Tabs 

  const existingTabs = document.querySelectorAll(".tabcontent");
  existingTabs.forEach(tab => {
      tab.classList.remove("show");
      tab.classList.add("fade-out");
      tab.remove()
  });



  // API FETCH
  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if ( tokens){
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }
  myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");

  const requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow"
  };

  fetch(`http://127.0.0.1:8000/api/searchmenu/?search_query=${searchInput}`, requestOptions)
    .then((response) => response.json())
    .then((result) => {

      const divAdd = document.createElement("div");
      const RowAdd = document.createElement("div");
      const container1 = document.getElementById("menu-container1");
      container1.innerHTML = ''
      RowAdd.className = "row";
      divAdd.appendChild(RowAdd);
      divAdd.className = "tabcontent show";
      divAdd.classList.add("fade-in")

        result.data.forEach((item) => {
          
          dishHtml = `
              <div class="col-md-4 mt-3 combo-fade-in">
                <div class="trending-recipes-container">
                  <a onclick="ShowPop('${item.category_name}','${item.subcategory_name}','${item.name}')" ><div class="share-icon">
                    <i class="fa-solid fa-share-nodes"></i>
                  </div></a>
                  <div class="text-center">
                    <a onclick="menuPage('${item.category_name}','${item.subcategory_name}','${item.name}')" ><img
                      src="${item.imageUrl}"
                      alt="icon"
                      class="main-food-image"
                    /></a>
                  </div>
                  <div><span class="off-precent">${parseInt(item.calculated_discount)}% OFF</span></div>
                  <h4>${item.name}</h4>

                  <p>
                 ${item.description.substring(0, 80)}...
                  </p>
                  <div class="icon">
                    <span>${item.avg_reviews} <i class="bi bi-star-fill"></i></span> (${item.total_reviews}
                    Reviews)
                  </div>
                  <h5 class="price-number">
                    &#8377;${parseInt(item.discounted_price)}
                    <span
                      class="text-muted"
                      style="text-decoration: line-through"
                      >&#8377;${parseInt(item.price)}</span
                    >
                  </h5>
                  <div
                    class="d-flex justify-content-between align-items-center"
                  >
                    <a href="#">
                      <button class="explore-more mt-3 rounded-3">
                        Add To Cart
                      </button>
                    </a>
                    <div class="quantity-container mt-3 rounded-3">
                      <button onclick="decreaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web')" class="quantity-btn-show">
                        −
                      </button>
                      <input
                        type="text"
                        name=""
                        value="${item.quantity}"
                        readonly
                        class="quantity-input-value ${item.name.replace(/\s+/g, '')}web"
                      />
                      <button onclick="increaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web')" class="quantity-btn-show">
                        +
                      </button>
                    </div>
                  </div>
                </div>
              </div>`;

            filerMenu = `<div class="col-6 mt-4 combo-fade-in">
                      <div class="mobile-recommended-container">
                        <div><a><img src="${item.imageUrl}" alt="" /></a></div>
                        <h6>${item.name.substring(0, 20)}...</h6>
                        <p style="margin-bottom:3px">${item.description.substring(0, 35)}...</p>
                        <div class="d-flex align-items-center justify-content-between">

                        <div class="icon">
                          <span>${item.avg_reviews} <i class="bi bi-star-fill"></i></span> (${item.total_reviews})
                        </div>
                        <div class="quantity-container rounded-3" style="border:none">
                    <button onclick="decreaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web')" class="quantity-btn-show">−</button>
                    <input
                      type="text"
                      name=""
                      value="${item.quantity}"
                      readonly
                      class="quantity-input-value ${item.name.replace(/\s+/g, '')}web"
                    />
                    <button onclick="increaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web')" class="quantity-btn-show">+</button>
                  </div>
                    </div>

                        <h5 class="price-number">
                          <b>&#8377;${parseInt(item.discounted_price)}</b>
                          <span
                            class="text-muted"
                            style="text-decoration: line-through; font-size: 16px"
                            >&#8377;${parseInt(item.price)}</span
                          >
                        </h5>
                              
                      </div>
                    </div>`

            RowAdd.innerHTML += dishHtml;
            if (container1) container1.innerHTML += filerMenu;

        })


        const container = document.getElementById("menu-container");
        if (container) container.appendChild(divAdd);
        document.getElementById("defaultOpen").classList.add("active");
        

    })
    .catch((error) => console.error(error));


}





function loadSubCategories(categoryId, event , menuItem = null , subcat = null) {
    event.preventDefault(); // Prevent default anchor click behavior

    const allPTags = document.querySelectorAll(".single-combo-item p");
    console.log(allPTags)
    allPTags.forEach(p => p.classList.remove("active-tag"));
    const element = document.getElementById(`${categoryId}`);
    if (element) {
      const pTag = element.querySelector("p");
      if (pTag) {
        pTag.classList.add("active-tag");
      }
    }

    const requestOptions = {
      method: "GET",
      redirect: "follow",
    };
    
    fetch(
      `http://127.0.0.1:8000/api/subcategories/?category_id=${categoryId}`,
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        data = data.data
        // console.log(data);

        // if (Array.isArray(data) && data.length === 0) {
        //   alert("Sorry, no data found");
        //   console.error("Sorry, no data found");
        //   return;
        // }

        const tabContainer = document.getElementById("subcategory-tabs");
        // const unorderedList = document.getElementById("our-menu-container");


        // <button class="tablinks" onclick="openMenu(event, 'all-recipes')" id="defaultOpen">All</button>
        tabContainer.innerHTML = '';  // Clear existing tabs
        // unorderedList.innerHTML = ""; // Clear existing items

        // Add "All" tab
        // const newlist = document.createElement("li");
        // const newLink = document.createElement("a");

        // newLink.className = "dropdown-item";
        // newLink.href = "#";
        // newLink.textContent = "All Recipes";
        // newLink.onclick = (event) => openMenu(event, 'all-recipes', data[0].category);
        // newlist.appendChild(newLink);
        // unorderedList.appendChild(newlist);

        const btn = document.createElement("button")
        btn.className = "tablinks";
        btn.textContent = "All";
        btn.id = "defaultOpen";
        
        btn.onclick = (event) => openMenu(event, 'all-recipes' , data[0].category);

        console.log(btn)
        
        tabContainer.appendChild(btn);

        // Add subcategory buttons
        if (data.length > 0) {
          data.forEach((sub) => {
            // For subcategories
            const btn = document.createElement("button");
            btn.className = "tablinks";
            btn.textContent = sub.name;
             
            if (sub.id){
              btn.onclick = (event) =>
                openMenu(event, sub.name.toLowerCase().replace(/\s+/g, "-") ,sub.category,sub.id);
            }
            else{
              btn.onclick = (event) =>
                openMenu(event, sub.name.toLowerCase().replace(/\s+/g, "-"), sub.category , null);
            }
            btn.id = sub.name.toLowerCase().replace(/\s+/g, "-")+sub.id;
            console.log(btn.id , menuItem)
            
            tabContainer.appendChild(btn);

            // For menu items
            // const newlist = document.createElement("li");
            // const newLink = document.createElement("a");
            // newLink.className = "dropdown-item";
            // newLink.href = "#";
            // newLink.onclick = (event) =>
            //   openMenu(event, sub.name.toLowerCase().replace(/\s+/g, "-"), sub.category, sub.id);
            // newLink.textContent = sub.name;

            // newlist.appendChild(newLink);
            // unorderedList.appendChild(newlist);
             
          });
        }


        if (menuItem !== null){
          document.getElementById(menuItem+subcat).click();
        }
        else{
          document.getElementById("defaultOpen").click();
        }
      })
      .catch((error) => console.error(error));

      
  }

function recomendation(){

    const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
    const tokens = cookieMatch ? cookieMatch[2] : null;
    const myHeaders = new Headers();
    if ( tokens){
      myHeaders.append("Authorization", `Bearer ${tokens}`);
    }
    const requestOptions = {
        method: "GET",
        headers: myHeaders,
        redirect: "follow"
      };
      
      fetch("http://127.0.0.1:8000/api/recomdated-menu/", requestOptions)
        .then((response) => response.json())
        .then((result) =>{
            
            if (result.success){
                
                const RecomDiv = document.getElementById("recomded")
                const MobRecomDiv = document.getElementsByClassName("g-2")[0]
                // console.log('MobRecomDiv',MobRecomDiv)
                result.data.forEach((item) => {
                    Mobhtml = `
                    <div class="col-6 mt-3 combo-fade-in">
                      <a onclick="menuPage('${item.category_name}','${item.subcategory_name}','${item.name}')"> <div class="new-home-page-card-container" style="background:url('${item.imageUrl}') center/cover no-repeat">
             <div class="ribbon">
              <span class="white">Pre</span><span>mium Options</span>
             </div>
                   
               <div class="home-info-details">
               <div class="d-flex justify-content-between align-items-baseline">
               <div>
                 <h1>${item.name.substring(0, 15)}...</h1>
                 <p class="rating">${item.avg_reviews} <i class="bi bi-star-fill"></i></p>
               </div>
               <a onclick="ShowPop('${item.category_name}','${item.subcategory_name}','${item.name}')" >
               <div class="menushare-icon-show">
                    <i class="fa-solid fa-share-nodes"></i>
                  </div></a>
               </div>
              <div class="d-flex justify-content-between align-items-center mt-2">
               <p class="card-price"> &#8377;${parseInt(item.discounted_price)} <span>&#8377;${parseInt(item.price)}</span></p>
              <div class="d-flex justify-content-between align-items-center rounded-3">
                      <button onclick="decreaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web')" class="quantity-btn-show new-quantity-decrease-icon">
                        −
                      </button>
                      <input
                        type="text"
                        name=""
                        value="${item.quantity}"
                        readonly
                        class="quantity-input-value2 ${item.name.replace(/\s+/g, '')}web"
                      />
                      <button onclick="increaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web')" class="quantity-btn-show new-quantity-decrease-icon">
                        +
                      </button>
                    </div>
              </div>
               </div>
                </div>
                </a>
                         
                    </div>   `


                    addhtml = `
                        <div class="col-md-3 mt-3 combo-fade-in">
                            <a onclick="menuPage('${item.category_name}','${item.subcategory_name}','${item.name}')" ><div class="new-home-page-card-container" style="background:url('${item.imageUrl}') center/cover no-repeat">
             <div class="ribbon">
              <span class="white">Pre</span><span>mium Options</span>
             </div>
               <div class="home-info-details">
               <div class="d-flex justify-content-between align-items-baseline">
               <div>
                 <h1>${item.name}</h1>
                 <p class="rating">${item.avg_reviews} <i class="bi bi-star-fill text-warning"></i> <span>(${item.total_reviews})</span></p>
               </div>
                <a onclick="ShowPop('${item.category_name}','${item.subcategory_name}','${item.name}')" ><div class="share-icon" >
                            <i class="fa-solid fa-share-nodes"></i>
                            </div></a>
               </div>
              <div class="d-flex justify-content-between align-items-center mt-2">
               <p class="card-price">  &#8377;${parseInt(item.discounted_price)} <span>&#8377;${parseInt(item.price)}</span></p>
              <div class="d-flex justify-content-between align-items-center rounded-3">
                      <button onclick="decreaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web')" class="quantity-btn-show new-quantity-decrease-icon">
                        −
                      </button>
                      <input
                        type="text"
                        name=""
                        value="${item.quantity}"
                                readonly
                                class="quantity-input-value2 ${item.name.replace(/\s+/g, '')}web"
                      />
                      <button onclick="increaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web')" class="quantity-btn-show new-quantity-decrease-icon">
                        +
                      </button>
                    </div>
              </div>
               </div>
                </div>
                </a>
                        </div>
                    `

                    RecomDiv.innerHTML += addhtml
                    MobRecomDiv.innerHTML += Mobhtml

                });

            }
        })
        .catch((error) => console.error(error));


  }




function multiplecomboadd(id = null ){
  // checking current page
  const currentPath = window.location.pathname;
  const is_party = currentPath === '/party-catering/' ? true : false ;


  let baseUrl
  if ( id != null){
    const allPTags = document.querySelectorAll(".multi-combo-item p");
      allPTags.forEach(p => p.classList.remove("active-tag"));
      const element = document.getElementById(`combo-${id}`);
      if (element) {
        const pTag = element.querySelector("p");
        if (pTag) {
          pTag.classList.add("active-tag");
        }
      }
    baseUrl = `http://127.0.0.1:8000/combo-data/?category_id=${id}&is_party_catering=${is_party}` 
  }else{
    baseUrl = `http://127.0.0.1:8000/combo-data/?is_party_catering=${is_party}`
  }

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

  fetch(baseUrl, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      
      console.log(result)
      if (result.success) {
        const muliple_combo = document.getElementById("multiple-combo-product")
        muliple_combo.innerHTML = ""
        result.data.forEach((item) =>{

          // Adding button format based on pages.
          let btn
          if (currentPath === '/party-catering/'){
            btn = `<button onclick="openPopup(${item.id})" class="explore-more mt-3" style="padding: 8px 7px;     font-size: 10px;">
                    Add To Cart
                  </button>`
          }else{
            btn = `<button onclick="decreaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web', false , false , ${is_party} , 'combo')" class="quantity-btn-show new-quantity-decrease-icon">
                      −
                    </button>
                    <input 
                        type="text" 
                        name="" 
                        value="${item.quantity}" 
                        readonly class="quantity-input-value2 ${item.name.replace(/\s+/g, '')}web" />
                    <button onclick="increaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web', false , false , ${is_party} , 'combo')" class="quantity-btn-show new-quantity-decrease-icon">
                      +
                    </button>`
          }


          // Main Item
          comboHtml =  `
          <div  class="col-xl-3 col-lg-3 col-md-3 col-6 mt-3 combo-fade-in">
            <div class="new-home-page-card-container" 
              style="background:url('${item.imageUrl}') center/cover no-repeat">
              <div class="ribbon">
                Premium Options
              </div>

              <div class="home-info-details">
                <div class="d-flex justify-content-between align-items-baseline">
                  <div>
                    <h1>${item.name}</h1>
                    <p class="rating">${item.avg_reviews} <i class="bi bi-star-fill text-warning"></i> <span>(${item.total_reviews} Reviews)</span></p>
                  </div>
                  <a href="#" class="text-decoration-none">
                    <div class="share-icon">
                      <i class="fa-solid fa-share-nodes"></i>
                    </div>
                  </a>
                </div>
                <div class="d-flex justify-content-between align-items-center mt-2">
                  <p class="card-price"> &#8377;${parseInt(item.discounted_price)} <span>&#8377;${parseInt(item.price)}</span></p>
                  <div class="d-flex justify-content-between align-items-center rounded-3">
                    ${btn}
                  </div>
                </div>
              </div>
            </div>
          </div>
          `

          // onclick="increaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web', false , false , ${is_party} , 'combo')" 
                    
          
          muliple_combo.innerHTML += comboHtml
          
        })


      }

    })
    .catch((error) => console.error(error));

  

}



document.addEventListener("DOMContentLoaded", function () {
  // console.log("I am DOM Event listner caller!")
  const currentPath = window.location.pathname;
  if (currentPath === '/' || currentPath === '/api/home-page/' || currentPath === '/party-catering/' ) {
    if (sessionStorage.getItem("menu_evt") === "true") {

      
      const menuItem = sessionStorage.getItem("menuItem");
      const CatID = sessionStorage.getItem("CatID");
      const SubcatId = sessionStorage.getItem("SubcatId");

      // Optional: create a fake event if needed
      const fakeEvent = new Event('click');

      // Call your original function
      loadSubCategories(CatID, fakeEvent,menuItem,SubcatId);
      // openMenu(fakeEvent, menuItem, CatID, SubcatId);

      // Clear the flag so it doesn't trigger again on reload
      sessionStorage.removeItem("menu_evt");
      sessionStorage.removeItem("menuItem");
      sessionStorage.removeItem("CatID");
      sessionStorage.removeItem("SubcatId");
    }
    else{
      loadSubCategories(3, event);
    }
  }
  if (currentPath === '/' || currentPath === '/api/menu-detils/') {
    recomendation();
  }
  if (currentPath ==='/party-catering/' ||  currentPath ==='/combo-main-page/' ){
    const firstComboItem = document.querySelector('#combo .combo-item');
    if (firstComboItem) {
      const comboId = firstComboItem.id;
      console.log('First combo-item ID:', comboId);
      document.getElementById(comboId).click();
    }
    
  }else if (currentPath === '/'){
    multiplecomboadd()
  }
  
});


function menuPage(categoryname,subcatname,menuName){

  // console.log(`/api/menu-detils/${categoryname}/${subcatname}/${menuName}/`)

  window.location.href = `/api/menu-detils/${categoryname}/${subcatname}/${menuName}/`;

}

function shareOnFacebook() {
      const shareLinkEl = document.getElementById('share-link');
      const shareUrl = encodeURIComponent(shareLinkEl.innerHTML);
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${shareUrl}`, '_blank');
    }
function shareOnTwitter() {
      const shareLinkEl = document.getElementById('share-link');
      const shareUrl = encodeURIComponent(shareLinkEl.innerHTML);
      const shareText = encodeURIComponent("Check this out!");
      window.open(`https://twitter.com/intent/tweet?url=${shareUrl}&text=${shareText}`, '_blank');
    }
function shareOnWhatsApp() {
      const shareLinkEl = document.getElementById('share-link');
      const shareUrl = encodeURIComponent(shareLinkEl.innerHTML);
      const shareText = encodeURIComponent("Check this out!");
      window.open(`https://wa.me/?text=${shareText}%20${shareUrl}`, '_blank');
    }
function shareOnEmail() {
      const shareLinkEl = document.getElementById('share-link');
      const body = encodeURIComponent(shareLinkEl.innerHTML);
      const subject = encodeURIComponent("Check this out!");
      window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    }
function shareOnInstagram() {
    const instagramProfileUrl = "https://www.instagram.com/";
    window.open(instagramProfileUrl, '_blank');
    }

function ShowPop(categoryName,subcatName,itemName) {
  var myModal = new bootstrap.Modal(document.getElementById('sharePopModal'));
  const shareLinkEl = document.getElementById('share-link');
  const encodedCategory = encodeURIComponent(categoryName);
  const encodedSubcat = encodeURIComponent(subcatName);
  const encodedItem = encodeURIComponent(itemName);


  const fullUrl = `${window.location.origin}/api/menu-detils/${encodedCategory}/${encodedSubcat}/${encodedItem}/`;
  shareLinkEl.innerHTML = fullUrl;
  shareLinkEl.setAttribute('data-url', fullUrl);
  myModal.show();
}

function copyToClipboard() {
  const shareLinkEl = document.getElementById('share-link');
  const text = shareLinkEl.textContent;
  navigator.clipboard.writeText(text).then(() => {
    showPopup('success', 'Copied to clipboard');
  }).catch(err => {
    console.error('Clipboard copy failed:', err);
    showPopup('error', 'Failed to copy');
  });
};




