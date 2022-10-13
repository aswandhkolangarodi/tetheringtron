
// kyc

$("#kyc").validate({
    errorClass: 'errors',
    rules: {
        country: {
            required: true,
        },
        city: {
            required: true,


        },
        idproof_name: {
            required: true,

        },
        address: {
            required: true,
        },
        pin: {
            required: true,
        },


    },
    messages: {
        country: {
            required: "Please select your country",

        },
        city: {
            required: "Please enter your city",

        },
        idproof_name: {
            required: "Please enter your pin",

        },
        address: {
            required: "Please enter your address",

        },
        pin: {
            required: "Please enter your pin",

        },


    },

    submitHandler: function (form) {
        form.submit();
    }

});


// deposit 

$("#deposit_form").validate({
    errorClass: 'errors',
    rules: {
        currency: {
            required: true,
        },
        amount: {
            required: true,
            number: true,


        },
    },
    messages: {
        currency: {
            required: "Please select your currency",

        },
        amount: {
            required: "Please enter the amount",

        },

    },

    submitHandler: function (form) {
        form.submit();
    }

});





// withdraw validation

$.validator.addMethod("notOnlyZero", function (value, element, param) {
    return this.optional(element) || parseInt(value) > 0;
});

$("#withdraw_form").validate({
    
    errorClass: 'errors',
    rules: {
        withdraw_amount: {
            required: true,
            notOnlyZero: '0',
            min: 100
        },
        trx_address: {
            required: true,



        },
    },
    messages: {
        withdraw_amount: {
            required: "Please enter the amount",
            notOnlyZero : "Enter a valid number",
            min:"Minimum withdroaw amount is 100"
        },
        trx_address: {
            required: "Please enter your trx-address",

        },

    },

    submitHandler: function (form) {
        form.submit();
    }

});


// youtube refferance 

$("#youtube_reffer").validate({
    errorClass: 'errors',
    rules: {
        youtube: {
            required: true,
            url: true
        },

    },

    submitHandler: function (form) {
        form.submit();
    }

});


$("#bank_details").validate({
    errorClass: 'errors',
    rules: {
        bank_name: {
            required: true,
        },
        branch :{
            required :true
        },
        ifsc_code :{
            
        },
        account_number :{
            required : true,
            number : true
        },
        swift_code :{
            required : true,
        }

    },
    messages :{
        bank_name :{
            required :"Please enter your bank name"
        },
        branch :{
            required :"Please enter your bank branch"
        },
        ifsc_code :{
           
        },
        account_number :{
            required : "Plese enter your account number",
            
        },
        swift_code :{
            required : "Please enter swift code",
        }
    },
    submitHandler: function (form) {
        form.submit();
    }

});

