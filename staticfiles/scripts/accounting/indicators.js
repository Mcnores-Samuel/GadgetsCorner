$(document).ready(function() {
    const sales_growth = $('#sales_growth');

    const formatValue = (value) => {
        return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    function salesGrowth() {
        $.ajax({
            url: '/gadgetsCorner/revenue_growth/',
            method: 'GET',
            contedType: 'application/json',
            success(data) {
                if (data.growth > 0) {
                    sales_growth.html(`<span class="text-success">${data.growth}%</span>`);
                } else {
                    sales_growth.html(`<span class="text-danger">${data.growth}%</span>`);
                }
            }

        });
    }

    function avgOrderValue() {
        $.ajax({
            url: '/gadgetsCorner/average_order_value/',
            method: 'GET',
            contedType: 'application/json',
            success(data) {
                $('#avg_order_value').html(`MK${formatValue(data.average_order_value)}`);
            }
        });
    }

    avgOrderValue();
    salesGrowth();
});