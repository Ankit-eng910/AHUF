
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


// (() => {
//   const openNav = document.querySelector(".open-menu"),
//       closeNav = document.querySelector(".close-menu"),
//       navMenu = document.querySelector(".nav-link-container"),
//       background = document.querySelector(".background"),
//       mediaSize = 992;

   
//   openNav.addEventListener("click", toggleMenu);
//   closeNav.addEventListener("click", toggleMenu);
//   background.addEventListener("click", toggleMenu);
//   function toggleMenu() {
//       navMenu.classList.toggle("open");
//       background.classList.toggle("active");
//   }


//   navMenu.addEventListener("click", (event) => {
//       if (event.target.hasAttribute("data-toggle") && window.innerWidth <= mediaSize) {
//           event.preventDefault();
//           const dropdownMenuBranch = event.target.parentElement;

  
//           if (dropdownMenuBranch.classList.contains("active")) {
//               collapseDropdownMenu(dropdownMenuBranch);
//           } else {

//             if (navMenu.querySelector(".dropdown-menu-branch.active")) {
//                   collapseDropdownMenu(navMenu.querySelector(".dropdown-menu-branch.active"));
//               }

            
//               dropdownMenuBranch.classList.add("active");
//               const dropdownMenu = dropdownMenuBranch.querySelector(".dropdown-main-menu");
//               dropdownMenu.style.maxHeight = dropdownMenu.scrollHeight + "px";
//           }
//       }
//   });


//   function collapseDropdownMenu(menuBranch = null) {
//       if (menuBranch) {
//           const dropdownMenu = menuBranch.querySelector(".dropdown-main-menu");
//           dropdownMenu.style.maxHeight = null;  
//           menuBranch.classList.remove("active");
//       }
//   }

   
//   window.addEventListener("resize", () => {
//       if (window.innerWidth > mediaSize) {
//           if (navMenu.classList.contains("open")) {
//               toggleMenu();
//           }
//           if (navMenu.querySelector(".dropdown-menu-branch.active")) {
//               collapseDropdownMenu(navMenu.querySelector(".dropdown-menu-branch.active"));
//           }
//       }
//   });
// })();


//   -----------------Products Slider---------------------------
document.addEventListener("DOMContentLoaded", function () {
    new Swiper(".products-slider", {
      spaceBetween: 10,
      speed: 800, // Smooth transition
      loop: true,
      grabCursor: true,
      // autoplay: {
      //   delay: 4000,
      //   disableOnInteraction: false,
      // },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      breakpoints: {
        0: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 2,
        },
      },
    });
  });

  // ===================Featured Categories============================
  document.addEventListener("DOMContentLoaded", function () {
    new Swiper(".featured-category-slider", {
      slidesPerView: 5,
      spaceBetween: 10,
      speed: 800, // Smooth transition
      loop: true,
      grabCursor: true,
      autoplay: {
        delay: 4000,
        disableOnInteraction: false,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      breakpoints: {
        0: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 2,
        },
        1024: {
          slidesPerView: 6,
        },
        1300: {
          slidesPerView: 7,
        },
      },
    });
  });
  //   -----------------Testimonial Slider---------------------------
 document.addEventListener("DOMContentLoaded", function () {
    new Swiper(".testimonial-slider", {
      slidesPerView: 3,
      spaceBetween: 10,
      speed: 800,
      loop: true,
      grabCursor: true,
      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
      },
      breakpoints: {
        0: { slidesPerView: 1 },
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
      },
    });

document.querySelectorAll(".copy-icon").forEach(function (copyBtn) {
      copyBtn.addEventListener("click", function () {
        const banner = copyBtn.closest(".offer-banner-slider");
        const textElem = banner.querySelector(".copy-text");
        const popup = banner.querySelector(".copy-popup");
        const text = textElem.innerText;

        // Copy to clipboard
        navigator.clipboard.writeText(text).then(function () {
          popup.classList.add("show");
          setTimeout(() => {
            popup.classList.remove("show");
          }, 2000); // Show for 2 seconds
        }).catch(function (err) {
          console.error("Copy failed:", err);
        });
      });
    });
  });


const currentPath = window.location.pathname;
let runApi = true;

// console.log(currentPath.startsWith('/api/menu-detils/'))
if (currentPath === '/' || currentPath.startsWith('/api/menu-detils/') || currentPath === '/party-catering/') {
  runApi = true;
} else {
  runApi = false;
}



