import getpass, os, imaplib, email, sys, datetime, subprocess, webbrowser
import oauth2 as oauth
import pygtk, gtk, time, json

clientid = "84849698594-gkbpua9fomsdentqhaimfn83iphoqg1h.apps.googleusercontent.com"
clientsecret = "KP3jKw4cGWY9BBNcwZizlat9"
mydict = { 'clientid': "84849698594-gkbpua9fomsdentqhaimfn83iphoqg1h.apps.googleusercontent.com", 'clientsecret': "KP3jKw4cGWY9BBNcwZizlat9" }
usrname = ""

def process(M):
	rv, data = M.search(None, "ALL")
	if rv != 'OK':
		print "No messages found!"
		return
	otpt = []
	yp = 0
	for num in data[0].split()[::-1]:
		if yp == 10: break
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print "ERROR getting message", num
			return
		msg = data[0][1]
		pp = msg.split('\n')
		output = ""
		for i in pp:
			if 'Subject: ' in str(i): output += (str(i) + '\n')
			if 'Date: ' in str(i): output += (str(i) + '\n')
			if 'From: ' in str(i): output += (str(i) + '\n')
		otpt.append(output)
		yp+=1
	return otpt


def JsonWriter(dict):
	try:
		if os.path.isdir(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail')):
			with open(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'test.json'), 'w') as outfile:
				json.dump(dict, outfile)
			return True
		else:
			os.mkdir(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail'))
			with open(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'test.json'), 'w') as outfile:
				json.dump(dict, outfile)
			return True
	except:
		print "File Error!"
		return False

def checkUser(username):
	uname = username.get_text()
	writename = ""
	if uname.endswith("@gmail.com"): 
		mydict['username'] = uname
		return True
	elif uname == "": 
		return False
	else: 
		mydict['username'] = uname+"@gmail.com"
		return True

def vfyChecker(fr, usernameentry, vfyurl, passcodeentry):
	if checkUser(usernameentry):
		webbrowser.open(vfyurl, new=1)
		passcodeentry.set_sensitive(True)
	else:
		msgDialog = gtk.MessageDialog(fr, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Please enter the email/ username of Gmail")
		msgDialog.run()
		msgDialog.destroy()
		
def DefaultDo(tag = "First", chkr = 'INBOX'):
	if tag == "Firsttime":
		#if JsonWriter(mydict):
		myop = CheckMail('INBOX')
		mywin = ""
		if myop[0]: mywin = UIMaker(myop[1], myop[2])
		return mywin
	else:
		try:
			myop = CheckMail(chkr)
			if myop[0]:
				mywin = UIMaker(myop[1], myop[2])
				return mywin
			else:
				with open(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'test.json'), 'r') as json_file:
					json_dat = json.load(json_file)
					mydict = json_dat
				reff = mydict['refresh_token']
				#print reff
				reftoken = oauth.RefreshToken(clientid, clientsecret, reff)
				#print reftoken
				jsonldd = reftoken
				#print jsonldd
				mydict['access_token'] = jsonldd['access_token']
				if JsonWriter(mydict):
					time.sleep(1000)
					myop = CheckMail(chkr)
					mywin = UIMaker(myop[1], myop[2])
					return mywin
		except IndexError:
			time.sleep(100)
			DefaultDo()

		
def verifiedCodes(fr, pCode, fram):
	authcode = pCode.get_text()
	if authcode == "":
		msDialog = gtk.MessageDialog(fr, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "Please copy authentication/verification code from Google and paste here!")
		msDialog.run()
		msDialog.destroy()
	else:
		hh = oauth.AuthorizeTokens(clientid, clientsecret, authcode)
		line = str(hh).replace('\'', '"').replace('u', '')
		jsonld = json.loads(line)
		mydict['access_token'] = jsonld['access_token']
		mydict['refresh_token'] = jsonld['refresh_token']
		if JsonWriter(mydict): 
			mDialog = gtk.MessageDialog(fr, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "Success")
			mDialog.run()
			mDialog.destroy()
			window.hide_all()
			#vbox.remove(fram)
			vbox.destroy()
			wwin = DefaultDo("Firsttime")
			#vbox.add(wwin)
			window.add(wwin)
			window.show_all()
			return True
		else:
			mDialog = gtk.MessageDialog(fr, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "Error! Try again")
			mDialog.run()
			mDialog.destroy()
			return False
				
