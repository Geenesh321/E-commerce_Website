const updateBtn = document.querySelector('.update-btn');
const submitBtn = document.getElementById('submit-btn');

updateBtn.addEventListener('click', function () {
    submitBtn.removeAttribute('disabled');
});

const form = document.getElementById('basic_details');

form.addEventListener('submit', function (event) {
    event.preventDefault();

    if (form.checkValidity() && validatePhoneNumber() && validateName()) {
        alert('Your Details Update successfully. "Click on Place Order" ');
    } else {
        // Check for specific validation errors
        if (!form.checkValidity()) {
            alert('Please fill in all the required fields.');
        } else if (!validatePhoneNumber()) {
            alert('Please enter a 10-digit phone number.');
        } else if (!validateName()) {
            alert('Name cannot contain special symbols or numbers.');
        }
    }
});

const formFields = form.querySelectorAll('input, textarea');
formFields.forEach(function (field) {
    field.addEventListener('input', function () {
        if (!field.checkValidity()) {
            field.classList.add('invalid');
        } else {
            field.classList.remove('invalid');
        }
    });
});

function validatePhoneNumber() {
    const phoneInput = document.getElementById('phone');
    const phoneNumber = phoneInput.value.trim();
    const phoneRegex = /^\d{10}$/;

    if (!phoneRegex.test(phoneNumber)) {
        phoneInput.classList.add('invalid');
        return false;
    } else {
        phoneInput.classList.remove('invalid');
        return true;
    }
}

function validateName() {
    const firstNameInput = document.getElementById('first_name');
    const lastNameInput = document.getElementById('last_name');
    const firstName = firstNameInput.value.trim();
    const lastName = lastNameInput.value.trim();
    const nameRegex = /^[A-Za-z\s]+$/;

    if (!nameRegex.test(firstName) || !nameRegex.test(lastName)) {
        firstNameInput.classList.add('invalid');
        lastNameInput.classList.add('invalid');
        return false;
    } else {
        firstNameInput.classList.remove('invalid');
        lastNameInput.classList.remove('invalid');
        return true;
    }
}