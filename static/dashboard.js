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

function renderCardsFromTable() {
    const tableRows = document.querySelectorAll("#tableBody tr");
    const cardContainer = document.getElementById("cardContainer");
    cardContainer.innerHTML = "";

    tableRows.forEach(row => {
      const cells = row.querySelectorAll("td");
      if (cells.length < 4) return;

      const title = cells[0].textContent.trim();
      const author = cells[1].textContent.trim();
      const genre = cells[2].textContent.trim();
      const rating = cells[3].textContent.trim();

      const col = document.createElement("div");
      col.className = "col-md-4 mb-4";

      col.innerHTML = `
        <div class="card book-card h-100">
          <div class="card-body">
            <h5 class="card-title">${title}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${author}</h6>
            <p class="card-text"><strong>Genre:</strong> ${genre}</p>
            <span class="badge bg-primary">Rating: ${rating}</span>
          </div>
        </div>
      `;

      cardContainer.appendChild(col);
    });
  }

  // Watch for changes in the table and update cards
  const observer = new MutationObserver(renderCardsFromTable);
  observer.observe(document.getElementById("tableBody"), { childList: true });