def NextStepProcess():
	frame = gtk.Frame()
	frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
	frame.set_border_width(2)
	frame.set_size_request(40, 30)
	imghbox = gtk.HBox()
	img = gtk.Image()
	img.set_from_file(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'logo.png'))
	img.set_size_request(200, 50)
	img.show()
	imghbox.pack_start(img, False)
	
	uhbox = gtk.HBox()
	username = gtk.Label("         Username:   ")
	usernameentry = gtk.Entry()
	usernameentry.set_size_request(190, 25)
	uhbox.pack_start(username, False)
	uhbox.pack_start(usernameentry, False)
	phbox = gtk.HBox()
	passcode = gtk.Label("Verfication Code:   ")
	passcodeentry = gtk.Entry()
	passcodeentry.set_visibility(False)
	passcodeentry.set_invisible_char(u"\u2022")
	passcodeentry.set_size_request(190, 25)
	passcodeentry.set_sensitive(False)
	phbox.pack_start(passcode, False)
	phbox.pack_start(passcodeentry, False)

	btnhbox = gtk.HBox()
	cancelbtn = gtk.Button(stock=gtk.STOCK_CANCEL)
	#cancelbtn.set_label("Cancel")
	cancelbtn.set_relief(gtk.RELIEF_NONE)
	cancelbtn.set_size_request(100, 30)
	#cancelbtn.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("#FFFFFF"))
	#cancelbtn.set_use_stock(True)
	cancelbtn.show()
	cancelbtn.connect("clicked", lambda x: gtk.main_quit())
	btnhbox.pack_start(cancelbtn, False)

	blanklabel = gtk.Label("            ")
	btnhbox.pack_start(blanklabel, False)

	nextbtn = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
	#nextbtn = gtk.LinkButton("http://www.google.com", )
	nextbtn.set_size_request(100, 30)
	nextbtn.connect("clicked", lambda q: verifiedCodes(window, passcodeentry, frame))
	nextbtn.set_relief(gtk.RELIEF_NONE)
	btnhbox.pack_start(nextbtn, False)
	btntable = gtk.Table(1, 4, False)
	vfyurl = "https://accounts.google.com/o/oauth2/auth?client_id=84849698594-gkbpua9fomsdentqhaimfn83iphoqg1h.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=https%3A%2F%2Fmail.google.com%2F"
	vfyhbox = gtk.HBox()
	vfybtn = gtk.Button("Get Verification Code from Google")
	vfybtn.set_size_request(310, 30)
	vfybtn.connect("clicked", lambda q: [vfyChecker(window, usernameentry, vfyurl, passcodeentry) ])
	vfybtn.set_relief(gtk.RELIEF_NORMAL)
	vfyhbox.pack_start(vfybtn, False)

	alignment = gtk.Alignment(0.5, 0.3, 0, 0)
	alignment.add(table)

	table.set_row_spacings(20)
	table.set_col_spacings(20)
	table.attach(imghbox, 0, 1, 0, 1, xoptions=gtk.EXPAND, yoptions = 0)
	table.attach(uhbox, 0, 1, 1, 2, xoptions=gtk.EXPAND, yoptions = 0)
	table.attach(vfyhbox, 0, 1, 2, 3, xoptions=gtk.EXPAND, yoptions = 0)
	table.attach(phbox, 0, 1, 3, 4, xoptions=gtk.EXPAND, yoptions = 0)
	#btntable.attach(btnhbox, 0, 1, 2, 3, xoptions=gtk.EXPAND, yoptions = gtk.FILL)
	#btntable.attach(cancelbtn, 0, 1, 0, 1)
	#btntable.attach(nextbtn, 0, 1, 0, 1)
	table.attach(btnhbox, 0, 1, 4, 5, xoptions=gtk.EXPAND, yoptions = 0)
	frame.add(alignment)
	return frame
	