//   ---------------------Our Menu Tabs---------------------------
function openMenu(evt,menuItem , CatID , SubcatId ) {

  

  const currentPath = window.location.pathname;
  console.log(currentPath)
  if (currentPath.startsWith('/api/menu-detils/')){

    sessionStorage.setItem("menu_evt", "true");   
    sessionStorage.setItem("menuItem", menuItem);
    sessionStorage.setItem("CatID", CatID);
    sessionStorage.setItem("SubcatId", SubcatId);
    is_party_catering = false
    // Redirect to home
    window.location.href = "/";
  }else if (currentPath === "/party-catering/"){
    is_party_catering = true
  }else {
    is_party_catering = false
  }

  evt.preventDefault();
  var i, tabcontent, tablinks;
  
  console.log("CatID", CatID, "SubcatId", SubcatId, 'menuItem', menuItem) 
  

  const existingTabs = document.querySelectorAll(".tabcontent");
   
  existingTabs.forEach(tab => {
    // if (tab.id !== menuItem) {
      tab.classList.remove("show");
      tab.classList.add("fade-out");
      
      tab.remove()
      // setTimeout(() => tab.remove(), 400); // after fade
    // }
  });
  
  

  tablinks = document.getElementsByClassName("tablinks");
  
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
   
   
  
   // ---------------------------Menu Items API-------------------------------------
    const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
    const tokens = cookieMatch ? cookieMatch[2] : null;
    const myHeaders = new Headers();
    if ( tokens){
      myHeaders.append("Authorization", `Bearer ${tokens}`);
    }
    const isAllRecipes = (menuItem === "all-recipes");
    const baseUrl = `http://127.0.0.1:8000/api/get-menu-items/?is_party_catering=${is_party_catering}&categoryId=${CatID || 3}` +
                  (isAllRecipes ? "" : `&subCategoryId=${SubcatId}`);

    myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");
    // console.log(baseUrl)
    const requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow"
    };

    // if (CatID === undefined || CatID === null) {
    //   console.log("CatID is undefined or null");
    //   CatID = 3
    // }
    fetch(baseUrl, requestOptions)
      .then((response) => response.json())
      .then((result) => {

        result  = result.data
        const divAdd = document.createElement("div");
        const RowAdd = document.createElement("div");
        const container1 = document.getElementById("menu-container1");
        container1.innerHTML = ''
        RowAdd.className = "row";
        divAdd.appendChild(RowAdd);
        divAdd.id = menuItem;
        divAdd.className = "tabcontent";
        divAdd.classList.add("fade-in")



        if (result.length > 0) {

         
         
          result.forEach((item) => {
             let btn
                if (currentPath === '/party-catering/'){
                  btn = `<button onclick="goToPlan('${item.id}' ,'${item.name.replace(/\s+/g, '')}web' , false ,false , ${is_party_catering} , 'menu' , ${item.quantity})" class="explore-more mt-3" style="padding: 8px 7px; font-size: 10px;">
                          Add To Cart
                        </button>`
                }else{
                  btn = `<button onclick="decreaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web', false , false , ${is_party_catering} )" class="quantity-btn-show new-quantity-decrease-icon">
                            −
                          </button>
                          <input 
                              type="text" 
                              name="" 
                              value="${item.quantity}" 
                              readonly class="quantity-input-value2 ${item.name.replace(/\s+/g, '')}web" />
                          <button onclick="increaseQty('${item.id}','${item.name.replace(/\s+/g, '')}web', false , false , ${is_party_catering} )" class="quantity-btn-show new-quantity-decrease-icon">
                            +
                          </button>`
                }
            
            dishHtml = `
                <div class="col-md-3 mt-4 combo-fade-in">
                  <a onclick="menuPage('${item.category_name}','${item.subcategory_name}','${item.name}')" > <div class="new-home-page-card-container" style="background:url('${item.imageUrl}') center/cover no-repeat">
             <div class="ribbon">
              <span class="white">Pre</span><span>mium Options</span>
             </div>
               <div class="home-info-details">
               <div class="d-flex justify-content-between align-items-baseline">
               <div>
                 <h1>${item.name}</h1>
                 <p class="rating">${item.avg_reviews} <i class="bi bi-star-fill text-warning"></i> <span>(${item.total_reviews}
                    Reviews)</span></p>
               </div>
               <a onclick="ShowPop('${item.category_name}','${item.subcategory_name}','${item.name}')" ><div class="menushare-icon-show ">
                    <i class="fa-solid fa-share-nodes"></i>
                  </div></a>
               </div>
              <div class="d-flex justify-content-between align-items-center mt-2">
               <p class="card-price"> &#8377;${parseInt(item.discounted_price)} <span>&#8377;${parseInt(item.price)}</span></p>
              <div class="d-flex justify-content-between align-items-center rounded-3">
                      ${btn}
                    </div>
              </div>
               </div>
                </div>
                </a>
              </div>`;

              filerMenu = `  
              <div class="col-6 mt-4 combo-fade-in">
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
                      ${btn}
                    </div>
              </div>
               </div>
                </div>
                </a>
                    </div>`

              RowAdd.innerHTML += dishHtml;
              // const container1 = document.getElementById("menu-container1");
              if (container1) {
                container1.innerHTML += filerMenu;
              }
          });
      }

      const container = document.getElementById("menu-container");
      console.log("I am menu container :" ,container)
      container.innerHTML = '';
      const loader = document.getElementById("tabLoader");  
      
       if (  loader) {
         
        
        loader.style.display = "block";
        const containerFadeClass = "container-fade";
        container.classList.add(containerFadeClass); // Add base transition class
        container.classList.add("fade-out");
         
        setTimeout(function () {
          loader.style.display = "none";
          container.innerHTML = ''; 
          container.appendChild(divAdd); 
          
          void container.offsetWidth;

          // Switch from fade-out to fade-in
          container.classList.remove("fade-out");
          container.classList.add("fade-in");

          // Optionally remove fade-in class after it's done
          setTimeout(() => {
            container.classList.remove("fade-in");
          }, 400);



          const newTab = document.getElementById(menuItem);

          if (isAllRecipes) {
            newTab.style.display = "block";
            document.getElementById("defaultOpen").classList.add("active");
            void newTab.offsetWidth; // force reflow
            newTab.classList.add("show");
            
          } else {
            newTab.style.display = "block";
            document.getElementById(menuItem + SubcatId).classList.add("active");
            void newTab.offsetWidth;
            newTab.classList.add("show");
             
          }

        }, 500); // Show cards after 800ms (loader delay)
      }
      })
        
      .catch((error) => console.error(error));
  }

  





