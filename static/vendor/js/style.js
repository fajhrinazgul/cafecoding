// $(document).ready(function () {

//     // swal("Hello World");

//     $(window).on("scroll", function () {
//         if ($(window).scrollTop() > 500) {
//             $(".navbar").removeClass("navbar-dark bg-dark");
//             $(".navbar").addClass("navbar-light bg-light");
//         }
//         else {
//             $(".navbar").removeClass("navbar-light bg-light");
//             $(".navbar").addClass("navbar-dark bg-dark");
//         }
//     })
// })

// function loginView() {
//     Swal.fire({
//         title: "Login Form",
//         html: `<input type="text" id="username" name="username" class="form-control" placeholder="Username" /> <input type="password" name="password" placeholder="Password" class="form-control" />`,
//         confirmButtonText: "Sign In",
//         focusConfirm: false,

//     })
// }

async function loginView() {
    const { value: email } = await Swal.fire({
        title: "Nama Pengguna",
        input: "text",
        inputLabel: "Nama pengguna",
        inputPlaceholder: "Masukkan nama pengguna anda",
    })

    const { value: password } = await Swal.fire({
        title: "Kata Sandi",
        input: "password",
        inputLabel: "Password",
        inputPlaceholder: "Masukkan password anda",
    })

    if (email && password) {
        await Swal.fire(`Entered Email: ${email}`);
        await Swal.fire(`Entered Password: ${password}`);
    }
}

$(document).ready(function() {
    // $.validator.setDefaults( {
    //     submitHandler: function() {
    //         alert( "Submitted" );
    //     }
    // })

    $("#registerForm").validate({
        rules: {
            first_name: "required",
            last_name: "required",
            username: {
                required: true,
                minlength: 8,
                // remote: {
                //     url: "http:/localhost:8000/account/check-username/",
                //     type: "post",
                //     dataType: "json",
                //     data: {
                //         username: function () {
                //             return $("#id_username").val();
                //         }
                //     }
                // }
            },
            email: {
                email: true,
                required: true
            },
            password1: {
                required: true,
                minlength: 8
            },
            password2: {
                required: true,
                equalTo: "#id_password1"
            }
        },
        errorElement: "div",
        errorPlacement: function ( error, element ) {
            error.addClass("invalid-feedback");
            element.parents(".col-sm-6").addClass("was-validated");
            error.insertAfter( element );
        }
    })
})