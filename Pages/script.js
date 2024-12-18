const videoMapContainer = document.querySelector(".video-map-container");
videoMapContainer.style.width = videoMapContainer.offsetWidth + "px";
videoMapContainer.style.height = videoMapContainer.offsetHeight + "px";

let isDragging = false;
let currentClip = null;
let previousMouseY = 0;

document.addEventListener("mousedown", (event) =>
{
    const fileDropZone = event.target.closest(".file-drop-zone");
    const backgroundClip = event.target.closest(".background-clip");
    const videoClip = event.target.closest(".video-clip");
    if (fileDropZone || !backgroundClip && !videoClip)
    {
        return;
    }

    // Set the dragging state
    isDragging = true;
    currentClip = backgroundClip || videoClip;

    currentClip.classList.add("dragging");
    document.body.style.userSelect = "none";
});
document.addEventListener("mousemove", (event) =>
{
    if (!isDragging || !currentClip)
    {
        return;
    }

    const parent = currentClip.parentElement;
    const siblings = [
        ...parent.children
    ].filter((child) =>
        currentClip.classList.contains(child.classList) &&
        child !== currentClip
    );

    const mouseY = event.clientY - parent.getBoundingClientRect().top;
    const nextSibling = siblings.find((sibling) =>
    {
        if (mouseY > previousMouseY)
        {
            // Moving downward
            return mouseY <= sibling.offsetTop;
        }
        else
        {
            // Moving upward
            return mouseY <= sibling.offsetTop + sibling.offsetHeight;
        }
    });
    parent.insertBefore(currentClip, nextSibling);

    previousMouseY = mouseY;
});
document.addEventListener("mouseup", () =>
{
    if (!currentClip)
    {
        return;
    }

    // Reset the dragging state
    currentClip.classList.remove("dragging");
    document.body.style.userSelect = "auto";

    isDragging = false;
    currentClip = null;
});

const fileDropZones = [...document.getElementsByName("fileDropZone")];
const fileInputs = [...document.getElementsByName("fileInput")];
const fileInfo = document.getElementById("fileInfo");

function handleFile(file, index)
{
    // fileInfo.textContent = `Selected file: ${file.name} (${file.size} bytes)`;
}

fileDropZones.forEach(fileDropZone =>
{
    // Dragover event (prevent default to allow drop)
    fileDropZone.addEventListener("dragover", (event) =>
    {
        event.preventDefault();
        fileDropZone.classList.add("dragover");
    });

    // Dragleave event
    fileDropZone.addEventListener("dragleave", () =>
    {
        fileDropZone.classList.remove("dragover");
    });

    // Drop event
    fileDropZone.addEventListener("drop", (event) =>
    {
        event.preventDefault();
        fileDropZone.classList.remove("dragover");
        const { files } = event.dataTransfer;
        if (files.length)
        {
            handleFile(files[0]);
        }
    });

    // Clicking on the zone to open the file dialog
    fileDropZone.addEventListener("click", () =>
    {
        const fileInput = fileDropZone.querySelector("input[type='file']");
        fileInput.click();
    });
});

// File input change event
fileInputs.forEach(fileInput =>
{
    fileInput.addEventListener("change", (event) =>
    {
        const { files } = event.target;
        if (files.length)
        {
            files.forEach((file, index) =>
            {
                handleFile(file, index);
            });
        }
    });
});