// Get the element with id="defaultOpen" and click on it
// console.log(document.getElementById("defaultOpen"))
// document.getElementById("defaultOpen").click();



  // -----------------------Read More Content--------------------------
//   document.addEventListener("DOMContentLoaded", function() {
//     document.getElementById("extraContent").style.display = "none";
// });

// document.getElementById("readMore").addEventListener("click", function() {
//     document.getElementById("extraContent").style.display = "block";
//     this.style.display = "none";
// });

// document.getElementById("readLess").addEventListener("click", function() {
//     document.getElementById("extraContent").style.display = "none";
//     document.getElementById("readMore").style.display = "inline";
// });


// -------------------------- Review Cart API -----------------------------------

function reviewCart(){

  console.log("I am ReviewCat called")
  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  if ( tokens){
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }else{
    return false
  }
  myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");

  const requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow"
  };

  fetch("http://127.0.0.1:8000/api/get-cart/", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      
      console.log(result)
      document.querySelectorAll('.change-name').forEach(function(el) {
        if (result.is_party_catering) {
          el.innerText = 'Party Cart';
        }
      });
      const reviewImages = document.querySelectorAll('.review-show-image')
      const mainCount = document.querySelector('.show-count')
      const boxCount = document.querySelector('.box-count')
      const noneBoxes = document.querySelectorAll('.box-none')


      // Clearing images that currently have  
      // console.log('reviewImages : ',reviewImages)
      if (reviewImages.length > 0){
        reviewImages.forEach(el => {
            el.innerHTML = ''
        })
      }


      // total quantity count variable
      let quant = 0

      if (result.data.length > 0){
        console.log("I am in if ")
        
        // removinh none-display to show view cart update
        noneBoxes.forEach(noneBox => {
          if (noneBox.classList.contains('none-display')) {
            noneBox.classList.remove('none-display');
          }
        });

        var count = 0
        result.data.forEach((item) =>{
          
          images = `
            <img
              id = "${item.id}"
              src="${item.menu_item_details.imageUrl}"
              alt="user"
            />
          `


          
          if (reviewImages.length > 0  && count < 3) {
            reviewImages.forEach(el => {
              el.innerHTML += images;    
            });
          }
          count += 1
          // reviewImages.innerHTML += images 
          // console.log(reviewImages)
          quant += parseInt(item.quantity)
          
         
        })

        
        
        const spanCont = document.getElementById("span-cont")
        const deskop_cart = document.querySelector('.desktop-cart-item-show')
        const mobile_cart = document.querySelector('.sticky-menubar-container')
        if (!(mobile_cart.classList.contains('main-menu-recommend-container'))){
          mobile_cart.classList.add('main-menu-recommend-container')
          
        }
        if (deskop_cart.classList.contains('none-display')){
          deskop_cart.classList.remove('none-display')
        }
        if (!spanCont.classList.contains('none-display')){
          spanCont.classList.add('none-display')
        }

        // console.log(deskop_cart,mobile_cart)

      }
      else{
        const spanCont = document.getElementById("span-cont")
        const deskop_cart = document.querySelector('.desktop-cart-item-show')
        const mobile_cart = document.querySelector('.sticky-menubar-container')
        if (!(deskop_cart.classList.contains('none-display'))){
          deskop_cart.classList.add('none-display')
        }
        if (mobile_cart.classList.contains('main-menu-recommend-container')){
          mobile_cart.classList.remove('main-menu-recommend-container')
        }

        noneBoxes.forEach(noneBox => {
          if (!(noneBox.classList.contains('none-display'))) {
            noneBox.classList.add('none-display');
          }
        });
        if (spanCont.classList.contains('none-display')){
          spanCont.classList.remove('none-display')
        }

      }


      mainCount.innerHTML = `${quant} items`
      boxCount.innerHTML = `${quant} Items`

    })
    .catch((error) => console.error(error));



}


