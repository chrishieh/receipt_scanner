<!-- src/components/PictureUpload.vue -->

<template>
  <div class="picture-upload">
    <label for="file-input" class="file-label">
      <span>Select a Picture</span>
      <input type="file" id="file-input" @change="handleFileUpload" />
    </label>
    <div v-if="selectedFile" class="preview-container">
      <img :src="imageUrl" alt="Selected" class="preview-image" />
    </div>
    <button @click="uploadPicture" :disabled="!selectedFile">Upload</button>

    <div v-if="uploadedData.length > 0" class="uploaded-data">
      <h3>Uploaded Data:</h3>
      <table>
        <thead>
          <tr>
            <th>Quantity</th>
            <th>Item</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rowData, rowIndex) in uploadedData" :key="rowIndex" @click="selectRow(rowIndex)" :class="{ 'selected-row': selectedRows.includes(rowIndex) }">
            <td v-for="(cellData, cellIndex) in rowData" :key="cellIndex">
              {{ cellData }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="paymentData.length > 0" class="payment-data">
      <h3>Your Bill:</h3>
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Ammount</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rowData, rowIndex) in paymentData" :key="rowIndex" @click="selectRow(rowIndex)" :class="{ 'selected-row': selectedRows.includes(rowIndex) }">
            <td v-for="(cellData, cellIndex) in rowData" :key="cellIndex">
              {{ cellData }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <button @click="calculateBill" class="calculate-bill-button">Calculate Bill</button>
    
    <div v-if="combinedString" class="combined-string">
      <h3>Your Subtotal:</h3>
      <p>{{ yourSubtotal }}</p>
    </div>

    <div v-if="selectedRowsData.length > 0" class="selected-rows">
      <h3>Selected Rows:</h3>
      <table>
        <thead>
          <tr>
            <th>Quantity</th>
            <th>Item</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rowData, rowIndex) in selectedRowsData" :key="rowIndex">
            <td v-for="(cellData, cellIndex) in rowData" :key="cellIndex">
              {{ cellData }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      imageUrl: null,
      uploadedData: [],
      taxRate: null,
      tipRate: null, 
      combinedString: '',
      selectedRows: [],
      selectedRowsData: [],
      paymentData: [],
      yourSubtotal: 0,
      yourTax: 0,
      yourTip: 0,
      yourTotal: 0
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      this.imageUrl = URL.createObjectURL(this.selectedFile);
    },
    uploadPicture() {
      if (!this.selectedFile) {
        console.error("Please select a picture before uploading.");
        return;
      }

      const formData = new FormData();
      formData.append("picture", this.selectedFile);

      // Replace the URL with your actual API endpoint
      const apiUrl = "http://localhost:5000/upload"; // Assuming your API is running on localhost:5000

      axios
        .post(apiUrl, formData)
        .then((response) => {
          console.log("Picture uploaded successfully!", response);
          this.uploadedData = response.data.item_list; // Assuming the array is in the 'data' property of the response
          this.taxRate = response.data.tax_rate
          console.log(this.taxRate)
          this.tipRate = response.data.tip_rate
        })
        .catch((error) => {
          console.error("Error uploading picture", error);
        });
    },
    selectRow(rowIndex) {
      // Toggle the selection state of the clicked row
      const index = this.selectedRows.indexOf(rowIndex);
      if (index === -1) {
        this.selectedRows.push(rowIndex);
      } else {
        this.selectedRows.splice(index, 1);
      }
    },
    calculateBill() {
      // For demonstration purposes, concatenate the values in the selected rows for the combined string
      this.combinedString = this.selectedRows.map(row => this.uploadedData[row][0]).join(' ');

      // Populate the selectedRowsData array with the data of the selected rows
      this.selectedRowsData = this.selectedRows.map(row => this.uploadedData[row]);
      var sum = 0;
      for (var i = 0; i < this.selectedRowsData.length; i++) {
        var numberWithoutDollar = this.selectedRowsData[i][2].substring(1);
        var parsedNumber = parseFloat(numberWithoutDollar);

        sum += parsedNumber
      }
      console.log(sum)
      this.yourSubtotal = sum;
      this.yourTip = sum * this.tipRate
      this.yourTax = sum * this.taxRate
      this.yourTotal = this.yourSubtotal + this.yourTax + this.yourTip
      this.selectedRowsData.concat(["", "Your Subtotal", this.yourSubtotal])
      this.paymentData = [["Your Subtotal: ", this.yourSubtotal],
                          ["Your Tax: ", this.yourTax],
                          ["Your Tip: ", this.yourTip],
                          ["Your Total: ", this.yourTotal]]
    },
  },
};
</script>



<style scoped>
/* Your styles for mobile-friendly design */
body {
    background-color: #f8f8f8; /* Set your desired light background color */
    color: #333;
  }

.picture-upload {
  padding: 20px;
}

.file-label {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  background-color: #4caf50;
  color: #fff;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.file-label:hover {
  background-color: #45a049;
}

.upload-button {
  margin-top: 10px;
  padding: 10px;
  background-color: #2196f3;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.upload-button:hover {
  background-color: #0b7dda;
}

.uploaded-data {
  margin-top: 20px;
}

.uploaded-data h3 {
  font-size: 1.2em;
  color: #333;
}

.uploaded-data table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.uploaded-data th, .uploaded-data td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.uploaded-data tr:hover {
  background-color: #f5f5f5;
}

.uploaded-data .selected-row {
  background-color: #add8e6; /* Light blue background for selected rows */
}

.calculate-bill-button {
  margin-top: 20px;
  padding: 10px;
  background-color: #2196f3;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.calculate-bill-button:hover {
  background-color: #0b7dda;
}

.combined-string {
  margin-top: 20px;
}

.combined-string h3 {
  font-size: 1.2em;
  color: #333;
}

.combined-string p {
  margin: 0;
  color: #333;
}

.selected-rows {
  margin-top: 20px;
}

.selected-rows h3 {
  font-size: 1.2em;
  color: #333;
}

.selected-rows table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.selected-rows th, .selected-rows td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
</style>