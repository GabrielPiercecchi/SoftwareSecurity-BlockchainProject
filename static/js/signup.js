document.addEventListener('DOMContentLoaded', function() {
    const addEmployerButton = document.getElementById('add-employer');
    const employersContainer = document.getElementById('employers-container');
    const addEmployerWithOrganizationButton = document.getElementById('add-employers-button');
    let employerCount = 1; // Inizia da 1 per evitare conflitti con il primo impiegato

    addEmployerWithOrganizationButton.addEventListener('click', function() {
        window.location.href = "/add_employers";
    });

    addEmployerButton.addEventListener('click', function() {
        employerCount++;
        const employerDiv = document.createElement('div');
        employerDiv.classList.add('employer');

        const fields = [
            { label: 'Username', type: 'text', name: 'emp_username', placeholder: 'Username' },
            { label: 'Password', type: 'password', name: 'emp_password', placeholder: 'Password' },
            { label: 'Confirm Password', type: 'password', name: 'emp_confirm_password', placeholder: 'Confirm Password' },
            { label: 'Name', type: 'text', name: 'emp_name', placeholder: 'Name' },
            { label: 'Surname', type: 'text', name: 'emp_surname', placeholder: 'Surname' },
            { label: 'Email', type: 'email', name: 'emp_email', placeholder: 'Employer@Email' }
        ];

        fields.forEach(field => {
            const formGroup = document.createElement('div');
            formGroup.classList.add('form-group');

            const label = document.createElement('label');
            label.setAttribute('for', `${field.name}_${employerCount}`);
            label.textContent = field.label;

            const input = document.createElement('input');
            input.setAttribute('type', field.type);
            input.setAttribute('id', `${field.name}_${employerCount}`);
            input.setAttribute('name', field.name);
            input.setAttribute('placeholder', field.placeholder);
            input.required = true;

            formGroup.appendChild(label);
            formGroup.appendChild(input);
            employerDiv.appendChild(formGroup);
        });

        employersContainer.appendChild(employerDiv);
    });
});