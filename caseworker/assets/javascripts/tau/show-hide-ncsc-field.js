class ShowHideNcscField {
  constructor($ncssFieldWrapper) {
    this.$ncssFieldWrapper = $ncssFieldWrapper;
  }

  showField() {
    this.$ncssFieldWrapper.style.display = "revert";
  }

  hideField() {
    this.$ncssFieldWrapper.style.display = "none";
  }

  toggleField(ratings) {
    if (ratings.some((rating) => rating.startsWith("ML"))) {
      this.showField();
    } else {
      this.hideField();
      this.$ncssFieldWrapper.querySelector("input").checked = false;
    }
  }
}

export default ShowHideNcscField;
