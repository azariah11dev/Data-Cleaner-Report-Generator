document.addEventListener("click", () => {
    document.getElementById("upload-btn").addEventListener("click", async () => {
        const file = document.getElementById("fileInput").files[0];
        if (!file) return alert("Select a file first");

        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch("http://localhost:8000/cleaner/upload", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        window.cleanedFilePath = data.cleaned_file_path;   // store globally
        console.log("Uploaded:", data);
    });

    document.getElementById("apply-btn").addEventListener("click", async () => {
        if (!window.cleanedFilePath) {
            return alert("Upload a file first");
        }

        const missing_strategy = document.getElementById("strategy").value;
        const columns = document.getElementById("columns").value
            .split(",")
            .map(c => c.trim());
        const fill_value = document.getElementById("fill-value").value;

        const res = await fetch("http://localhost:8000/cleaner/apply", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                cleaned_file_path: window.cleanedFilePath,
                strategy: missing_strategy,
                columns: columns,
                fill_value: fill_value
            })
        });

        const data = await res.json();
        console.log("Updated stats:", data.stats);

        // Now fetch preview
        const previewRes = await fetch(
            `http://localhost:8000/live-update/changes?cleaned_file_path=${window.cleanedFilePath}`
        );

        const previewData = await previewRes.json();
        console.log("Preview:", previewData);
    });

});