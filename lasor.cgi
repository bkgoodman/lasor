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
opts['dest_unit']=""
opts['scangap']=""
opts['dpi']=""
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

		if 'input_dest_width' in form:
			try:
				opts['dest_width'] = float(form['input_dest_width'].value)
			except BaseException as e:
				opts['dest_width'] = imgw
		if 'input_dest_height' in form:
			try:
				opts['dest_height'] = float(form['input_dest_height'].value)
			except:
				opts['dest_height'] = imgh
		opts['dest_unit']=""
		if 'input_unit' in form and form['input_unit'].value.strip() != "":
			opts['dest_unit'] = form['input_unit'].value
		else:
			opts['dest_unit'] = "pixels"

		if 'input_posterize' in form:
			opts['posterize'] = "input_posterize_"+form['input_posterize'].value.strip()

		if 'input_dpi' in form:
			opts['dpi'] = form['input_dpi'].value.strip()
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
		#imgopts = ['-grayscale','average'] 
		if 'input_posterize' in form:
			try:
				imgopts += ['-posterize',str(int(form['input_posterize'].value))]
				opts['debug'] += "\n"+"POSTERIZE "+str(int(form['input_posterize'].value))+"\n"
			except BaseException as e:
				opts['debug'] += "Posetize err"+str(e)
				pass
		imgopts += ['-colorspace','Gray'] 

		# Get from /etc/ImageMagick-6/thresholds.xml
		#imgopts += ['-dither','FloydSteinberg','-colors','2']
		#imgopts += ['-ordered-dither','h4x4o']
		if brightness != 0 or contrast != 0:
			imgopts += ['-brightness-contrast',"{0},{1}".format(brightness,contrast)]
		#imgopts += ['-ordered-dither','c7x7b']
		imgopts += ['-ordered-dither','h8x8a']
		#imgopts += ['-ordered-dither','checks']
		#imgopts += ['-ordered-dither','h4x4a']
		#imgopts += ['-ordered-dither','c7x7w']
		
		imgopts += ['-normalize']
		p= subprocess.Popen(['convert',fname]+imgopts+[fname],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		p.stdin.write(str(base64.b64decode(img)))
		(out,stderr) = p.communicate()
		opts['debug'] += str(stderr)
		out = base64.b64encode(out)
		opts['filecont']+='<p>OUTPUT</p>'
		opts['filecont']+='<img src="data:image/{filetype};base64, {img}" alt="Retained file" />'.format(img=out,filetype=str(filetype))
	except BaseException as e:
		opts['filecont']+=str(e)
		opts['filecont']+=str(sys.exc_info())
print "Content-type: text/html"
print
fd = open("lasor.html")
html =  fd.read()
print html.format(**opts)
