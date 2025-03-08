let currentPage = 1;
let limit = 5;

async function fetchBooks() {
    let genre = document.getElementById("genreFilter").value;
    let rating = document.getElementById("ratingFilter").value;
    limit = document.getElementById("limitSelect").value;

    let url = `/books?page=${currentPage}&limit=${limit}`;
    if(genre) {
        url += `&genre=${genre}`;
    }
    if(rating) {
        url += `&rating=${rating}`;
    }

    try {
        const response = await fetch(url);
        const data = await response.json();

        let tableBody = document.getElementById("tableBody");
        tableBody.innerHTML = "";

        data.books.forEach(book => {
            let row = `<tr>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.genre}</td>
                    <td>${book.rating || "N/A"}</td>
                </tr>`;
            tableBody.innerHTML += row;
        });

        totalPages = data.total_pages;

        updatePageButtons();

    } 
    catch (error) {
        console.error("Error fetching books : ", error);
    }
}

function nextPage() {
    if(currentPage < totalPages) {
        currentPage++;
        fetchBooks();
    } 
}

function prevPage() {
    if(currentPage > 1) {
        currentPage--;
    }
    fetchBooks();
}

function updateLimit() {
    currentPage = 1;
    fetchBooks();
}

function updatePageButtons() {
    document.getElementById("prevBtn").disabled = currentPage === 1;
    document.getElementById("nextBtn").disabled = currentPage >= totalPages;
}

window.onload = fetchBooks;