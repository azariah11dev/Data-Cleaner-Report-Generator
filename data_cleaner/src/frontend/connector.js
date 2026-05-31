/*
==================================================================================== 
helper functions
====================================================================================
*/
function renderPreviewTable(data) {
    const container = document.getElementById("preview-container");

    let tableHTML = "<table border='1' cellpadding='6' style='border-collapse: collapse;'>";
    tableHTML += "<thead><tr>";

    data.columns.forEach(col => {
        tableHTML += `<th>${col}</th>`;
    });

    tableHTML += "</tr></thead>";
    tableHTML += "<tbody>";

    data.preview.forEach(row => {
        tableHTML += "<tr>";
        data.columns.forEach(col => {
            tableHTML += `<td>${row[col] ?? ""}</td>`;
        });
        tableHTML += "</tr>";
    });

    tableHTML += "</tbody></table>";
    container.innerHTML = tableHTML;
}


function renderStats(stats) {
    const container = document.getElementById("stats-container");
    container.innerHTML = "";

    const wrapper = document.createElement("div");
    wrapper.className = "stats-wrapper";

    wrapper.innerHTML = `
        <h3>Cleaning Summary</h3>
        <p><strong>Strategy:</strong> ${stats.strategy}</p>
        <p><strong>Rows Before:</strong> ${stats.rows_before}</p>
        <p><strong>Rows After:</strong> ${stats.rows_after}</p>
        <p><strong>Fill Value:</strong> ${stats.fill_value ?? "None"}</p>
        <hr>
        <h4>Missing Values (Before)</h4>
    `;

    const beforeTable = document.createElement("table");
    beforeTable.className = "stats-table";
    beforeTable.innerHTML = `<tr><th>Column</th><th>Missing</th></tr>`;

    for (const [col, val] of Object.entries(stats.missing_before)) {
        beforeTable.innerHTML += `<tr><td>${col}</td><td>${val}</td></tr>`;
    }

    wrapper.appendChild(beforeTable);
    wrapper.innerHTML += `<h4>Missing Values (After)</h4>`;

    const afterTable = document.createElement("table");
    afterTable.className = "stats-table";
    afterTable.innerHTML = `<tr><th>Column</th><th>Missing</th></tr>`;

    for (const [col, val] of Object.entries(stats.missing_after)) {
        afterTable.innerHTML += `<tr><td>${col}</td><td>${val}</td></tr>`;
    }

    wrapper.appendChild(afterTable);
    container.appendChild(wrapper);
}

/*
==================================================================================== 
Upload
====================================================================================
*/
document.getElementById("upload-btn").addEventListener("click", async (e) => {
    e.preventDefault();
    const file = document.getElementById("fileInput").files[0];
    if (!file) return alert("Select a file first");

    // FIX 1: declare data in outer scope so the preview fetch can access it
    let uploadData;

    try {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch("http://localhost:8000/cleaner/upload", {
            method: "POST",
            body: formData
        });

        uploadData = await res.json();

        window.filePath = uploadData.file_path;
        window.cleanedFileName = uploadData.file_name;

        console.log("Uploaded:", uploadData);

    } catch (err) {
        console.error("Error uploading file:", err);
        return alert(`Upload failed: ${err.message}`);
    }

    try {
        const previewRes = await fetch(
            `http://localhost:8000/live-update/preview?file_name=${encodeURIComponent(uploadData.file_name)}`
        );

        const previewData = await previewRes.json();
        console.log("Preview:", previewData);
        renderPreviewTable(previewData);
    } catch (err) {
        console.error("Error fetching preview:", err);
    }
});

/*
==================================================================================== 
Apply cleaning
====================================================================================
*/
document.getElementById("apply-btn").addEventListener("click", async (e) => {
    e.preventDefault();
    if (!window.filePath) {
        return alert("Upload a file first");
    }

    const missing_strategy = document.getElementById("strategy").value;
    const columns = document.getElementById("columns").value
        .split(",")
        .map(c => c.trim())
        .filter(c => c.length > 0);

    const fill_value = document.getElementById("fill-value").value.trim();

    // FIX 2: validate that fill_value is provided when strategy is "constant"
    if (missing_strategy === "constant" && fill_value === "") {
        return alert("A fill value is required for the Constant strategy");
    }

    try {
        const res = await fetch("http://localhost:8000/cleaner/clean", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                file_name: window.cleanedFileName,
                missing_strategy: missing_strategy,
                columns: columns,
                fill_value: fill_value
            })
        });

        // FIX 3: fetch doesn't throw on 4xx/5xx — check res.ok and render error into stats-container
        if (!res.ok) {
            const err = await res.json();
            const detail = err.detail || "Unknown error";
            document.getElementById("stats-container").innerHTML =
                `<p style="color: red;"><strong>Error:</strong> ${detail}</p>`;
            return;
        }

        const data = await res.json();
        console.log("Updated stats:", data.stats);

        window.cleanedFilePath = data.cleaned_file;
        renderStats(data.stats);

    } catch (err) {
        console.error("Error applying cleaning:", err);
        document.getElementById("stats-container").innerHTML =
            `<p style="color: red;"><strong>Error:</strong> ${err.message}</p>`;
    }
});

/*
==================================================================================== 
Download
====================================================================================
*/
document.getElementById("downloadBtn").addEventListener("click", async (e) => {
    e.preventDefault();
    try {
        const url = `http://localhost:8000/live-update/download?file_path=${encodeURIComponent(window.cleanedFilePath)}`;
        console.log("Downloading from:", url);
        window.location.href = url;
    } catch (err) {
        console.error("Error downloading file:", err);
    }
});

/*
==================================================================================== 
Delete
====================================================================================
*/
document.getElementById("deleteBtn").addEventListener("click", async (e) => {
    e.preventDefault();

    if (!window.filePath && !window.cleanedFilePath) {
        return alert("No files to delete");
    }

    const uploadPath = encodeURIComponent(window.filePath);
    const cleanedPath = encodeURIComponent(window.cleanedFilePath);

    try {
        const res = await fetch(
            `http://localhost:8000/delete/target?upload_path=${uploadPath}&cleaned_path=${cleanedPath}`,
            { method: "DELETE" }
        );

        const data = await res.json();
        console.log("Delete response:", data);

        alert("Files deleted successfully");

        window.filePath = null;
        window.cleanedFilePath = null;

        document.getElementById("stats-container").innerHTML = "";
        document.getElementById("preview-container").innerHTML = "";

    } catch (err) {
        console.error("Error deleting files:", err);
        alert("Failed to delete files");
    }
});