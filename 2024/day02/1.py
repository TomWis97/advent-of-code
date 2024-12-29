from base import AoCBase
b = AoCBase()
b.parse_args()

safe_reports = 0
for report in b.source_data:
    levels = [ int(x.strip()) for x in report.split(' ') ]
    last_level = None
    last_direction_up = None  # Can be None, True or False
    safe = True
    for level in levels:
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
        b.debug("Report '{}' is safe".format(report))
        safe_reports += 1
print(safe_reports)
