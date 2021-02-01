// import axios from 'axios';

$('.saved').click(function() {
    let storeId = $('#select-store').val()
    axios.post('/accounts/setting', {
        display_store_id: storeId,
    })
    .then(function (response) {
        alert(response.status);
        location.reload();
    })
    .catch(function (error) {
        console.log(error);
    });
})