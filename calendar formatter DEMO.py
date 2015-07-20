#I have no idea what i am doing
#get icalendar from https://github.com/collective/icalendar
from icalendar import Calendar, Event
from datetime import datetime, date
cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')
#somebullshit
import pytz
todaysdate = date.today()
#this creates a variable for today's date


#define the calendar display
def display(cal):
	return cal.to_ical().replace('\r\n', '\n').strip()

#begin to construct and event
evnum = 0 #this is for the initial uid, and will increase once every itteration.

g = open('calendar.ics','rb') #this is where the file you are going to read is

gcal = Calendar.from_ical(g.read())
futureEvents = []
brokenEvents = []
repeatEvents = []

for component in gcal.walk():
	#walk through each event
	if component.name == "VEVENT":
		evnum = evnum+1
		event = Event()
		event['uid'] = evnum
		cstart = component.get('dtstart')
		eventtime = cstart.dt
		csummary = component.get('summary')
		cdesc = component.get('Description')
		cend = component.get('dtend')
		cloc = component.get('Location')
		corg = component.get('Organizer')
		cstatus = component.get('Status')
		cFreq = component.get('Rrule')
		try:
			corgname = corg.params['CN']
		except:
			pass
		try: #can we convert the date and time into just a date?
			eventdate = eventtime.date()
		except:
			pass
		#get the event atendees
		eventAttendees = component.get('ATTENDEE')
		if component.get('ATTENDEE'):
			attendeesTable = []
			eventAttendees = component.get('ATTENDEE')
			for People in eventAttendees:
				try:
					if People.params['CUTYPE'] == "INDIVIDUAL":
						try:
							attendeesTable.append(str(People.params['EMAIL']))
						except:
							attendeesTable.append(str(People.params['CN']))
				except:
					pass
		try:
			event['summary'] = csummary
		except:
			pass
		try:
			event['Organizer'] = corgname
		except:
			pass
		try:
			event['Location'] = cloc
		except:
			pass
		try:
			event['Description'] = cdesc
		except:
			pass
		try:
			event['dtstart'] = cstart
		except:
			pass
		try:
			event['dtend'] = cend
		except:
			pass
		try:
			event['status'] = cstatus
		except:
			pass 
		try:
			event['RRULE'] = cFreq
		except:
			pass
		try:
    			event['attendee'] = attendeesTable
		except:
			print ""
		try:
			print "Event Success " + str(csummary) + " #:"+ str(evnum)
		except:
			print "Event success " + str(evnum)
#OK, EVERYTHING IS HELD IN A TABLE NOW -- LETS FIND EVENTS THAT REOCCURE
		if cFreq:
			eventfacts = []
			try:
				eventfacts.append(str(csummary))
			except:
				pass
			try:
				eventfacts.append(str(cdesc))
			except:
				pass
			try:
				eventfacts.append(str(cloc))
			except:
				pass
			try:
				eventfacts.append(str(corgname))
			except:
				pass
			try:
				eventfacts.append(str(cstatus))
			except:
				pass
			repeatEvents.append(eventfacts)
#THIS IS THE MOMENT!
		if eventdate <= todaysdate:
			cal.add_component(event) #add the table to the new calendar
#The moment is over, damn... always so fast.
		else:
			dateRational = "The event: " + str(csummary) + " -- had a eventdate of: " + str(eventdate) + " -- which is greater than today: " + str(todaysdate) + " -- Here are the details"
			eventfacts = []
			futureEvents.append(dateRational)
			try:
				eventfacts.append(str(csummary))
			except:
				pass
			try:
				eventfacts.append(str(cstart.dt))
			except:
				pass
			try:
				eventfacts.append(str(cend.dt))
			except:
				pass
			try:
				eventfacts.append(str(cdesc))
			except:
				pass
			try:
				eventfacts.append(str(cloc))
			except:
				pass
			try:
				eventfacts.append(str(corgname))
			except:
				pass
			try:
				eventfacts.append(str(cstatus))
			except:
				pass
			futureEvents.append(eventfacts)
			futureEvents.append(" ")
			#Future Events finished
			#Now print out the future events in a readable way
print "---FINAL STATUS---"
print "The following events were not added because they are future events: "
print "/summary/         /description/       /location/      /organizer/     /status/ "
for subevent in futureEvents:
	print subevent
#write to file
print "------------------------------"
print "The following events were not added because they are generally messed up: "
print "/summary/         /description/   /Start/      /END/       /location/      /organizer/     /status/ "
for subevent in brokenEvents:
	print subevent
print "------------------------------"
print "The following events were repeating events, that MAY OR MAY NOT need to be recreated for the future"
print "/summary/         /description/       /location/      /organizer/     /status/ "
for subevent in repeatEvents:
	print subevent
import tempfile, os
directory = tempfile.mkdtemp()
f = open(os.path.join('/CalenderParser', 'cleanedupcalendar.ics'), 'w')
f.write(cal.to_ical())
f.close
g.close()