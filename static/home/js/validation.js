

$('#signup').validate({
    errorClass: 'errors',
    rules: {
        username: {
            required: true,


        },
        phone: {
            required: true,
            matches: "[0-9]+",

        },
        email: {
            required: true,
            email: true,
        },

        password: {
            checklower: true,
            checkupper: true,
            checkdigit: true,
            required: true,
            minlength: 8,
            maxlength: 30,
            
        },
        confirm_password: {
            
            equalTo: "#passwd_reg",
        }
    },
    messages: {
        username: {
            required: "Please enter username",

        },
        email: {
            required: "Please enter email address",
            email: "Enter a valid email"

        },
        phone: {
            required: "Please enter phone number",


        },
        password: {
            required: "Please enter password",
        },
        confirm_password:{
            equalTo:"Password must be same"
        }
    },
    SubmitHandler: function (form) {
        form.submit();
    }
})