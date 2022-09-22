
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
