# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
import requests
import xml.etree.ElementTree as ET
from cgi import print_environ
import requests,json
from datetime import date
from datetime import time,datetime
import xmltodict
from os import name
from os import name
from collections import namedtuple
# import frappe
# from numpy import empty
# import pandas as pd
import json
import datetime
# from frappe.permissions import check_admin_or_system_manager
# from frappe.utils.csvutils import read_csv_content
# from six.moves import range
# from six import string_types
# from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
# 	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime,date
from calendar import monthrange
# from frappe import _, msgprint
# from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from os import name
from os import name
from collections import namedtuple
import frappe

from numpy import empty
import pandas as pd
import json
import datetime
from frappe.permissions import check_admin_or_system_manager
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests

from datetime import date, timedelta,time
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_url_to_form
import math

from datetime import date, timedelta,time
# from frappe.utils.background_jobs import enqueue
# from frappe.utils import get_url_to_form
import math

from frappe.model.document import Document

class EmployeeCheckinsProcess(Document):
	pass



	
