from django.http import HttpResponse
import json


class ScheduleClass:
    def __init__(self, opening_hours):
        self.opening_hours = opening_hours

    def schedule(self):
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        result = ""

        for day in days:
            hours = self.opening_hours.get(day, [])
            if not hours:
                result += f"{day.capitalize()}: Closed\n"
            else:
                formatted_hours = []
                i = 0
                while i < len(hours):
                    if hours[i]['type'] == 'open':
                        open_hour = self.fromUnix(hours[i]['value'])
                        if i + 1 < len(hours) and hours[i + 1]['type'] == 'close':
                            close_hour = self.fromUnix(hours[i + 1]['value'])
                            formatted_hours.append(f"{open_hour} - {close_hour}")
                            i += 2
                        else:
                            next_day = days[(days.index(day) + 1) % 7]
                            next_day_hours = self.opening_hours.get(next_day, [])
                            if next_day_hours and next_day_hours[0]['type'] == 'close':
                                close_hour = self.fromUnix(next_day_hours[0]['value'])
                                formatted_hours.append(f"{open_hour} - {close_hour}")
                                i += 1
                            else:
                                formatted_hours.append(f"{open_hour} - For last client")
                                i += 1
                    else:
                        i += 1

                result += f"{day.capitalize()}: {', '.join(formatted_hours)}\n"

        return result

    @staticmethod
    def fromUnix(time):
        hour = int(time / 3600) % 24
        minute = int((time % 3600) / 60)
        if hour < 12:
            suffix = "AM"
        else:
            suffix = "PM"
        if hour <= 12:
            hour = hour
        else:
            hour = hour - 12
        return f"{hour:02d}:{minute:02d} {suffix}"

def Schedule_endpoint(request):
    data = {
        "monday": [],
        "tuesday": [
            {
                "type": "open",
                "value": 36000
            },
            {
                "type": "close",
                "value": 64800
            }
        ],
        "wednesday": [],
        "thursday": [
            {
                "type": "open",
                "value": 37800
            },
            {
                "type": "close",
                "value": 64800
            }
        ],
        "friday": [
            {
                "type": "open",
                "value": 36000
            }
        ],
        "saturday": [
            {
                "type": "close",
                "value": 3600
            },
            {
                "type": "open",
                "value": 36000
            }
        ],
        "sunday": [
            {
                "type": "close",
                "value": 3600
            },
            {
                "type": "open",
                "value": 43200
            },
            {
                "type": "close",
                "value": 75600
            }
        ]
    }
    json_data = request.body.decode('utf-8')
    if json_data == '':
        json_data = json.dumps(data)
    data = json.loads(json_data)
    converter = ScheduleClass(data)
    output = converter.schedule()
    response = f'<pre>{output}</pre>'
    return HttpResponse(response)