#!/usr/bin/env python3
import re
import sys
import datetime

class process_cal:
    
    class event:

        def __init__(self, dtstart, dtend, rrule, locaiton, summary):
            """Creates a event object with the respected values passed in"""

            self.dtstart = dtstart
            self.dtend = dtend
            self.rrule = rrule
            self.location = locaiton
            self.summary = summary


        def __repr__(self):
            """__repr__ function for event class"""

            return "event(%r, %r, %r, %r, %r)" % (self.dtstart, self.dtend, self.rrule, self.location, self.summary)


        def is_valid_date(self, date):
            """Returns boolean if date passed in is equal to the date of self"""

            date = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
            extracted_event_date = re.search(r"(20\d{2})(\d{2})(\d{2})", self.dtstart)
            extracted_event_date = extracted_event_date.group(1) + extracted_event_date.group(2) + extracted_event_date.group(3)
            
            return date == extracted_event_date

        def get_event_dashes(self, date_header):
            """Genereates required ammount of dashes needed for output"""

            dashes = ''
            for i in range(len(date_header)):
                dashes += '-'

            return dashes

        def return_event_info_str(self, start_time, start_ampm, end_time, end_ampm, summary, locaiton):
            """"Returns a string of the event info that will appear in final output
                Note: This does not return the header for the event date
            """

            event_info = '''==STARTTIME== ==STARTAMPM== to ==ENDTIME== ==ENDAMPM==: ==SUMMARY== {{==LOCATION==}}'''

            event_info_final = re.sub('==STARTTIME==', start_time, event_info).rjust(76)
            
            event_info_final = re.sub('==STARTAMPM==', start_ampm, event_info_final)

            event_info_final = re.sub('==ENDTIME==', end_time.rjust(5), event_info_final)
                
            event_info_final = re.sub('==ENDAMPM==', end_ampm, event_info_final)
            event_info_final = re.sub('==SUMMARY==', self.summary, event_info_final)
            event_info_final = re.sub('==LOCATION==', self.location, event_info_final)

            return event_info_final


        def generate_output(self, is_first):
            """Generates the required output to the terminal, returns the full string back to get_events_for_day"""

            final_str = ''

            extracted_event_datetime = re.search(r"(20\d{2})(\d{2})(\d{2})T(\d{2})(\d{2})", self.dtstart)
            extracted_end_datetime = re.search(r"(20\d{2})(\d{2})(\d{2})T(\d{2})(\d{2})", self.dtend)
            date = datetime.date(int(extracted_event_datetime.group(1)), int(extracted_event_datetime.group(2)), int(extracted_event_datetime.group(3)))
            start_time_obj = datetime.time(int(extracted_event_datetime.group(4)), int(extracted_event_datetime.group(5)))
            end_time_obj = datetime.time(int(extracted_end_datetime.group(4)), int(extracted_end_datetime.group(5)))


            date_header = '''==MONTH== ==DAY==, ==YEAR== (==FULLDAY==)'''
            year = date.strftime("%Y")
            month = date.strftime("%B")
            day = date.strftime("%d")
            str_day = date.strftime("%a")

            start_time = start_time_obj.strftime('%-I') + ':' + start_time_obj.strftime('%M')
            start_ampm = start_time_obj.strftime('%p')

            end_time = end_time_obj.strftime('%-I') + ':' + end_time_obj.strftime('%M')
            end_ampm = end_time_obj.strftime('%p')

            if (is_first):
                #If it is the first occurance of a new date, then we want to genereate the "date header"
                date_header_final = re.sub('==MONTH==', month, date_header)
                date_header_final = re.sub('==DAY==', day, date_header_final)
                date_header_final = re.sub('==YEAR==', year, date_header_final)
                date_header_final = re.sub('==FULLDAY==', str_day, date_header_final)
                dashes = self.get_event_dashes(date_header_final)
                event_info = self.return_event_info_str(start_time, start_ampm, end_time, end_ampm, self.summary, self.location)
                final_str += date_header_final + "\n" + dashes + "\n" + event_info
            else:
                event_info = self.return_event_info_str(start_time, start_ampm, end_time, end_ampm, self.summary, self.location)
                final_str += event_info

            return final_str


    def __init__(self, filename):
        """Creates new process_cal with the filename"""

        self.filename = filename

    def __repr__(self):
        """__repr__ function for process_cal class"""

        return "process_cal(%r)" % (self.filename)

    def get_events_for_day(self, date):
        """This function acts as the main(), calling all required Functions / Methods to generate the desired output"""

        is_first = 1
        output_str = ''
        empty_str = ''
        all_events = self.process_file()
        all_events = self.handle_rrules(all_events)

        for event in all_events:
            if event.is_valid_date(date):
                output_str += event.generate_output(is_first) + "\n"
                is_first = 0
        
        #Removing the last occurnace of a \n
        output_str = empty_str.join(output_str.rsplit('\n', 1))

        return output_str

    def handle_rrules(self, events):
        """Creates new events based off RRULE of event"""

        rrule = ""
        for event in events:
            if event.rrule != "":
                split_rrule = re.split('[=, ;]', event.rrule)
                #Checking if it includes WKST, if so then we want to grab another index
                if(split_rrule[4] == "UNTIL"):
                    rrule_date = split_rrule[5]
                else:
                    rrule_date = split_rrule[3]
                #Converting rrule and dtstart date to datetime objects
                rrule_date = re.search(r"(20\d{2})(\d{2})(\d{2})", rrule_date)
                current_date = re.search(r"(20\d{2})(\d{2})(\d{2})", event.dtstart)

                end_date =  datetime.date(int(rrule_date.group(1)), int(rrule_date.group(2)), int(rrule_date.group(3)))
                current_date = datetime.date(int(current_date.group(1)), int(current_date.group(2)), int(current_date.group(3)))
                
                while((current_date + datetime.timedelta(days=7)) <= end_date):
                    current_date += datetime.timedelta(days=7)
                    #We do not need to change the dtend values, this is because we only need to use the time from it and not the date, and the time will stay the same regardless if the event is taking place on another day
                    converted_date_format =  str(current_date).replace("-","") + "T" + event.dtstart[9:]
                    e = process_cal.event(converted_date_format, event.dtend, rrule, event.location, event.summary)
                    events.append(e)

        return events


    def process_file(self):
        """Opens, Parses, and puts required data into its own event object from the passed in file"""

        event_list = []
        ics_data = open(self.filename, 'r')

        for line in ics_data:

            line = line.rstrip('\n')

            #checking if the line is empty
            if(line == ""):
                continue

            split_line = re.split('[:]', line)

            prop = split_line[0]
            value = split_line[1]

            if(prop == "DTSTART"):
                dtstart = value
            if(prop == "DTEND"):
                dtend = value
            if(prop == "RRULE"):
                rrule_flag = True
                rrule = value
            if(prop == "LOCATION"):
                location = value
            if(prop == "SUMMARY"):
                summary = value

            if(prop == 'END' and value == 'VEVENT'):
                if(rrule_flag == False):
                    rrule = ""
                e = process_cal.event(dtstart, dtend, rrule, location, summary)
                event_list.append(e)

            if(prop == 'BEGIN' or value == 'END'):
                rrule_flag = False
                continue
                

        return event_list










