function doPoll(){
    $.get('auth_status/'+sessionStorage.getItem("userid"), function(data) {
        console.log(data)
        if(data['state'] == 2){
            console.log("otp confirmed")
            window.open('confirm_transaction/'+sessionStorage.getItem("userid"),"_self");
        }
        setTimeout(doPoll,2000);
    });
}

// ({'state': data['state'], 'user_id': user_id})

doPoll()