#!/usr/bin/python

import cgitb
import cgi
import base64
import subprocess
cgitb.enable()
form = cgi.FieldStorage()

opts={}
opts['filecont']=""
opts['debug']=""
opts['form']=""
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

if img is not None:
	try:
		fname = filetype+":-"

		p= subprocess.Popen(['identify','-format',"%[fx:w] %[fx:h]",fname],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		p.stdin.write(str(base64.b64decode(img)))
		(imageid,stderr) = p.communicate()
		(imgw,imgh) = imageid.split()
		opts['debug']+="Image is {0}x{1}".format(imgw,imgh)

		#imgopts = ['-grayscale','average'] 
		imgopts = ['-colorspace','Gray'] 

		# Get from /etc/ImageMagick-6/thresholds.xml
		#imgopts += ['-dither','FloydSteinberg','-colors','2']
		#imgopts += ['-ordered-dither','h4x4o']
		imgopts += ['-brightness-contrast','20,45']
		#imgopts += ['-ordered-dither','c7x7b']
		imgopts += ['-ordered-dither','h8x8a']
		#imgopts += ['-ordered-dither','checks']
		#imgopts += ['-ordered-dither','h4x4a']
		#imgopts += ['-ordered-dither','c7x7w']
		p= subprocess.Popen(['convert',fname]+imgopts+[fname],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		p.stdin.write(str(base64.b64decode(img)))
		(out,stderr) = p.communicate()
		out = base64.b64encode(out)
		opts['filecont']+='<p>OUTPUT</p>'
		opts['filecont']+='<img src="data:image/{filetype};base64, {img}" alt="Retained file" />'.format(img=out,filetype=str(filetype))
	except BaseException as e:
		opts['filecont']+=str(e)
print "Content-type: text/html"
print
fd = open("lasor.html")
html =  fd.read()
print html.format(**opts)
