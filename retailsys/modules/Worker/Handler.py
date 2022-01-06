import time


def UI_control(Bunch):

    def UI_control_lowskill(function):
        def wrapper(*args, **kwargs):
            while 1:
                try:
                    ret = function(*args, **kwargs)
                    if ret and type(ret) == bool:
                        return False
                    return ret
                except Exception as e:

                    # write_log('line_error', e, self.numb)
                    error_api.change_position(e, 1)
                    command = error_api.wait_change_position()
                    if command == 'next':
                        break
                    elif command == 'cans':
                        # exit
                        return True
                    elif command == 'repeat':
                        continue
            # next
            return False
        return wrapper
    return UI_control_lowskill


def Waiter(count, element_finder=None, can_skip=False):
    time_start = time.time()
    match type_sleep, count, element_finder, can_skip:
        case "last", count, element_finder, can_skip:
            time.sleep(count * TIME_DELAY_PERC)
        case "fast", count, None, can_skip:
            if not can_skip:
                time.sleep(count * TIME_DELAY_PERC)
        case "fast", count, element_finder, can_skip:
            start = time.time()
            while 1:
                if time.time() - start > MAX_TIME_WAIT:
                    self.write_log('line_delay_max_time', json.dumps({
                        "time_delta": round(time.time() - time_start, 5),
                        "line_status": self.Status.get_status(),
                        "TYPE_SLEEP": self.type_sleep,
                        "can_skip": can_skip,
                        "count": count,
                        "element_finder": 0 if element_finder is None else 1
                    }), self.numb)
                    raise FinderTooTime(self.numb, MAX_TIME_WAIT)
                try:
                    return element_finder()
                except:
                    pass


    self.write_log('line_delay', json.dumps({
        "time_delta": round(time.time() - time_start, 5),
        "line_status": self.Status.get_status(),
        "TYPE_SLEEP": self.type_sleep,
        "can_skip": can_skip,
        "count": count,
        "element_finder": 0 if element_finder is None else 1
    }), self.numb)


def ErrorChecker():
    errors = [lambda i: "invalid-feedback"]
    try:
        errors = [i.text for i in self.web_driver.find_elements(By.CLASS_NAME, "invalid-feedback")]
        if errors != '':
            self.write_log("invalid-feedback", ' | '.join(errors), self.numb)
            if call_solver:
                return self.error_solver(self.ErrorSheet.get_error_description(errors[0]))
        else:
            return False
    except:
        pass
    return False


def ErrorSolver():
    pass