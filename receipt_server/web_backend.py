from flask import Flask, request, jsonify
from flask_cors import CORS 
import image_processor

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
	print("trying to get uploaded file")
	# Check if the POST request contains a file
	# if 'file' not in request.files:
	# 	return 'No file part'

	file = request.files['picture']
	image_text = image_processor.process_image(file)
	image_text[:] = [x for x in image_text if x.strip()]
	return_list = []
	for item in image_text:
		if "Subtotal" not in item and "Tax" not in item and "Tip" not in item and "Total" not in item:
			if item[0] in "123456789":
				quantity = item[0]
			else:
				quantity = 1
			price = item[item.find("$"):]
			name = item[1:item.find("$")]
			if int(quantity) > 1:
				for i in range(int(quantity)):
					return_list.append([1, name, price])
			else:
				return_list.append([quantity, name, price])
		elif "Subtotal" in item:
			subtotal = item[item.find("$")+1:]
		elif "Tax" in item:
			tax = item[item.find("$")+1:]
		elif "Tip" in item:
			tip = item[item.find("$")+1:]
	tax_rate = float(tax)/float(subtotal)
	tip_rate = float(tip)/float(subtotal)
	# return_list.append["multiplier", "Tax", tax/subtotal]
	# return_list.append["percent", "Tip", tip/subtotal]
	print(image_text)
	print("printed image text")
	# Check if the file has a filename
	if file.filename == '':
		return 'No selected file'

		
	return jsonify(item_list=return_list,
					tax_rate=tax_rate,
					tip_rate=tip_rate)

if __name__ == '__main__':
    app.run(debug=True)