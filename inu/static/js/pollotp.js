function doPoll(){
    $.get('auth_status/'+sessionStorage.getItem("userid"), function(data) {
        console.log(data)
        if(data['state'] == 2){
            window.open('confirm_transaction/'+sessionStorage.getItem("userid"))
        }
        setTimeout(doPoll,5000);
    });
}

// ({'state': data['state'], 'user_id': user_id})

doPoll()