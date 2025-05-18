$(document).ready(function () {
    const isStudent = $('.user-table').data('is-student') === 'true';

    const columnDefs = [
        { "orderable": false, "targets": 0 }, // No. column
        { "orderable": true, "targets": isStudent ? [1, 2, 3, 4, 5, 6] : [1, 2, 3, 4, 5] }
    ];

    const table = $('.user-table').DataTable({
        "pageLength": 5,
        "lengthMenu": [5, 10, 15, 20, 25, 50, 100],
        "ordering": true,
        "order": [],
        "columnDefs": columnDefs,
        "language": {
            "search": "",
            "searchPlaceholder": "Search students...",
            "lengthMenu": "Show _MENU_ per page",
            "zeroRecords": "No matching records found",
            "info": "Showing _START_ to _END_ of _TOTAL_ entries",
            "infoEmpty": "No entries available",
            "infoFiltered": "(filtered from _MAX_ total entries)",
            "paginate": {
                "next": ">",
                "previous": "<"
            }
        },
        "initComplete": function () {
            $(".dataTables_filter label").contents().filter(function () {
                return this.nodeType === 3;
            }).remove();

            $(".dataTables_filter").prepend(
                "<label class='me-2 font-medium'>🔎</label>"
            );
        }
    });

    // Row number logic
    table.on('order.dt search.dt draw.dt', function () {
        table.column(0, { search: 'applied', order: 'applied' }).nodes().each(function (cell, i) {
            cell.innerHTML = i + 1;
        });
    }).draw();
});