def changer(change1):
	window.hide_all()
	vbox.remove(change1)
	getframe = NextStepProcess()
	vbox.add(getframe)
	window.show_all()

def CheckMail(tag):
	try:
		myemail = mydict['username']
		access_token = mydict['access_token']
		auth_string = 'user=%s\1auth=Bearer %s\1\1' % (myemail, access_token)
		imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
		imap_conn.debug = 4
		imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
		imap_conn.select(tag)
		imaplist = imap_conn.list()
		mylist = imaplist[1]
		return [True, mylist, imap_conn]
	except:
		return [False]

def ConnectME(fr, labl):
	sDialog = gtk.MessageDialog(fr, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, labl)
	sDialog.run()
	sDialog.destroy()
		
def UIMaker(mylist, imap_conn):
	result = process(imap_conn)
	frame = gtk.Frame()
	vbox = gtk.VBox()
	vbox.set_size_request(0,40)
	hbox = gtk.HBox()
	vbox.pack_start(hbox, False)
	table = gtk.Table(10, 1, gtk.FALSE)
	hhbox = gtk.HBox()
	wh = window.get_size()
	table.show()
	labels = ['(\\HasNoChildren) "/" "INBOX"', '(\\Flagged \\HasNoChildren) "/" "[Gmail]/Starred"', '(\\HasNoChildren \\Sent) "/" "[Gmail]/Sent Mail"', '(\\Drafts \\HasNoChildren) "/" "[Gmail]/Drafts"', '(\\HasNoChildren \\Important) "/" "[Gmail]/Important"']
	for i in mylist:
		if str(i) in labels:
			btn = gtk.Button()
			btn.set_size_request(80, 40)
			if 'INBOX' in str(i):
				lbl = gtk.Label()
				lbl.set_text('Inbox')
				lbl.set_line_wrap(True)
				btn.set_label(lbl.get_text())
			if 'Sent Mail' in str(i): 
				btn.set_label('Sent Mail')
				#btn.connect('clicked', sentmail)
			if 'Starred' in str(i): btn.set_label('Starred')
			if 'Drafts' in str(i): btn.set_label('Drafts')
			if 'Important' in str(i): btn.set_label('Important')
			#eb = gtk.EventBox()
			#eb.add(btn)
			btn.show()
			btn.connect("clicked", lambda a: ConnectME(window, btn.get_label()))
			btn.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#F2F2F2"))
			hbox.pack_start(btn, False)
	refbtn = gtk.ToolButton(gtk.STOCK_REFRESH)
	refbtn.set_size_request(40, 40)
	refbtn.show()
	refbtn.set_tooltip_text("Get Messages")
	refbtn.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#F2F2F2"))
	hbox.pack_start(refbtn, False)
	scroller = gtk.ScrolledWindow(None, None)
	scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	scroller.show()
	vvbox = gtk.VBox()
	layout = gtk.Layout(None, None)
	cnt = 0
	for i in result:
		btn = gtk.Button()
		btn.set_size_request(50, 70)
		lbl = gtk.Label()
		lbl.set_text(str(i))
		lbl.set_line_wrap(True)
		btn.set_label(lbl.get_text())
		#btn.set_label(str(i))
		#vvbox.pack_start(btn, False)
		table.attach(btn, 0, 1, cnt, cnt+1)
		cnt += 80
		#scroller.add(btn)
	scroller.add_with_viewport(table)
	vbox.pack_start(scroller, True, True, 0)
	#talignment = gtk.Alignment(0.1, 0.1, 0.1, 0.1)
	vbox.set_size_request(100, wh[1])
	#talignment.add(hhbox)
	hhbox.pack_start(vbox, True, True, 0)
	return hhbox
	
