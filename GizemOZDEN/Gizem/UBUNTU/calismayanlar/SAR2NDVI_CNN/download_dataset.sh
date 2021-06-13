# download
wget -o dataset.zip "http://www.grip.unina.it/index.php?option=com_content&view=article&id=79&Itemid=489&jsmallfib=1&dir=JSROOT/SAR2NDVI_CNN&download_file=JSROOT/SAR2NDVI_CNN/DATASET.zip"

# unpack
unzip -d dataset.zip DATASET

# remove zip file
rm -rf dataset.zip
