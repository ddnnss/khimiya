

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
        return parts.join(".").replace(/0+$/, "");
}