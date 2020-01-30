from flask import Flask, render_template, send_from_directory, url_for, request, redirect
import ephem
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import mpld3
from json import JSONEncoder
import logging

#from io import BytesIO
#import base64
'''
import bokeh.plotting as plt
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.embed import components
'''
app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/otool/calculate/', methods=['POST', 'GET'])
def calculate():
	"""Main method."""

	fightml = ""
	if request.method == 'POST':

		lofar = ephem.Observer()
		lofar.lon = '6.869882'
		lofar.lat = '52.915129'
		lofar.elevation = 15.
		lofar.pressure = 0.     # no refraction at horizon
		lofar.horizon = '-0:34' # idem
		dateTokens = []
		if request.form['date'] != None and request.form['date'] != "":
			dateTokens = request.form['date'].split('/')
		lofar.date = str(dateTokens[2] + '/' + dateTokens[0] + '/' + dateTokens[1])
		endOfDay = lofar.date
		endOfDay += 1.

		targets = []
		aTeam = []
		solSystem = []
		calibrators = []
		time = []
		lst = []
		targetList = ""
		minElevation = 0.
		
		if request.form['elevation'] != None and request.form['elevation'] != "":
			minElevation = np.double(request.form['elevation'])

		if request.form['targetList'] != None and request.form['targetList'] != "":
			targetList = request.form['targetList']

		if request.form['names'] != None and request.form['names'] != "" and request.form['ra'] != None and request.form['ra'] != "" and request.form['dec'] != None and request.form['dec'] != "":
			for name, ra, dec in zip(request.form['names'].split(","), request.form['ra'].split(","), request.form['dec'].split(",")):
				target = Target()
				target.name = name
				target.elevation = []
				target.body = createFixedBody(str(ra), str(dec), '2000')
				target.body.compute(lofar)
				target.note = "</br>" + name + " and "
				targets.append(target)

		if request.form.get('CygA') != None:
			cygA = Target()
			cygA.name = 'CygA'
			cygA.elevation = []
			cygA.body = createFixedBody('19:59:28:3566', '+40:44:02.096', '2000')
			cygA.body.compute(lofar)
			for target in targets:
				target.note += "<li>Cyg A: " + str(ephem.separation(target.body, cygA.body)) + "</li>"
			aTeam.append(cygA)

		if request.form.get('CasA') != None:
			casA = Target()
			casA.name = 'CasA'
			casA.elevation = []
			casA.body = createFixedBody('23:23:27.94', '+58:48:42.4', '2000')
			casA.body.compute(lofar)
			for target in targets:
				target.note += "<li>Cas A: " + str(ephem.separation(target.body, casA.body)) + "</li>"
			aTeam.append(casA)

		if request.form.get('TauA') != None:
			tauA = Target()
			tauA.name = 'TauA'
			tauA.elevation = []
			tauA.body = createFixedBody('05:34:31.971', '+22:00:52.06', '2000')
			tauA.body.compute(lofar)
			for target in targets:
				target.note += "<li>Tau A: " + str(ephem.separation(target.body, tauA.body)) + "</li>"
			aTeam.append(tauA)

		if request.form.get('VirA') != None:
			virA = Target()
			virA.name = 'VirA'
			virA.elevation = []
			virA.body = createFixedBody('12:30:49.4233', '+12:23:28.043', '2000')
			virA.body.compute(lofar)
			for target in targets:
				target.note += "<li>Vir A: " + str(ephem.separation(target.body, virA.body)) + "</li>"
			aTeam.append(virA)

		if request.form.get('Sun') != None:
			sun = Target()
			sun.name = 'Sun'
			sun.elevation = []
			sun.body = ephem.Sun()
			sun.body.compute(lofar)
			for target in targets:
				target.note += "<li>Sun: " + str(ephem.separation(target.body, sun.body)) + "</li>"
			solSystem.append(sun)

		if request.form.get('Jupiter') != None:
			jup = Target()
			jup.name = 'Jupiter'
			jup.elevation = []
			jup.body = ephem.Jupiter()
			jup.body.compute(lofar)
			for target in targets:
				target.note += "<li>Jupiter: " + str(ephem.separation(target.body, jup.body)) + "</li>"
			solSystem.append(jup)

		if request.form.get('Saturn') != None:
			sat = Target()
			sat.name = 'Saturn'
			sat.elevation = []
			sat.body = ephem.Saturn()
			sat.body.compute(lofar)
			for target in targets:
				target.note += "<li>Saturn: " + str(ephem.separation(target.body, sat.body)) + "</li>"
			solSystem.append(sat)

		if request.form.get('3C48') != None:
			c48 = Target()
			c48.name = '3C 48'
			c48.elevation = []
			c48.body = createFixedBody('01:37:41.2994', '+33:09:35.134', '2000')
			c48.body.compute(lofar)
			for target in targets:
				target.note += "<li>3C 48: " + str(ephem.separation(target.body, c48.body)) + "</li>"
			calibrators.append(c48)

		if request.form.get('3C147') != None:
			c147 = Target()
			c147.name = '3C 147'
			c147.elevation = []
			c147.body = createFixedBody('05:42:36.1379', '+49:51:07.234', '2000')
			c147.body.compute(lofar)
			for target in targets:
				target.note += "<li>3C 147: " + str(ephem.separation(target.body, c147.body)) + "</li>"
			calibrators.append(c147)

		if request.form.get('3C295') != None:
			c295 = Target()
			c295.name = '3C 295'
			c295.elevation = []
			c295.body = createFixedBody('14:11:20.519', '+52:12:09.97', '2000')
			c295.body.compute(lofar)
			for target in targets:
				target.note += "<li>3C 295: " + str(ephem.separation(target.body, c295.body)) + "</li>"
			calibrators.append(c295)

		if request.form.get('3C196') != None:
			c196 = Target()
			c196.name = '3C196'
			c196.elevation = []
			c196.body = createFixedBody('08:13:36.033', '+48:13:02.56', '2000')
			c196.body.compute(lofar)
			for target in targets:
				target.note += "<li>3C 196: " + str(ephem.separation(target.body, c196.body)) + "</li>"
			calibrators.append(c196)

		if request.form.get('3C380') != None:
			c380 = Target()
			c380.name = '3C 380'
			c380.elevation = []
			c380.body = createFixedBody('18:29:31.7809', '+48:44:46.160', '2000')
			c380.body.compute(lofar)
			for target in targets:
				target.note += "<li>3C 380: " + str(ephem.separation(target.body, c380.body)) + "</li>"
			calibrators.append(c380)

		if request.form.get('3C286') != None:
			c286 = Target()
			c286.name  = '3C 286'
			c286.elevation = []
			c286.body = createFixedBody('13:31:08.28', '+30:30:32.9', '2000')
			c286.body.compute(lofar)
			for target in targets:
				target.note += "<li>3C 286: " + str(ephem.separation(target.body, c286.body)) + "</li>"
			calibrators.append(c286)

		if request.form.get('CTD93') != None:
			c93 = Target()
			c93.name = 'CTD 93'
			c93.elevation = []
			c93.body = createFixedBody('16:09:13.32', '+26:41:29.0', '2000')
			c93.body.compute(lofar)
			for target in targets:
				target.note += "<li>CTD 93: " + str(ephem.separation(target.body, c93.body)) + "</li>"
			calibrators.append(c93)

		previous = None
		lock = 0

		while lofar.date < endOfDay - ephem.minute:
			lofar.date += ephem.minute

			for target in targets:
				target.body.compute(lofar)
				target.elevation.append(ephem.degrees(target.body.alt) * (180. / math.pi))

			for at in aTeam:
				at.body.compute(lofar)
				at.elevation.append(ephem.degrees(at.body.alt) * (180. / math.pi))

			for calibrator in calibrators:
				calibrator.body.compute(lofar)
				calibrator.elevation.append(ephem.degrees(calibrator.body.alt) * (180. / math.pi))

			for sol in solSystem:
				sol.body.compute(lofar)
				sol.elevation.append(ephem.degrees(sol.body.alt) * (180. / math.pi))

			time.append(lofar.date.datetime())

			if previous > lofar.sidereal_time():
				lock = 1

			if lock:
				lst.append(ephem.Date(str(lofar.date).split(' ')[0].split("/")[0] + "/" + str(lofar.date).split(' ')[0].split("/")[1] + "/" + str(int(str(lofar.date).split(' ')[0].split("/")[2]) + 1) + ' ' + str(lofar.sidereal_time())).datetime())
			else:
				lst.append(ephem.Date(str(lofar.date).split(' ')[0] + ' ' + str(lofar.sidereal_time())).datetime())

			previous = lofar.sidereal_time()

		fig, ax = plt.subplots(2, 1, figsize=(15, 10),sharex=False, sharey=False)
		fig.canvas.draw()
		fig.subplots_adjust(hspace=0.5)

		ax[0].set_yticks([20, 60, 80])
		
		for target in targets:
			ax[0].plot(lst, target.elevation, '--', label=target.name)

		sun = ephem.Sun()
		sun.compute(lofar)
		
		ax[0].hlines(minElevation, lst[0], lst[len(lst) - 1], colors='k', linestyles='solid', lw=2)

		
		# Does not work with mpld3
		#axis1.axvspan(ephem.Date(lofar.previous_rising(sun) - ephem.hour).datetime(), ephem.Date(lofar.previous_rising(sun) + ephem.hour).datetime(), facecolor='0.5', alpha=0.5)
		#trans = transforms.blended_transform_factory(axis1.transData, axis1.transAxes)
		#rect = patches.Rectangle((ephem.Date(lofar.previous_rising(sun) - ephem.hour).datetime(), 20), width=ephem.Date(ephem.hour).datetime(), height=90, transform=trans, color='yellow', alpha=0.5)

		#axis1.add_patch(rect)

		ax[0].set_ylabel(r'Elevation [degrees]', fontsize=18, fontweight='bold', color='#000000')
		ax[0].set_title('LOFAR target visibility', fontsize=20, fontweight='bold')
		
		time = np.array(time)
		cnt = 1
		
		for target in targets:
			ax[1].plot(time, cnt * produceSegments(np.array(target.elevation), minElevation), '--', solid_capstyle='round', lw=5)
			cnt+=1

		for calibrator in calibrators:
			ax[0].plot(lst, calibrator.elevation, label=calibrator.name)
			cnt+=1
			ax[1].plot(time, cnt * produceSegments(np.array(calibrator.elevation), minElevation), solid_capstyle='round', lw=5)

		for at in aTeam:
			ax[0].plot(lst, at.elevation, label=at.name)
			cnt+=1
			ax[1].plot(time, cnt * produceSegments(np.array(at.elevation), minElevation), solid_capstyle='round', lw=5)
		
		for sol in solSystem:
			ax[0].plot(lst, sol.elevation, label=sol.name)
			cnt+=1
			ax[1].plot(time, cnt * produceSegments(np.array(sol.elevation), minElevation), solid_capstyle='round', lw=5)

		sep_message = "The angular distance on the sky (dd:mm:ss.s) between: "

		for target in targets:
			sep_message+=target.note
			sep_message+= "<ul>"
			for calibrator in calibrators:
				sep_message+=calibrator.note
			for at in aTeam:
				sep_message+=at.note
			for sol in solSystem:
				sep_message+=sol.note
			sep_message+= "</ul>"

		ax[1].vlines((lofar.previous_rising(sun)).datetime(), 0, cnt + 1, colors='r', linestyles='dashed', lw=2)
		ax[1].vlines((lofar.previous_setting(sun)).datetime(), 0, cnt + 1, colors='r', linestyles='dashed', lw=2)

		ax[1].vlines(ephem.Date(lofar.previous_rising(sun) - ephem.hour).datetime(), 0, cnt + 1, colors='k', linestyles='dashdot', lw=2)
		ax[1].vlines(ephem.Date(lofar.previous_rising(sun) + ephem.hour).datetime(), 0, cnt + 1, colors='k', linestyles='dashdot', lw=2)

		ax[1].vlines(ephem.Date(lofar.previous_setting(sun) - ephem.hour).datetime(), 0, cnt + 1, colors='k', linestyles='dashdot', lw=2)
		ax[1].vlines(ephem.Date(lofar.previous_setting(sun) + ephem.hour).datetime(), 0, cnt + 1, colors='k', linestyles='dashdot', lw=2)

		ax[1].text(ephem.Date(lofar.previous_rising(sun) - 2. * ephem.hour).datetime(), cnt + 1.5, "Sunrise +/- 1hr")
		ax[1].text(ephem.Date(lofar.previous_setting(sun) - 2. * ephem.hour).datetime(), cnt + 1.5, "Sunset +/- 1hr")

		ax[1].set_ylabel(r'Sources', fontsize=18, fontweight='bold', color='#000000', labelpad=30)
		plt.ylim(0, cnt + 3)

		ax[0].grid()
		ax[0].set_xlabel('LST')
		ax[0].xaxis.labelpad = 20
		ax[0].yaxis.labelpad = 20

		ax[1].axes.get_yaxis().set_ticks([])
		ax[1].set_xlabel('UT')
		ax[1].xaxis.tick_top()
		ax[1].xaxis.set_label_position('top')
		ax[1].xaxis.labelpad = 20
		
		legend1 = ax[0].legend(loc='upper center', shadow=True, labelspacing=0.01, ncol=4, bbox_to_anchor=(0.5, 1.))
		
		fightml = mpld3.fig_to_html(fig)

	logger.info("Finished computations, rendering...")
	return render_template('otool.html', form=request.form, plot=fightml, info=sep_message)

# Array masks don't plot with mpld3
def produceSegments(elevArray, minElevation):
	"""Replace entries in the elevation array with NaNs if they are below the elevation selected by the user."""
	targetVisibility = np.ones(len(elevArray))
	for i, elev in enumerate(elevArray):
		if elev < minElevation:
			targetVisibility[i] = np.nan

	return targetVisibility

def createFixedBody(ra, dec, epoch):
	"""Fixed body adapted to us."""
	fixedBody = ephem.FixedBody()
	fixedBody._ra = ra
	fixedBody._dec = dec
	fixedBody._epoch = epoch
	return fixedBody

class Target(object):
	"""Encapsulates celestial bodies."""
	def __init__(self, name="", body=None, elevation=[], note = ""):
		self.name = name
		self.body = body
		self.elevation = elevation
		self.note = note
	
@app.route('/otool/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

# Home page
@app.route('/otool/')
def otool():
	"""The landing page"""
	return render_template('otool.html')

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	app.run(debug=True)
	logger.info("Server running.")
    #app.run()
    #app.run(host='0.0.0.0')
