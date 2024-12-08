const videoMapContainer = document.querySelector(".video-map-container");
videoMapContainer.style.width = videoMapContainer.offsetWidth + "px";
videoMapContainer.style.height = videoMapContainer.offsetHeight + "px";

let isDragging = false;
let currentClip = null;
let containerOffsetY = 0;
let initY = 0;

document.addEventListener("mousedown", (event) =>
{
    const backgroundClip = event.target.closest(".background-clip");
    const videoClip = event.target.closest(".video-clip");
    if (!backgroundClip && !videoClip)
    {
        return;
    }

    // Set the dragging state
    isDragging = true;
    currentClip = backgroundClip || videoClip;

    // containerOffsetY = currentClip.offsetTop;
    // currentClip.style.top = containerOffsetY + "px";
    // initY = event.clientY;

    currentClip.classList.add("dragging");
    document.body.style.userSelect = "none";
});
let nextSibling = null;
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

    // // this should be the difference from the currentclip top to the previousSibling top or the parent top
    // const _previousSibling = siblings.filter((sibling) =>
    // {
    //     return (
    //         event.clientY - parent.getBoundingClientRect().top >
    //         sibling.offsetTop + sibling.offsetHeight / 2
    //     )
    // }).pop() || parent;
    // console.log(_previousSibling.offsetHeight);

    // Increase the margin top of the next sibling to indicate where the dragging clip will be inserted
    const _nextSibling = siblings.find((sibling) =>
    {
        // console.log(`event.clientY: ${event.clientY}, parent.getBoundingClientRect().top: ${parent.getBoundingClientRect().top}, sibling.offsetTop: ${sibling.offsetTop}, sibling.offsetHeight: ${sibling.offsetHeight}`);
        return (
            event.clientY - parent.getBoundingClientRect().top <=
            sibling.offsetTop + sibling.offsetHeight / 2
        );
    });

    // if (_nextSibling !== nextSibling)
    // {
    //     console.log(`nextSibling.offsetTop: ${nextSibling ? nextSibling.offsetTop : "null"}, _nextSibling.offsetTop: ${_nextSibling ? _nextSibling.offsetTop : "null"}`);
    //     nextSibling = _nextSibling;
    //     containerOffsetY -= nextSibling ? nextSibling.offsetHeight : 0;
    // }

    // let newTop = containerOffsetY - (initY - event.clientY);
    // if (newTop < 0)
    // {
    //     // Can't go above the container height
    //     newTop = 0;
    // }
    // else
    // {
    //     // Can't go below the container height
    //     newTop = Math.min(newTop, parent.offsetHeight);
    // }
    // currentClip.style.top = newTop + "px";

    // // Reset the margin top of all siblings
    // siblings.forEach((clip) =>
    // {
    //     clip.style.marginTop = "10px";
    // });



    // console.log(parent.children);
    // console.log(currentClip.style.top);

    // if (currentClip.classList.contains("video-clip"))
    // {
    //     if (nextSibling)
    //     {
    //         nextSibling.style.marginTop = currentClip.offsetHeight + 20 + "px";
    //     }
    // }
    // else if (currentClip.classList.contains("background-clip"))
    // {
    //     if (nextSibling)
    //     {
    //         nextSibling.style.marginTop = currentClip.offsetHeight + 20 + "px";
    //     }
    // }

    // Insert the dragging clip before the next sibling
    // If there is no next sibling, it will be inserted at the end
    parent.insertBefore(currentClip, _nextSibling);
});
document.addEventListener("mouseup", () =>
{
    if (!currentClip)
    {
        return;
    }

    // // Reset the margin top of all the background clips
    // const parent = currentClip.parentElement;
    // const siblings = [
    //     ...parent.children
    // ].filter((child) =>
    //     currentClip.classList.contains(child.classList) &&
    //     child !== currentClip
    // );
    // siblings.forEach((clip) =>
    // {
    //     clip.style.marginTop = "10px";
    // });

    // Reset the dragging state
    currentClip.classList.remove("dragging");
    document.body.style.userSelect = "auto";

    // currentClip.style.top = "auto";

    isDragging = false;
    currentClip = null;
});