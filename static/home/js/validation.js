
// sign up
var value = $("#password_reg").val();
$.validator.addMethod("checklower", function (value) {
    return /[a-z]/.test(value);
});
$.validator.addMethod("checkupper", function (value) {
    return /[A-Z]/.test(value);
});
$.validator.addMethod("checkdigit", function (value) {
    return /[0-9]/.test(value);
});
$.validator.addMethod("pwcheck", function (value) {
    return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) && /[a-z]/.test(value) && /\d/.test(value) && /[A-Z]/.test(value);
});
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
            minlength: 6,
            maxlength: 30,
            required: true,
            //pwcheck: true,
            checklower: true,
            checkupper: true,
            checkdigit: true

        },
        confirm_password: {

            equalTo: "#password_reg",
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
            pwcheck: "Password is not strong enough",
            checklower: "Need atleast 1 lowercase alphabet",
            checkupper: "Need atleast 1 uppercase alphabet",
            checkdigit: "Need atleast 1 digit"
        },
        confirm_password: {
            equalTo: "Password must be same"
        }
    },
    submitHandler: function (form) {
        console.log('test');
        form.submit();
    
    }
})

// change password



var change_value = $("#change_password").val();
$.validator.addMethod("checklower", function (change_value) {
    return /[a-z]/.test(change_value);
});
$.validator.addMethod("checkupper", function (change_value) {
    return /[A-Z]/.test(change_value);
});
$.validator.addMethod("checkdigit", function (change_value) {
    return /[0-9]/.test(change_value);
});
$.validator.addMethod("pwcheck", function (change_value) {
    return /^[A-Za-z0-9\d=!\-@._*]*$/.test(change_value) && /[a-z]/.test(change_value) && /\d/.test(change_value) && /[A-Z]/.test(change_value);
});

$('#form_change_password').validate({
    errorClass: 'errors',
    rules: {
        new_password: {
            minlength: 6,
            maxlength: 30,
            required: true,
            //pwcheck: true,
            checklower: true,
            checkupper: true,
            checkdigit: true

        },
        reconfirm_password: {

            equalTo: "#change_password",
        }
    },
    messages: {
        password: {
            pwcheck: "Password is not strong enough",
            checklower: "Need atleast 1 lowercase alphabet",
            checkupper: "Need atleast 1 uppercase alphabet",
            checkdigit: "Need atleast 1 digit"
        },
        confirm_password: {
            equalTo: "Password must be same"
        }
    },
    submitHandler: function (form) {
        console.log('test');
        form.submit();
    
    }
})
