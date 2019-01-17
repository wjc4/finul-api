function doPoll(){
    $.get('auth_status/'+sessionStorage.getItem("userid"), function(data) {
        console.log(data)
        if(data['state'] == 2){
            console.log("otp confirmed");
            window.open('confirm_transaction/'+sessionStorage.getItem("userid"),"_self");
        } else if(data['state'] == 0){
            console.log("tx rejected");
            alert('Transaction is rejected.');
            window.open('transaction',"_self");
        }
        setTimeout(doPoll,2000);
    });
}

// ({'state': data['state'], 'user_id': user_id})

doPoll()