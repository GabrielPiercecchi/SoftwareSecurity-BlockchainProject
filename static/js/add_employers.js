document.addEventListener('DOMContentLoaded', function() {
    const addEmployerButton = document.getElementById('add-employer');
    const employersContainer = document.getElementById('employers-container');
    let employerCount = 1;

    addEmployerButton.addEventListener('click', function() {
        employerCount++;
        const employerDiv = document.createElement('div');
        employerDiv.classList.add('employer');
        employerDiv.innerHTML = `
            <div class="form-group">
                <label for="emp_username_${employerCount}">Username:</label>
                <input type="text" id="emp_username_${employerCount}" name="emp_username" required>
            </div>
            <div class="form-group">
                <label for="emp_password_${employerCount}">Password:</label>
                <input type="password" id="emp_password_${employerCount}" name="emp_password" required>
            </div>
            <div class="form-group">
                <label for="emp_name_${employerCount}">Name:</label>
                <input type="text" id="emp_name_${employerCount}" name="emp_name" required>
            </div>
            <div class="form-group">
                <label for="emp_surname_${employerCount}">Surname:</label>
                <input type="text" id="emp_surname_${employerCount}" name="emp_surname" required>
            </div>
            <div class="form-group">
                <label for="emp_email_${employerCount}">Email:</label>
                <input type="email" id="emp_email_${employerCount}" name="emp_email" required>
            </div>
        `;
        employersContainer.appendChild(employerDiv);
    });
});