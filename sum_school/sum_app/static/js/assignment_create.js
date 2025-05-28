$(document).ready(function () {
    $("#assignment-create-form").on("submit", function (e) {
        $(".text-danger").remove(); // Clear previous errors
        let hasError = false;

        const title = $("#title").val().trim();
        const endDate = new Date($("#end_date").val());
        const type = $("#type").val();
        const moduleId = $("#module_id").val();
        const maxScore = parseInt($("#max_score").val());
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Compare only date

        const allowedTypes = [
            // Document and image MIME types
            "image/png", "image/jpeg", "image/jpg", "image/gif",
            "application/pdf", "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "text/plain", "text/html", "text/css", "application/javascript", "application/json",
            "application/xml", "text/x-python", "text/x-php", "text/x-java-source", "text/x-c", "text/x-c++", "text/x-shellscript"
        ];
        
        const allowedExtensions = [
            ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt",
            ".html", ".css", ".js", ".ts", ".json", ".xml", ".py", ".php", ".java",
            ".cpp", ".c", ".cs", ".rb", ".go", ".sh", ".sql", ".swift"
        ];
        
        function hasAllowedExtension(filename) {
            return allowedExtensions.some(ext => filename.toLowerCase().endsWith(ext));
        }

        const showError = (selector, message) => {
            $(`<small class="text-danger">${message}</small>`).insertAfter($(selector));
            hasError = true;
        };

        // Title
        if (!title) {
            showError("#title", "Title is required.");
        } else if (title.length > 100) {
            showError("#title", "Title must be 100 characters or fewer.");
        } else if (!/^[a-zA-Z0-9\s\-_,.()]+$/.test(title)) {
            showError("#title", "Title must not contain special characters.");
        }

        // End date
        if (!$("#end_date").val()) {
            showError("#end_date", "Due date is required.");
        } else if (endDate <= today) {
            showError("#end_date", "Due date must be after today.");
        }

        // Type
        if (!["1", "2"].includes(type)) {
            showError("#type", "Invalid type selected.");
        }

        // Module
        if (!$("#module_id option[value='" + moduleId + "']").length) {
            showError("#module_id", "Invalid module selected.");
        }

        // Max Score
        if (!$("#max_score").val()) {
            showError("#max_score", "Max score is required.");
        } else if (isNaN(maxScore) || maxScore < 1 || maxScore > 100) {
            showError("#max_score", "Max score must be between 1 and 100.");
        }

        // File
        const fileInput = $(`#file`)[0];
        if (fileInput && fileInput.files.length > 0) {
            const file = fileInput.files[0];
            if (file.size > 10 * 1024 * 1024) {
                showError(`#file`, `File must be less than 10MB.`);
            }
            if (!allowedTypes.includes(file.type) && !hasAllowedExtension(file.name)) {
                showError(`#file`, `File type is not supported.`);
            }
        }

        // Stop submission on error
        if (hasError) {
            e.preventDefault();
        }
    });
});
