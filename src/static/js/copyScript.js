function copyToClipboard(button) {
    const copyText = document.querySelector("#shortened-url");
    const container = button.parentElement;
    container.classList.add('show-tooltip');
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
    setTimeout(() => {
        container.classList.remove('show-tooltip');
    }, 2000);
}
