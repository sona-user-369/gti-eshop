



    function filterItems(items, price) {

        return items.filter(item => {

            return item.product_data.prix >= price[0].replace('$', '') && item.product_data.prix <= price[1].replace('$', '')
        })

    }





