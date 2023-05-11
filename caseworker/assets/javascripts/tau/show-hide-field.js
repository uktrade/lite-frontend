class ShowHideFormField {
  // Default form field is display: none;
  constructor(divElement) {
    this.divElement = divElement;
  }

  // Methods
  showField = () => {
    this.divElement.style.display = "revert";
  };
  hideField = () => {
    this.divElement.style.display = "none";
  };
}

export default ShowHideFormField;
