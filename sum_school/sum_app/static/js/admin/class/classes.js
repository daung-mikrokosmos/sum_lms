const scheduletable = document.querySelector('#schedule--table');

// at first none sorting column
let sortColumnIndex = -1;
let sortDirectionControl = 1;

const sortTable = (columnIndex) => {
    const headerRowItems = [...scheduletable.tHead.rows[0].cells];
    const bodyRows = [...scheduletable.tBodies[0].rows];

    if(sortColumnIndex === columnIndex){
        sortDirectionControl *= -1;
    } else {
        sortColumnIndex = columnIndex;
    }

    // re arrange rows
    bodyRows.sort((a,b)=> {
        const A = a.cells[columnIndex].innerText;
        const B = b.cells[columnIndex].innerText;

        return A.localeCompare(B, undefined, {numeric : true}) * sortDirectionControl;
    })

    //Append new sorted Rows to table body
    bodyRows.forEach((row)=> {
        scheduletable.tBodies[0].appendChild(row);
    })

    // change the pointer according to the sorting column
    headerRowItems.forEach((th,i)=> {
        th.classList.remove('sort-asc','sort-desc');

        if(i === columnIndex) {
            th.classList.add(sortDirectionControl === 1 ? 'sort-asc' : 'sort-desc');
        }
    })
}