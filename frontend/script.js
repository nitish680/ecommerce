

const category=document.getElementById("categories");
const container=document.getElementById("product-container")
const searchbar=document.getElementById("searchbar");
console.log("script.js loaded");
const products=[];
let cart = JSON.parse(localStorage.getItem("cart")) || [];



function display_products(productsToDisplay){
    for(const product of productsToDisplay){
        const card=document.createElement("div");
        card.className="product-card";
        card.innerHTML=`
        <img src="${product.image}">
        <h2 class="product-name">${product.name}</h2>
        <p>${product.rating}</p>
        <p>${product.price}</p>
        <button>AddCart</button>
        
        `;
        const button=card.querySelector("button");
        const productName = card.querySelector(".product-name");
        
        productName.addEventListener("click", function() {
            console.log(product.id);
            window.location.href = `products.html?id=${product.id}`;
        });
        button.addEventListener("click",function(){
            console.log("BUTTON CLICKED:", product.name);
            cart = JSON.parse(localStorage.getItem("cart")) || [];
            const existingitem =cart.find(function(item){
                return item.product.id === product.id;
            });
            if(existingitem){
                existingitem.quantity++;
                
            }
            else{
                const quantity=1;
                cart.push({product,quantity});
            }
            // cart.push(product);
            
            console.log(cart);
            localStorage.setItem("cart",JSON.stringify(cart));

            // window.location.href=`cart.html`;
        });
        container.appendChild(card);
        
}


}




function filter_product() {
    
    const searchtext = searchbar.value;
    const categories = category.value;
    
    const matchingProducts = products.filter(function(product) {
        
        return product.name.toLowerCase().includes(searchtext.toLowerCase())
        && (categories === "all" || product.category === categories);

    });

    return matchingProducts;
}
searchbar.addEventListener("input",function(){
    const searchtext=searchbar.value;
    const matchingproduct= filter_product();
    container.innerHTML="";
    display_products(matchingproduct);
});
category.addEventListener("change" ,function(){
    const selected=category.value;
    const matchingproduct=filter_product();
    container.innerHTML="";
    display_products(matchingproduct);
    
    
});
const url = `${API_BASE_URL}/products`;

async function get() {
    let response = await fetch(url);
    let answer = await response.json();
    products.push(...answer);
    display_products(products);
}
get();