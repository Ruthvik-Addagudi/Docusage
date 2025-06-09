// Unified and Fully Optimized JavaScript File

document.addEventListener('DOMContentLoaded', function () {

    console.log("Script loaded successfully");

    const dqaPopup = document.getElementById("dqa-popup");
    const dqaButton = document.getElementById("dqa-btn");
    const dqaCloseButton = document.getElementById("dqa-close-popup");
    const dqaStartExamButton = document.getElementById("dqa-start-exam");
    const dqaSubmitExamButton = document.getElementById("dqa-submit-exam");
    const dqaDownloadFeedbackButton = document.getElementById("dqa-download-feedback");
    const dqaSetup = document.getElementById("dqa-setup");
    const dqaExamSection = document.getElementById("dqa-exam-section");
    const dqaFeedbackSection = document.getElementById("dqa-feedback-section");
    const dqaExamQuestions = document.getElementById("dqa-exam-questions");
    const dqaFeedbackContent = document.getElementById("dqa-feedback-content");
    const dqaTimerDisplay = document.getElementById("dqa-timer-display");
    const dqaTimerCount = document.getElementById("dqa-timer-count");

    let uploadedFile = false;
    let timerInterval;
    let quizQuestions = [];

    document.getElementById("file-upload").addEventListener("change", function () {
        uploadedFile = true;
        console.log("File uploaded successfully.");
    });

    if (!dqaButton || !dqaPopup || !dqaCloseButton || !dqaStartExamButton || !dqaSubmitExamButton || !dqaDownloadFeedbackButton) {
        console.error("Error: Missing DOM elements.");
        return;
    }

    // ---------- Common Elements ---------- //
    const outputTextarea = document.getElementById('output');
    const dragDropArea = document.getElementById('drag-drop-area');
    const fileInput = document.getElementById('file-upload');
    const uploadStatus = document.getElementById('upload-status');
    const summarizeBtn = document.getElementById('summarize-btn');
    const mindmapBtn = document.getElementById('mindmap-btn');
    const trueFalseBtn = document.getElementById('true-false-btn');
    const fillBlankBtn = document.getElementById('fill-blank-btn');
    const mcqBtn = document.getElementById('mcq-btn');

    //const outputTextarea = document.getElementById("output");
    const autoSaveToggle = document.getElementById("autoSaveToggle");
    const loadRecentAnalysisBtn = document.getElementById("loadRecentAnalysis");
    const clearOutputBtn = document.getElementById("clearOutput");
    const downloadOutputBtn = document.getElementById("downloadOutput");
    
    const STORAGE_KEY = "docusage_saved_analysis";

    let analysisData = JSON.parse(localStorage.getItem('savedAnalyses')) || {};
    let uploadedFilePath = "";
    let summary = "";

    const darkModeToggle = document.getElementById("darkModeToggle");
    const body = document.body;
    const header = document.querySelector(".header");

    // Check if dark mode is already enabled
    if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-mode");
        header.classList.add("dark-mode");
        darkModeToggle.innerHTML = "☀️"; // Sun icon for light mode
    }

    // Toggle dark mode on button click
    darkModeToggle.addEventListener("click", function () {
        body.classList.toggle("dark-mode");
        header.classList.toggle("dark-mode");

        // Save user preference
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("darkMode", "enabled");
            darkModeToggle.innerHTML = "☀️"; // Sun icon when dark mode is active
        } else {
            localStorage.setItem("darkMode", "disabled");
            darkModeToggle.innerHTML = "🌙"; // Moon icon when light mode is active
        }
    });

    // ---------- Utility Functions ---------- //
    function updateLoadDropdown(filter = '') {
        // Commenting out this function as "loadDropdown" is not defined in the HTML
        // loadDropdown.innerHTML = '<option value="">Select a saved analysis...</option>';
        // Object.keys(analysisData).filter(key => key.toLowerCase().includes(filter.toLowerCase())).forEach(key => {
        //     let option = document.createElement('option');
        //     option.value = key;
        //     option.textContent = key;
        //     loadDropdown.appendChild(option);
        // });
    }

    function fetchData(endpoint, postData, successCallback) {
        fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(postData)
        })
            .then(response => response.json())
            .then(successCallback)
            .catch(() => outputTextarea.value += `Error fetching data from ${endpoint}\n`);
    }

    function handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    uploadedFilePath = data.file_path;
                    uploadStatus.textContent = data.message;
                    uploadStatus.style.color = '#28a745';
                } else {
                    uploadStatus.textContent = `Error: ${data.error}`;
                    uploadStatus.style.color = '#dc3545';
                }
            })
            .catch(() => {
                uploadStatus.textContent = 'An error occurred during upload.';
                uploadStatus.style.color = '#dc3545';
            });
    }

    // ---------- File & Text Analysis Handling ---------- //
    summarizeBtn.addEventListener('click', () => {
        if (!uploadedFilePath) return alert('Please upload a PDF file first.');

        fetchData('/extract-text', { file_path: uploadedFilePath }, data => {
            fetchData('/summarize', { text: data.text }, sumData => {
                summary = sumData.summary;
                outputTextarea.value += `\nSummary:\n${summary}\n\n`;
            });
        });
    });

    const questionHandlers = {
        'true-false-btn': { endpoint: '/true-false', label: 'True/False Questions', count: 5 },
        'fill-blank-btn': { endpoint: '/fill-in-the-blanks', label: 'Fill in the Blanks', count: 3 },
        'mcq-btn': { endpoint: '/mcq', label: 'Multiple-Choice Questions (MCQs)', count: 5 }
    };

    Object.keys(questionHandlers).forEach(id => {
        document.getElementById(id).addEventListener('click', () => {
            if (!summary) return alert('Please generate a summary first.');
            const { endpoint, label, count } = questionHandlers[id];

            fetchData(endpoint, { text: summary, num_questions: count }, data => {
                outputTextarea.value += `\n${label}:\n`;

                if (endpoint === '/mcq') {
                    data.mcqs.forEach((q, i) => {
                        outputTextarea.value += `${i + 1}. ${q.question}\n`;
                        q.options.forEach((opt, j) => outputTextarea.value += `   ${String.fromCharCode(65 + j)}. ${opt}\n`);
                        outputTextarea.value += `   (Correct Answer: ${q.correct_answer})\n\n`;
                    });
                } else {
                    data.questions.forEach((q, i) => outputTextarea.value += `${i + 1}. ${q.question} (Answer: ${q.answer})\n`);
                }
            });
        });
    });

    mindmapBtn.addEventListener('click', () => {
        if (!summary) return alert('Please generate a summary first.');
        fetchData('/generate-mind-map', { text: summary }, data => alert(data.message || data.error));
    });

    // ---------- File Upload Drag & Drop ---------- //
    dragDropArea.addEventListener('dragover', e => { e.preventDefault(); dragDropArea.style.borderColor = '#0056b3'; });
    dragDropArea.addEventListener('dragleave', () => dragDropArea.style.borderColor = '#007bff');
    dragDropArea.addEventListener('drop', e => { e.preventDefault(); handleFileUpload(e.dataTransfer.files[0]); });

    fileInput.addEventListener('change', e => handleFileUpload(e.target.files[0]));

    document.getElementById("searchButton").addEventListener("click", function () {
        performSearch();
    });
    
    // Make Enter Key trigger search
    document.getElementById("searchInput").addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            performSearch();
        }
    });
    
    // Toggle Case Sensitivity in Real-Time
    document.getElementById("caseSensitiveToggle").addEventListener("change", function () {
        performSearch();
    });
    
    // Function to Perform Search
    function performSearch() {
        let keyword = document.getElementById("searchInput").value.trim();
        let caseSensitive = document.getElementById("caseSensitiveToggle").checked;
    
        if (!keyword) {
            alert("Please enter a keyword to search.");
            return;
        }
    
        fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword: keyword, caseSensitive: caseSensitive })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                displaySearchResults(data.results, keyword, caseSensitive);
            }
        })
        .catch(error => console.error("Error:", error));
    }
    
    // Display Search Results
    function displaySearchResults(results, keyword, caseSensitive) {
        let resultsContainer = document.getElementById("searchResults");
        resultsContainer.innerHTML = "";
    
        if (results.length === 0) {
            resultsContainer.innerHTML = "<p>No matches found.</p>";
            return;
        }
    
        // Highlight Matched Text in Results
        let regex = new RegExp(keyword, caseSensitive ? "g" : "gi"); // Case-sensitive toggle
        results.forEach(text => {
            let highlightedText = text.replace(regex, match => `<mark>${match}</mark>`);
            let resultItem = document.createElement("p");
            resultItem.innerHTML = highlightedText;
            resultsContainer.appendChild(resultItem);
        });
    }
    
    // Show Popup when Search Button is Clicked (Main UI)
    document.getElementById("searchButtonMain").addEventListener("click", function () {
        document.getElementById("searchPopup").style.display = "block";
    });
    
    // Close search popup when close button is clicked
    document.getElementById("closeSearchPopup").addEventListener("click", function () {
        document.getElementById("searchPopup").style.display = "none";
    });

    // Close popup when Escape key is pressed
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            document.getElementById("searchPopup").style.display = "none";
        }
    });

    document.getElementById("saveButton").addEventListener("click", function () {
        let outputContent = document.getElementById("output").value.trim();
    
        if (!outputContent) {
            alert("⚠️ No analysis available to save. Please generate content first.");
            return;
        }
    
        // Get uploaded file name (if available), otherwise use default
        let uploadedFileName = document.getElementById("uploadedFileName")?.innerText || "analysis";
        let cleanFileName = uploadedFileName.replace(/\.[^/.]+$/, ""); // Remove file extension
        let defaultFileName = cleanFileName + "_" + new Date().toISOString().replace(/[:.]/g, "-");
    
        document.getElementById("fileNameInput").value = defaultFileName; // Set default file name
        document.getElementById("savePopup").style.display = "block";
    });
    
    // ✅ Pressing "Enter" Key Saves & Closes Save Popup
    document.getElementById("fileNameInput").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            document.getElementById("confirmSave").click(); // Trigger Save
        }
    });
    
    document.getElementById("confirmSave").addEventListener("click", function () {
        let fileName = document.getElementById("fileNameInput").value.trim();
        let outputContent = document.getElementById("output").value.trim();
    
        if (!fileName) {
            alert("⚠️ File name cannot be empty.");
            return;
        }
    
        fetch('/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fileName: fileName, content: outputContent })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("✅ Analysis saved successfully!");
                document.getElementById("savePopup").style.display = "none";
            } else {
                alert("❌ Error saving file: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));
    });
    
    document.getElementById("cancelSave").addEventListener("click", function () {
        document.getElementById("savePopup").style.display = "none";
    });
    
    // ✅ Load Feature with Properly Aligned Icons
    document.getElementById("loadButton").addEventListener("click", function () {
        fetch('/load')
        .then(response => response.json())
        .then(data => {
            let loadPopup = document.getElementById("loadPopup");
            let fileList = document.getElementById("fileList");
    
            fileList.innerHTML = ""; // Clear previous content
    
            if (data.files.length === 0) {
                fileList.innerHTML = "<p>No saved analyses found.</p>";
            } else {
                data.files.forEach(file => {
                    let listItem = document.createElement("li");
                    listItem.classList.add("file-item");
    
                    // Container for file details (Ensures alignment)
                    let fileDetails = document.createElement("div");
                    fileDetails.classList.add("file-details");
    
                    // File Name Display (Removing .json Extension)
                    let fileNameSpan = document.createElement("span");
                    fileNameSpan.innerText = file.replace(".json", ""); 
                    fileNameSpan.classList.add("file-name");
    
                    fileDetails.appendChild(fileNameSpan);
                    listItem.appendChild(fileDetails);
    
                    // Icon Container (Ensures icons are aligned properly)
                    let iconContainer = document.createElement("div");
                    iconContainer.classList.add("icon-container");
    
                    // ✅ Load Button
                    let loadBtn = document.createElement("button");
                    loadBtn.innerHTML = "📂"; // Folder icon
                    loadBtn.classList.add("icon-btn");
                    loadBtn.onclick = function () {
                        fetch(`/get_analysis?file=${file}`)
                        .then(response => response.json())
                        .then(fileData => {
                            document.getElementById("output").value = fileData.content;
                            alert("✅ Analysis Loaded!");
                            loadPopup.style.display = "none";
                        })
                        .catch(error => console.error("Error:", error));
                    };
                    iconContainer.appendChild(loadBtn);
    
                    // ✅ Delete Button
                    let deleteBtn = document.createElement("button");
                    deleteBtn.innerHTML = "🗑️"; // Trash icon
                    deleteBtn.classList.add("icon-btn");
                    deleteBtn.onclick = function () {
                        if (confirm("⚠️ Are you sure you want to delete this file?")) {
                            fetch(`/delete?file=${file}`, { method: 'DELETE' })
                            .then(response => response.json())
                            .then(result => {
                                if (result.success) {
                                    listItem.remove(); // Remove from UI
                                    alert("✅ File Deleted Successfully.");
                                } else {
                                    alert("❌ Error Deleting File: " + result.error);
                                }
                            })
                            .catch(error => console.error("Error:", error));
                        }
                    };
                    iconContainer.appendChild(deleteBtn);
    
                    listItem.appendChild(iconContainer);
                    fileList.appendChild(listItem);
                });
            }
            loadPopup.style.display = "block";
        })
        .catch(error => console.error("Error:", error));
    });
    
    // ✅ Close Load Popup
    document.getElementById("closeLoadPopup").addEventListener("click", function () {
        document.getElementById("loadPopup").style.display = "none";
    });

    // ✅ Load saved analysis on page load
    const savedText = localStorage.getItem(STORAGE_KEY);
    if (savedText) {
        outputTextarea.value = savedText;  // Load into textarea
    }

    // ✅ Auto-Save Functionality
    function saveAnalysis() {
        if (autoSaveToggle.checked) {
            localStorage.setItem(STORAGE_KEY, outputTextarea.value);
        }
    }

    // ✅ Listen for input changes
    outputTextarea.addEventListener("input", saveAnalysis);

    // ✅ Handle auto-save checkbox changes
    autoSaveToggle.addEventListener("change", function () {
        if (!autoSaveToggle.checked) {
            localStorage.removeItem(STORAGE_KEY);
        } else {
            saveAnalysis();
        }
    });

    // ✅ Load Most Recent Analysis Button
    loadRecentAnalysisBtn.addEventListener("click", function () {
        const savedText = localStorage.getItem(STORAGE_KEY);
        if (savedText) {
            outputTextarea.value = savedText;
            alert("✅ Your last analysis has been restored.");
        } else {
            alert("⚠️ No recent analysis found.");
        }
    });

    // ✅ Auto-Save every 5 seconds (if enabled)
    setInterval(function () {
        if (autoSaveToggle.checked) {
            localStorage.setItem(STORAGE_KEY, outputTextarea.value);
        }
    }, 5000);


    // ✅ Clear Output with Confirmation
    clearOutputBtn.addEventListener("click", function () {
        const confirmClear = confirm("⚠️ Are you sure you want to clear the analysis? This cannot be undone.");
        if (confirmClear) {
            outputTextarea.value = "";
            localStorage.removeItem(STORAGE_KEY);
            alert("✅ Output cleared permanently.");
        }
    });

    // ✅ Download Output
    downloadOutputBtn.addEventListener("click", function () {
        const text = outputTextarea.value;
        if (text.trim() === "") {
            alert("No output to download.");
            return;
        }

        const blob = new Blob([text], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "analysis_output.txt";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });



    //Dynamic question generation module code
    // ✅ Open Quiz Setup
    dqaButton.addEventListener("click", function () {
        if (!uploadedFile) {
            alert("Please upload a file first.");
            return;
        }
        dqaPopup.style.display = "block";
        dqaSetup.style.display = "block";
        dqaExamSection.style.display = "none";
        dqaFeedbackSection.style.display = "none";
        dqaTimerDisplay.style.display = "none";
    });

    // ❌ Close Quiz Popup
    dqaCloseButton.addEventListener("click", function () {
        dqaPopup.style.display = "none";
        clearInterval(timerInterval);
    });

    // 🏁 Start Quiz
    dqaStartExamButton.addEventListener("click", function () {
        let selectedTypes = [];
        if (document.getElementById("dqa-mcq").checked) selectedTypes.push("mcq");
        if (document.getElementById("dqa-true-false").checked) selectedTypes.push("true_false");
        if (document.getElementById("dqa-fill-blank").checked) selectedTypes.push("fill_in_the_blanks");

        let numQuestions = parseInt(document.getElementById("dqa-num-questions").value);
        let timerMinutes = parseInt(document.getElementById("dqa-timer").value);

        if (selectedTypes.length === 0) {
            alert("Please select at least one question type.");
            return;
        }
        if (isNaN(numQuestions) || numQuestions <= 0) {
            alert("Please enter a valid number of questions.");
            return;
        }
        if (isNaN(timerMinutes) || timerMinutes <= 0) {
            alert("Please enter a valid exam duration.");
            return;
        }

        fetch("/generate_dqa", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question_types: selectedTypes, num_questions: numQuestions })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            quizQuestions = data.questions;
            dqaSetup.style.display = "none";
            dqaExamSection.style.display = "block";
            dqaFeedbackSection.style.display = "none";
            dqaExamQuestions.innerHTML = "";
            dqaTimerDisplay.style.display = "block";

            quizQuestions.forEach((q, index) => {
                dqaExamQuestions.innerHTML += `
                    <p><b>Q${index + 1}:</b> ${q.question}</p>
                    <input type="text" id="answer-${index}" placeholder="Your answer"><br><br>
                `;
            });

            let timeRemaining = timerMinutes * 60;
            timerInterval = setInterval(() => {
                let minutes = Math.floor(timeRemaining / 60);
                let seconds = timeRemaining % 60;
                dqaTimerCount.textContent = `${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;
                if (timeRemaining <= 0) {
                    clearInterval(timerInterval);
                    dqaSubmitExamButton.click();
                }
                timeRemaining--;
            }, 1000);
        })
        .catch(error => {
            console.error("❌ Error:", error);
            alert(`Failed to load questions: ${error.message}`);
        });
    });

    // ✅ Submit Quiz
    dqaSubmitExamButton.addEventListener("click", function () {
        clearInterval(timerInterval);

        let answers = quizQuestions.map((q, index) => {
            return {
                question: q.question,
                correct_answer: q.correct_answer,
                user_answer: document.getElementById(`answer-${index}`).value.trim()
            };
        });

        fetch("/evaluate_dqa", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers: answers })
        })
        .then(response => response.json())
        .then(data => {
            dqaExamSection.style.display = "none";
            dqaFeedbackSection.style.display = "block";
        
            // ✅ Add score here
            dqaFeedbackContent.innerHTML = `<h3>Feedback</h3><p><b>Score:</b> ${data.score} / ${data.total}</p><hr>`;
        
            data.feedback.forEach(f => {
                dqaFeedbackContent.innerHTML += `
                    <p><b>Question:</b> ${f.question}</p>
                    <p><b>Your Answer:</b> ${f.correct ? "✅ Correct" : `❌ Incorrect (Correct: ${f.correct_answer})`}</p>
                    <hr>
                `;
            });
        })
        .catch(error => {
            console.error("Error evaluating answers:", error);
            alert("Evaluation failed. Try again.");
        });
    });

    // ⬇️ Download Feedback
    dqaDownloadFeedbackButton.addEventListener("click", function () {
        window.location.href = "/download_feedback";
    });

});