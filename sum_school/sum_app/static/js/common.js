const backBtn = document.querySelector('#back-button');


$(function () {
    setTimeout(function () {
        $('.alert-msg').fadeOut('slow');
    }, 3000);
    $('[data-bs-toggle="tooltip"]').tooltip();

    $(".clickable-row").click(function () {
        const href = $(this).data("href");
        if (href) {
            window.location = href;
        }
    });

    $('.assignment-form-item-1').removeClass('d-none');
    var dataId = $('.assignment-form-item-1').data('id') + 1;

    $('#add-btn').on('click', function (e) {
        e.preventDefault();
        $('.assignment-form-item-' + dataId).removeClass('d-none');
        dataId++;

        if (dataId > 2) {
            $('#remove-btn').removeClass('d-none');
        }
        if (dataId > 5) {
            $('#add-btn').addClass('d-none');
        }
    });

    $('#remove-btn').on('click', function (e) {
        e.preventDefault();
        dataId--;
        $('.assignment-form-item-' + dataId).addClass('d-none');
        $('#file_' + dataId).val('');

        if (dataId <= 2) {
            $('#remove-btn').addClass('d-none');
        }
        if (dataId < 6) {
            $('#add-btn').removeClass('d-none');
        }
    });

    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    const allowedExtensions = [
        ".jpg", ".jpeg", ".png", ".gif", ".pdf",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt",
        ".html", ".css", ".js", ".ts", ".json", ".xml", ".py",
        ".php", ".java", ".cpp", ".c", ".cs", ".rb", ".go", ".sh",
        ".sql", ".swift"
    ];

    for (let i = 1; i <= 5; i++) {
        $('#file_' + i).on('change', function () {
            const input = $(this);
            const file = this.files[0];
            const errorDiv = input.siblings('.invalid-feedback');

            // Reset error state
            input.removeClass('is-invalid');
            errorDiv.text('');

            if (file) {
                const ext = '.' + file.name.split('.').pop().toLowerCase();

                if (file.size > MAX_FILE_SIZE) {
                    errorDiv.text(`File must not be greater than 10MB.`);
                    input.addClass('is-invalid');
                    input.val('');
                } else if (!allowedExtensions.includes(ext)) {
                    errorDiv.text(`Invalid file type (${ext}).`);
                    input.addClass('is-invalid');
                    input.val('');
                }
            }
        });
    }

    $('.submit--form').on('submit', function (e) {
        let atLeastOneSelected = false;
        var messageField = $('.file-required');
    
        for (let i = 1; i <= 5; i++) {
            const fileInput = $('#file_' + i);
            const file = fileInput[0].files[0];
    
            if (file) {
                atLeastOneSelected = true;
                break;
            }
        }
    
        if (!atLeastOneSelected) {
            e.preventDefault();
            messageField.text(`File must not be greater than 10MB.`).css('display', 'block');
        }
    });

    $('#scoreModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var studentId = button.data('student-id');
        var taskId = button.data('task-id');
  
        $('#modal-student-id').val(studentId);
        $('#modal-task-id').val(taskId);
      });
});

if (backBtn) {
    backBtn.addEventListener('click', function (e) {
        window.history.back();
    })
}