def OneTimePage():
	frame2 = gtk.Frame()
	imghbox = gtk.HBox()
	img = gtk.Image()
	img.set_from_file(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'logo.png'))
	img.set_size_request(200, 50)
	img.show()
	imghbox.pack_start(img, False)
	starttable = gtk.Table(3, 1, False)
	starttable.set_size_request(900, 500)
	starttable.set_row_spacings(20)
	starttable.set_col_spacings(20)
	startalignment = gtk.Alignment(0.3, 0.3, 0.1, 0.1)
	startalignment.add(starttable)
	starttable.attach(imghbox, 0, 1, 0, 1, xoptions=gtk.EXPAND, yoptions = 0)
	
	texthbox = gtk.HBox()
	starttextview = gtk.TextView()
	starttextview.set_size_request(800, 400)
	starttextview.show()
	starttextbuffer = starttextview.get_buffer()
	mitlicfile = open(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'mitlicense.txt'), 'r')
	mitlicstring = mitlicfile.read()
	mitlicfile.close()
	starttextbuffer.set_text(mitlicstring)
	starttextview.set_wrap_mode(gtk.WRAP_WORD)
	starttextview.set_editable(False)
	texthbox.pack_start(starttextview, False)
	starttable.attach(texthbox, 0, 1, 1, 2, xoptions=gtk.EXPAND, yoptions = 0)
	
	btnhbox = gtk.HBox()
	cancelbtn = gtk.Button(stock=gtk.STOCK_QUIT)
	#cancelbtn.set_label("Cancel")
	cancelbtn.set_relief(gtk.RELIEF_NONE)
	cancelbtn.set_size_request(100, 30)
	#cancelbtn.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("#FFFFFF"))
	#cancelbtn.set_use_stock(True)
	cancelbtn.show()
	cancelbtn.connect("clicked", lambda x: gtk.main_quit())
	btnhbox.pack_start(cancelbtn, False)
	blanklabel = gtk.Label("            ")
	btnhbox.pack_start(blanklabel, False)
	nextbtn = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
	#nextbtn = gtk.LinkButton("http://www.google.com", )
	nextbtn.set_size_request(100, 30)
	nextbtn.connect("clicked", lambda q: changer(frame2))
	nextbtn.set_relief(gtk.RELIEF_NONE)
	btnhbox.pack_start(nextbtn, False)
	starttable.attach(btnhbox, 0, 1, 2, 3, xoptions=gtk.EXPAND, yoptions = 0)
	frame2.add(startalignment)
	return frame2

window = gtk.Window()
window.set_default_size(900, 700)
window.set_size_request(440, 500)
window.set_title("TestMail App")
window.set_resizable(True)
window.set_icon_from_file(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'gmaillogo.png'))
window.set_position(gtk.WIN_POS_CENTER)
#stIcon = gtk.StatusIcon()
#stIcon.set_from_file(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'gmaillogo.png'))
#stIcon.set_visible(True)
table = gtk.Table(4, 3, False)
hbox = gtk.HBox()
vbox = gtk.VBox()
getf2 = ""

#getf1 = NextStepProcess()
if os.path.isfile(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'test.json')):
	with open(os.path.join(os.path.sep, os.path.expanduser('~'), 'TestMail', 'test.json'), 'r') as json_file:
		json_dat = json.load(json_file)
		mydict = json_dat
	window.hide_all()
	wwin = DefaultDo()
	vboxe = gtk.VBox()
	vboxe.pack_start(wwin, False)
	#vbox.pack_start(wwin, False)
	window.add(vboxe)	
	window.show_all()
else: 
	getf2 = OneTimePage()
	vbox.add(getf2)
	window.add(vbox)
	window.show_all()
#frame.add(vbox)


#vbox.pack_start(table, False)
#vbox.add(alignment)
#vbox.pack_start(phbox, False)



window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
window.show_all()
window.connect("destroy", lambda w: gtk.main_quit())
gtk.main()