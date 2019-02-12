# -*- coding:utf-8 -*-
role_dict = {
    "superuser": 0,
    "common_user": 1,
    "product": 2,
    "user": 3,
    "acl": 4
}

period_status = {
    0: "Creating",
    1: "Waiting to run",
    2: "Running",
    3: "Complete",
    4: "Failure",
    5: "Suspended",
    6: "Waiting cycle",
    7: "The %s group is running",
    8: "The %s group is completed",
    9: "Periodic operation",
    10: "Scheduled task running",
    11: "Cycle pause"
}

period_audit = {
    0: "Created a job",
    1: "Reopened the Job",
    2: "Continued parallelism",
    3: "Completed the job",
    4: "Failed Job",
    5: "Parallel suspended",
    7: "The first %s group begins",
    8: "The %s group is completed",
    9: "Start all",
    10: "Continued cycle",
    11: "Suspended cycle"
}