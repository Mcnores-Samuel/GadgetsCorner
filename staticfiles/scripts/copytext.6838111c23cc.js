function copyText(elementId) {
  // Get the text from the span
  const textToCopy = document.querySelector(`#${elementId}`).innerText;
  const textcontainer = document.querySelector(`#${elementId}`);

  const textarea = document.createElement('textarea');
  textarea.innerText = textToCopy;
  document.body.appendChild(textarea);

  textarea.select();
  textarea.focus();
  document.execCommand('copy');
  document.body.removeChild(textarea);
  textcontainer.classList.add('text-success');
  textcontainer.innerText = 'Copied!';
  setTimeout(() => {
    textcontainer.innerText = textToCopy;
  }, 1000);
}
