
// Reward

$("#reward").validate({
    errorClass: 'errors',
    rules: {
        reffer: {
            required: true,
            number: true,
        },
        youtubereffer: {
            required: true,
            number: true,
        }


    },
    messages: {
        reffer: {
            required: "Please enter the trx amount for refferance",

        },
        youtubereffer: {
            required: "Please enter the trx amount for youtube",

        },

    },



    submitHandler: function (form) {
        form.submit();
    }

});





// Announcement




$("#main_announcement").validate({
    errorClass: 'errors',
    rules: {
        announcement: {
            required: true,
        },

    },
    messages: {
        announcement: {
            required: "Please add announcement",
        },
    },
    submitHandler: function (form) {
        form.submit();
    }

});





// Earnings


$("#Earnings").validate({
    errorClass: 'errors',
    rules: {
        Earnings: {
            required: true,
        },

    },
    messages: {
        Earnings: {
            required: "Please add Earnings",
        },
    },
    submitHandler: function (form) {
        form.submit();
    }

});