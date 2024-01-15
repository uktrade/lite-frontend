class ShowHideNcscField {
  constructor($ncscFieldWrapper) {
    this.$ncscFieldWrapper = $ncscFieldWrapper;
  }

  showField() {
    this.$ncscFieldWrapper.style.display = "revert";
  }

  hideField() {
    this.$ncscFieldWrapper.style.display = "none";
  }

  toggleField(ratings) {
    if (ratings.some((rating) => rating.startsWith("ML"))) {
      this.showField();
    } else {
      this.hideField();
      this.$ncscFieldWrapper.querySelector("input").checked = false;
    }
  }
}

export default ShowHideNcscField;
