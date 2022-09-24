
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
            number : true,
            

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

$("#withdraw_form").validate({
    errorClass: 'errors',
    rules: {
        withdraw_amount: {
            required: true,
            number : true,
        },
        trx_address: {
            required: true,
            
            

        },
    },
    messages: {
        withdraw_amount: {
            required: "Please enter the amount",

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
            url : true
        },
        
    },

    submitHandler: function (form) {
        form.submit();
    }

    });
