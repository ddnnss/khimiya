 let cart = document.getElementById("shopping-bag");
    let cart_menu = document.getElementById("shopping_bag_menu");
    function showcart() {
        cart_menu.style.display = 'block'
        cart_menu.classList.add('slide-top')

    }
    function hidecart() {
        cart_menu.style.display = 'none'

    }



    cart.addEventListener("mouseenter", showcart, false);
    cart_menu.addEventListener("mouseleave", hidecart, false)
    cart.addEventListener("mouseleave", function (event) {
        if (event.relatedTarget.classList != 'nav-search-cart'){
                cart_menu.style.display = 'none'

            }
    });

     function plusItem(el){
        let event = new Event('change');
        let id= 'item_total'

        let oldValue = document.getElementById(id).value


        let newVal = parseFloat(oldValue) + 1;

        document.getElementById(id).value = newVal
        document.getElementById(id).dispatchEvent(event);
    }

    function minusItem(el){
        let event = new Event('change');

        let id= 'item_total'
        let oldValue = document.getElementById(id).value

        if (parseFloat(oldValue) > 2){
            var newVal = parseFloat(oldValue) - 1;

        }else {
            var newVal = 1
        }
        document.getElementById(id).value = newVal
        document.getElementById(id).dispatchEvent(event);
    }



    function numberWithCommas(x) {
        var parts = x.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        return parts.join(".");
}