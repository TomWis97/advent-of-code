from base import AoCBase
from copy import deepcopy
b = AoCBase()
b.parse_args()

safe_reports = 0
for report in b.source_data:
    current_report = [ int(x.strip()) for x in report.split(' ') ]
    b.debug("Current report", current_report)
    reports_to_check = [deepcopy(current_report)]
    reports_check_results = []
    for index in range(len(current_report)):
        temp_list = deepcopy(current_report)
        del temp_list[index]
        reports_to_check.append(temp_list)

    for check_report in reports_to_check:
        last_level = None
        last_direction_up = None  # Can be None, True or False
        safe = True
        for level in check_report:
            if last_level == None:
                last_level = level
                continue

            if level > last_level:
                current_direction_up = True
            elif level < last_level:
                current_direction_up = False
            elif level == last_level:
                safe = False

            if last_direction_up == None:
                last_direction_up = current_direction_up
            elif last_direction_up != current_direction_up:
                # Change of direction
                safe = False

            if abs(last_level - level) > 3:
                b.debug("Unsafe: {} - {} = {} ".format(last_level, level, abs(last_level - level)))
                safe = False
            last_level = level
        if safe:
            reports_check_results.append(True)
            b.debug("Report '{}' is safe".format(report))
        else:
            reports_check_results.append(False)
            b.debug("Report '{}' is UNSAFE".format(report))
    if True in reports_check_results:
        safe_reports += 1
print(safe_reports)
