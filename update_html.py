# Load the existing HTML file
html_file_path = "cannabis_intel_nexus.html"

with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Inject JavaScript to fetch and display strain data dynamically
updated_html_content = html_content.replace("</body>", """
<script>
    document.addEventListener("DOMContentLoaded", function() {
        fetch("strains.json")  // Fetch JSON data
        .then(response => response.json())
        .then(data => {
            const strainContainer = document.getElementById("strain-list");
            strainContainer.innerHTML = ""; // Clear existing content

            data.forEach(strain => {
                let strainCard = document.createElement("div");
                strainCard.className = "strain-card";
                strainCard.innerHTML = `
                    <h2>${strain["Strain"]}</h2>
                    <p><strong>Brand:</strong> ${strain["Brand"]}</p>
                    <p><strong>Category:</strong> ${strain["Category"]}</p>
                    <p><strong>Type:</strong> ${strain["Product Type"]}</p>
                    <p><strong>THC:</strong> ${strain["Total THC (%)"]}% | 
                       <strong>CBD:</strong> ${strain["Total CBD (%)"]}%</p>
                    <p><strong>Total Terpenes:</strong> ${strain["Terpenes Total (%)"]}%</p>
                    <p><strong>Effects:</strong> ${strain["Effects"]}</p>
                `;
                strainContainer.appendChild(strainCard);
            });
        })
        .catch(error => console.error("Error fetching strains:", error));
    });
</script>
</body>
""")

# Save the updated HTML file
updated_html_file_path = "cannabis_intel_nexus_updated.html"
with open(updated_html_file_path, "w", encoding="utf-8") as file:
    file.write(updated_html_content)

# Provide the updated HTML file path for integration
updated_html_file_path
