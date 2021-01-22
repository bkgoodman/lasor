#!/usr/bin/python

import cgitb
import sys
import cgi
import base64
import subprocess
cgitb.enable()
form = cgi.FieldStorage()

opts={}
opts['filecont']=""
opts['debug']=""
opts['form']=""
opts['height']=""
opts['width']=""
opts['brightness']=50
opts['contrast']=50
opts['title']="The title"
img=None
filetype=None
loadfile=False
if 'input_file' in form:
	fi = form['input_file']
	opts['debug']+=str(dir(fi))+"\n"
	opts['debug']+=str(dir(fi.file))+"\n"
	opts['debug']+=str(fi.length)+"\n"
	if fi.file and fi.filename:
		try:
			img=base64.b64encode(fi.file.read())
			filetype=fi.filename.split(".")[-1]
			opts['filecont']='<img src="data:image/{filetype};base64, {img}" alt="Input File" />'.format(img=img,filetype=filetype)
			#opts['debug']+=str(dir(fi))
			#opts['debug']+="\n"
			opts['debug']+=str(fi.filename)
			loadfile=True
			opts['form'] += '<input type="hidden" id="input_origfile" name="input_origfile" value="{0}"></input>'.format(img)+"\n"
			opts['form'] += '<input type="hidden" id="input_origfiletype" name="input_origfiletype" value="{0}"></input>'.format(filetype)+"\n"
		except BaseException as e:
			opts['filecont']=str(e)
	elif 'input_origfile' in form:
			img = form['input_origfile'].value
			filetype = form['input_origfiletype'].value
			opts['filecont']='<img src="data:image/{filetype};base64, {img}" alt="Retained file" />'.format(img=img,filetype=str(filetype))
			opts['debug']+="orig type {0}\n".format(filetype)
			opts['form'] += '<input type="hidden" id="input_origfile" name="input_origfile" value="{0}"></input>'.format(img)+"\n"
			opts['form'] += '<input type="hidden" id="input_origfiletype" name="input_origfiletype" value="{0}"></input>'.format(filetype)+"\n"

