// import axios from 'axios';

$('.saved').click(function() {
    let storeId = $('#select-store').val()
    axios.post('/accounts/setting', {
        display_store_id: storeId,
    })
    .then(function (response) {
        alert(response.hello)
        console.log(response);
    })
    .catch(function (error) {
        console.log(error);
    });
})