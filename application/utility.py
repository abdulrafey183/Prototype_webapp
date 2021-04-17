def savecnic(cnicfile, cnic, side):

	''' 
	Utility function to save the CNIC image file
	uploaded by the user.
	'''
	
	if not cnicfile:
		flash("ERROR: CNIC Image Missing!", "danger")
		return False

	# path to folder for storing cnic images
	cnic_file_path = app.root_path + '\\static\\img\\cnic\\agents\\' + str(cnic) + side + '.jpg'

	cnicfile.save(cnic_file_path)
	return cnic_file_path
