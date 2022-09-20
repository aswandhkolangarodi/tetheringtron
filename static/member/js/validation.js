
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

            idproof_document: {
                fileType: {
                    types: ["jpeg", "jpg"]
                },

            },
            member_image: {
                fileType: {
                    types: ["jpeg", "jpg"]
                },

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
            idproof_document: {
                required: "Please upload idproof as image",

            },
            member_image: {
                required: "Please upload your image as passport size",

            },

        },

        submitHandler: function (form) {
            form.submit();
        }

        });