if (runApi){
 
reviewCart();
}





// ---------------------------Quantity-------------------------------------


function increaseQty(menuId, id_name, shouldReload = false , is_view_cart = false , is_party_catering = false ,  item_type = 'menu' ) {
   
  const qtyInput = document.querySelectorAll(`.${id_name}`);
  // console.log(qtyInput)
  // let current = parseInt(qtyInput.value);
  // qtyInput.value = current + 1;

  //---------------------------------Add Acess Token 

  // const oneYear = 60 * 60 * 24 * 365;
  // var token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4OTIzMTkyLCJpYXQiOjE3NDczODcxOTIsImp0aSI6IjdiMTUzMWM0YjgyNDQxNDNhNjU0N2Y0ZDA0YzdiNDI2IiwidXNlcl9pZCI6Mn0.TvZ1X0WvjhiZGNUeiNfM0Ard-V3dz_8rFHl5hiD-HYY'
  // document.cookie = `access_token=${token}; path=/; max-age=${oneYear}; secure; samesite=Lax`;
  
  
  // ------------------------------- clear acess token
  // document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; secure; samesite=Lax";

  // --------------------------------Fetching acess token
  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;
  const myHeaders = new Headers();
  // console.log(tokens)

  console.log(currentPath)


  if ( !tokens){
    // console.log(cookieMatch,menuId,id_name)
    window.location.href = '/api/login-page/';
    return false
  } 
  else{
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }

  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");


  // console.log(parseInt(qtyInput[0].value))
  if ((currentPath === '/' || currentPath.startsWith('/api/menu-detils/')) && !is_view_cart){
    is_party_catering = false
    console.log(is_party_catering)
  }else if (currentPath === '/party-catering/' && !is_view_cart){
    is_party_catering = true
    console.log(is_party_catering)
  }

  // menu items
  let type =  item_type === "combo" ? "combo" : "menu";


  const raw = JSON.stringify({
    "item_id": menuId,
    "item_type": type,
    "quantity": parseInt(qtyInput[0].value) +1,
    "is_party_catering": is_party_catering
  });


  
  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
  };

  fetch("http://127.0.0.1:8000/api/add-cart/", requestOptions)
    .then((response) => response.json())
    .then((result) => {

      console.log(result)
      if (result.success === true){
        qtyInput.forEach(input => 
          {
            let current = parseInt(input.value) || 0;
            input.value = current + 1;
          });
          if (shouldReload) {
            location.reload(); // Only reload if requested
          }
          reviewCart();
        }
      else {
        showPopup('warning', `${result.message}`)
      }
      
      // console.log(result)
    })
    .catch((error) => console.error(error));
 
}