opts['dest_width']=""
opts['dest_height']=""
opts['threshold']=50
opts['black_threshold']=0
opts['white_threshold']=100
opts['dest_unit']=""
opts['scangap']=""
opts['dpi']="300"
opts['res_type']=""
opts['posterize']="input_posterize_none"
if img is not None:
	try:
		fname = filetype+":-"

		p= subprocess.Popen(['identify','-format',"%[fx:w] %[fx:h]",fname],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		p.stdin.write(str(base64.b64decode(img)))
		(imageid,stderr) = p.communicate()
		(imgw,imgh) = imageid.split()
		opts['debug']+="Image is {0}x{1}".format(imgw,imgh)
		opts['width']=imgw
		opts['height']=imgh

		if loadfile:
				opts['dest_width'] = imgw
		elif 'input_dest_width' in form:
			try:
				opts['dest_width'] = float(form['input_dest_width'].value)
			except BaseException as e:
				opts['dest_width'] = imgw

		if loadfile:
				opts['dest_height'] = imgh
		elif 'input_dest_height' in form:
			try:
				opts['dest_height'] = float(form['input_dest_height'].value)
			except:
				opts['dest_height'] = imgh
		opts['dest_unit']=""

		if loadfile:
			opts['dest_unit'] = "pixels"
			opts['dest_unit'] = "pixels"
		elif 'input_unit' in form and form['input_unit'].value.strip() != "":
			opts['dest_unit'] = form['input_unit'].value
		else:
			opts['dest_unit'] = "pixels"

		if 'input_threshold' in form:
			opts['threshold'] = form['input_threshold'].value
		if 'input_white_threshold' in form:
			opts['white_threshold'] = form['input_white_threshold'].value
		if 'input_black_threshold' in form:
			opts['black_threshold'] = form['input_black_threshold'].value
		if 'input_posterize' in form:
			opts['posterize'] = "input_posterize_"+form['input_posterize'].value.strip()

		if 'input_dpi' in form:
			dpi = 300
			opts['dpi'] = form['input_dpi'].value.strip()
			try:
				dpi = int(opts['dpi'].strip())
			except:
				pass
		if 'input_scangap' in form:
			opts['scangap'] = form['input_scangap'].value.strip()
		if 'input_res_type' in form:
			opts['res_type'] = form['input_res_type'].value.strip()
		try:
			if 'input_brightness' in form:
				opts['brightness'] = int(form['input_brightness'].value.strip())
			if 'input_contrast' in form:
				opts['contrast'] = int(form['input_contrast'].value.strip())
		except:
				opts['brightness'] = 50
				opts['contrast'] = 50

		brightness = opts['brightness']-50
		contrast = opts['contrast']-50

		

		opts['debug']+=str(dict(form))
		imgopts = []

		ww = opts['dest_width']
		hh = opts['dest_height']
		if opts['dest_unit'] == 'inches':
			ww *= dpi
			hh *= dpi
		elif opts['dest_unit'] == 'centimeteres':
			ww *= dpi/2.54
			hh *= dpi/2.54
		imgopts +=['-scale','{0}x{1}'.format(str(int(ww)),str(int(hh)))]
		#imgopts += ['-segment',"1.5x1.5"]
		#imgopts = ['-grayscale','average'] 
		#imgopts += ['-colors','2']
		if 'input_posterize' in form and form['input_posterize'].value != 'none':
			try:
				imgopts += ['-colors',str(int(form['input_posterize'].value))]
				imgopts += ['-median','2']
				pval = int(form['input_posterize'].value)
				if pval > 2: pval=2
				imgopts += ['-posterize',str(pval)]
				opts['debug'] += "\n"+"POSTERIZE "+str(int(form['input_posterize'].value))+"\n"
			except BaseException as e:
				opts['debug'] += "Posetize err"+str(e)
				pass
		imgopts += ['-colorspace','Gray'] 

		# Get from /etc/ImageMagick-6/thresholds.xml
		if brightness != 0 or contrast != 0:
			imgopts += ['-brightness-contrast',"{0},{1}".format(brightness,contrast)]

		if 'input_white_threshold' in form and form['input_white_threshold'].value.strip() != "":
			imgopts += ['-white-threshold',form['input_white_threshold'].value+"%"]

		if 'input_black_threshold' in form and form['input_black_threshold'].value.strip() != "":
			imgopts += ['-black-threshold',form['input_black_threshold'].value+"%"]
		#### imgopts += ['-edge','2']

		#imgopts +=['-scale','50%x50%']
		#imgopts += ['-dither','FloydSteinberg','-colors','2']
		#imgopts +=['-scale','200%x200%']

		if 'input_dither' in form:
			d = form['input_dither'].value
			if d == 'Floyd Steinberg (Fine)':
				imgopts += ['-dither','FloydSteinberg','-colors','2']
			elif d == 'Simple BW Threshold':
				th = form['input_threshold'].value
				imgopts +=['-threshold',th+'%']
			elif d == 'Floyd Steinberg':
				imgopts +=['-scale','50%x50%']
				imgopts += ['-dither','FloydSteinberg','-colors','2']
				imgopts +=['-scale','200%x200%']
			else:
				imgopts += ['-ordered-dither',d]
		#imgopts += ['-ordered-dither','h4x4o']
		#imgopts += ['-ordered-dither','c7x7b']
		#imgopts += ['-ordered-dither','h8x8a']
		#imgopts += ['-ordered-dither','checks']
		#imgopts += ['-ordered-dither','h4x4a']
		#imgopts += ['-ordered-dither','c7x7w']
		ditheropts = [
			'Simple BW Threshold',
			'Floyd Steinberg',
			'Floyd Steinberg (Fine)',
			"checks",
			"o2x2",
			"o3x3",
			"o4x4",
			"o8x8",
			"h4x4a",
			"h6x6a",
			"h8x8a",
			"h4x4o",
			"h6x6o",
			"h8x8o",
			"h16x16o",
			"c5x5b",
			"c5x5w",
			"c6x6b",
			"c6x6w",
			"c7x7b",
			"c7x7w"
		]
		opts['ditheropts']=""
		for x in ditheropts:
			sel=""
			if 'input_dither' in form and x == form['input_dither'].value:
				sel="selected"
			opts['ditheropts'] += "<option {1} value='{0}'>{0}</option>\n".format(x,sel)
	
		hatching = {
			'(None)':None,
			'Diagonal':\
"0,0,0,0,5,"+\
"0,0,0,5,0,"+\
"0,0,5,0,0,"+\
"0,5,0,0,0,"+\
"5,0,0,0,0",
			'Cross':
"0,0,3,0,0,"+\
"0,0,4,0,0,"+\
"3,4,5,4,3,"+\
"0,0,4,0,0,"+\
"0,0,3,0,0",
			'Star':
"0,0,3,0,0,"+\
"0,0,4,0,0,"+\
"3,4,5,4,3,"+\
"0,5,4,0,0,"+\
"5,0,3,0,0",
			'Horizontal':
"0,0,0,0,0,"+\
"0,0,0,0,0,"+\
"5,5,5,5,5,"+\
"0,0,0,0,0,"+\
"0,0,0,0,0",
			'Vertical':
"0,0,5,0,0,"+\
"0,0,5,0,0,"+\
"0,0,5,0,0,"+\
"0,0,4,0,0,"+\
"0,0,5,0,0",
			'Thicken':
"0,0,2,0,0,"+\
"0,3,5,3,0,"+\
"2,5,5,5,2,"+\
"0,3,5,3,0,"+\
"0,0,2,0,0"
		}
		opts['hatching']=""
		for x in sorted(hatching.keys()):
			sel=""
			if 'input_hatching' in form and x == form['input_hatching'].value:
				sel="selected"
			opts['hatching'] += "<option {1} value='{0}'>{0}</option>\n".format(x,sel)

		#imgopts += ['-convolve','0,3,0,3,5,3,0,3,0']

		if 'input_hatching' in form: 
			h= hatching[form['input_hatching'].value]
			if h is not None:
				imgopts += ['-convolve', h]
		imgopts += ['-normalize']
		imgopts +=['-threshold','50%']

		#
		# Torque the image for display
		# Double the width
		newsize = '{0}x{1}'.format(str(int(ww)*2),str(int(hh)))
		imgopts +=['-resize',newsize,'-background','white','-gravity','west','-extent',newsize]
		imgopts+=['-copy','{0}x{1}'.format(ww,hh),"{0},0".format(ww,0)]
		imgopts+=['(','-clone','0','-crop','20x20+150+150','-repage','+200+200!',')','-flatten']
		
		
		opts['debug'] += "\n"
		opts['debug'] += " ".join(imgopts)
		p= subprocess.Popen(['convert',fname]+imgopts+[fname],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		p.stdin.write(str(base64.b64decode(img)))
		(out,stderr) = p.communicate()
		opts['debug'] += str(stderr)
		out = base64.b64encode(out)
		opts['filecont']+='<p>OUTPUT</p>'
		opts['filecont'] ='<img src="data:image/{filetype};base64, {img}" alt="Retained file" />'.format(img=out,filetype=str(filetype))+ "<br/>"+ opts['filecont']
	except BaseException as e:
		opts['filecont']+=str(e)
		opts['filecont']+=str(sys.exc_info())
print "Content-type: text/html"
print
fd = open("lasor.html")
html =  fd.read()
print html.format(**opts)
