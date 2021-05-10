from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colorpapers_product.settings')
application = get_wsgi_application()
from django.conf import settings
from dashboard.data_queries import KEEPA_QUERIES
from dashboard.models import processExecutions
from datetime import datetime 
import threading
from multiprocessing import Process


# def executeThread(row):
#     print("THREAD STARTED>>>")
#     obj = KEEPA_QUERIES()
#     obj.executeNode(row)


class manageCrons:

    def __init__(self):
        self.START_NEW_PROCESS = False
        self.checkIfAnyProcessRunning()
        self.executeNewProcessIfAny()
    
    def executeNewProcessIfAny(self):
        if self.START_NEW_PROCESS is True:
            row_to_process = processExecutions.objects.filter(status='pending')
            for row in row_to_process:
                row.status='running'
                row.save()
                obj = KEEPA_QUERIES()
                obj.executeNode(row)
                # p = Process(target=executeThread, args=(row,))
                # p.start()
                break
        else:
            print("EXISITNG PROCESS IS RUNNING")

    
    def checkIfAnyProcessRunning(self):
        running_process = processExecutions.objects.filter(status='running')
        if int(running_process.count()) > 0:
            for row_object in running_process:
                current_datetime = datetime.now()
                execution_last_updated_time = row_object.updated_at
                current_datetime_object = datetime(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day, hour=current_datetime.hour,minute=current_datetime.minute)
                execution_last_updated_time = datetime(year=execution_last_updated_time.year, month=execution_last_updated_time.month, day=execution_last_updated_time.day, hour=execution_last_updated_time.hour,minute=execution_last_updated_time.minute)
                diffrence = current_datetime_object-execution_last_updated_time
                if int(diffrence.seconds) > 1800:
                    row_object.status = 'completed'
                    row_object.completed_at = datetime.now()
                    row_object.updated_at = datetime.now()
                    row_object.save()
                    self.START_NEW_PROCESS = True
                else:
                    self.START_NEW_PROCESS = False
                    break
        else:
            self.START_NEW_PROCESS = True
            
manageCrons()