function decreaseQty(menuId,id_name, shouldReload = false , is_view_cart = false , is_party_catering = false ,  item_type = 'menu') {
  const qtyInput = document.querySelectorAll(`.${id_name}`);
  console.log("i am from decreaseQty")
  // -------------------------------- Fetching acess token
  const cookieMatch = document.cookie.match('(^|;)\\s*access_token\\s*=\\s*([^;]+)');
  const tokens = cookieMatch ? cookieMatch[2] : null;

  // ------------------------------- Token adding to Header
  const myHeaders = new Headers();
  if ( !tokens){
    window.location.href = '/api/login-page/';
    return false
  } 
  else{
    myHeaders.append("Authorization", `Bearer ${tokens}`);
  }

  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Cookie", "csrftoken=F7QxpvkG0tOKT8D2CnzRFW2ZRZyIRle1");

  // =========== checking current url =====================

  if ((currentPath === '/' || currentPath.startsWith('/api/menu-detils/')) && !is_view_cart){
    is_party_catering = false
  }else if (currentPath === '/party-catering/' && !is_view_cart){
    is_party_catering = true
  }

  // menu items
  let type =  item_type === "combo" ? "combo" : "menu";

  // --------------------------------- Quantity Logic to decrease
  if (parseInt(qtyInput[0].value) > 0 &&  is_party_catering && !is_view_cart) {
      quant =  parseInt(qtyInput[0].value);
  }else if(parseInt(qtyInput[0].value) > 0){
      quant =  parseInt(qtyInput[0].value) - 1;
  }else{
      quant =  parseInt(qtyInput[0].value);
  }
  const raw = JSON.stringify({
    "item_id": menuId,
    "item_type": type,
    "quantity": quant,
    "is_party_catering": is_party_catering
  });
  console.log(raw)
  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow"
  };

  fetch("http://127.0.0.1:8000/api/add-cart/", requestOptions)
    .then((response) => response.json())
    .then((result) => {

      console.log(result)

      if (result.success === true){
          qtyInput.forEach(input => {
            let current = parseInt(input.value);
            if (current > 0 &&  !is_party_catering ) {
              input.value = current - 1;
            }else{
              input.value = current ;
            }
          });
          if (shouldReload) {
            location.reload(); // Only reload if requested
          }
          reviewCart();
        }
      else {
        showPopup('warning', `${result.message}`)
      }
      
      // console.log(result)
    })
    .catch((error) => console.error(error));

}



function showPopup(type, message) {
  const container = document.getElementById('popupContainer');
  const popup = document.createElement('div');
  popup.className = `main-popup ${type}` ;
  // popup.role = 'alert';
  popup.innerHTML = `
      <div class="me-2">${
      type === 'success' ? '✅' :
      type === 'warning' ? '⚠️' :
      '❌'
    }</div>
      <div class="message">${message}</div>
     <button class="close-btn ms-auto" onclick="this.parentElement.remove()"><i class="bi bi-x-circle"></i></button>
  `;
  
  container.appendChild(popup);
  setTimeout(() => popup.remove(), 3500);
}


function toggleSubmenu(clickedElement) {
    event.preventDefault();
    event.stopPropagation();

    const submenuParent = clickedElement.closest('.dropdown-submenu');
    if (!submenuParent) return;

    const submenu = submenuParent.querySelector('.submenu');
    if (!submenu) return;

    // Find the icon inside the clicked div
    const icon = clickedElement.querySelector('.plus-icons');

    // Close other open submenus
    document.querySelectorAll('.dropdown-submenu.show').forEach(el => {
      if (el !== submenuParent) {
        el.classList.remove('show');
        const otherSubmenu = el.querySelector('.submenu');
        if (otherSubmenu) {
          otherSubmenu.style.maxHeight = null;
        }
        const otherIcon = el.querySelector('.plus-icons');
        if (otherIcon) {
          otherIcon.classList.remove('bi-dash-circle-fill', 'minus');
          otherIcon.classList.add('bi-plus-circle-fill');
        }
      }
    });

    const isOpen = submenuParent.classList.toggle('show');

    if (isOpen) {
      submenu.style.maxHeight = submenu.scrollHeight + "px";
      if (icon) {
        icon.classList.remove('bi-plus-circle-fill');
        icon.classList.add('bi-dash-circle-fill', 'minus');
      }
    } else {
      submenu.style.maxHeight = null;
      if (icon) {
        icon.classList.remove('bi-dash-circle-fill', 'minus');
        icon.classList.add('bi-plus-circle-fill');
      }
    }
  }

// ==================================Combo Category Slider==================================================

function scrollCombo(direction) {
  const container = document.getElementById('comboSlider');
  const scrollAmount = 200; // Adjust based on card width
  if (direction === 'left') {
    container.scrollLeft -= scrollAmount;
  } else {
    container.scrollLeft += scrollAmount;
  }
}