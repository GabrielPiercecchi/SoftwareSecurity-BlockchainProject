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
        employerDiv.innerHTML = `
            <div class="form-group">
                <label for="emp_username_${employerCount}">Username:</label>
                <input type="text" id="emp_username_${employerCount}" name="emp_username" placeholder="Username" required>
            </div>
            <div class="form-group">
                <label for="emp_password_${employerCount}">Password:</label>
                <input type="password" id="emp_password_${employerCount}" name="emp_password" placeholder="Password" required>
            </div>
            <div class="form-group">
                <label for="emp_confirm_password_${employerCount}">Confirm Password:</label>
                <input type="password" id="emp_confirm_password_${employerCount}" name="emp_confirm_password" placeholder="Confirm Password" required>
            </div>
            <div class="form-group">
                <label for="emp_name_${employerCount}">Name:</label>
                <input type="text" id="emp_name_${employerCount}" name="emp_name" placeholder="Name" required>
            </div>
            <div class="form-group">
                <label for="emp_surname_${employerCount}">Surname:</label>
                <input type="text" id="emp_surname_${employerCount}" name="emp_surname" placeholder="Surname" required>
            </div>
            <div class="form-group">
                <label for="emp_email_${employerCount}">Email:</label>
                <input type="email" id="emp_email_${employerCount}" name="emp_email" placeholder="Employer@Email" required>
            </div>
        `;
        employersContainer.appendChild(employerDiv);
    });
});