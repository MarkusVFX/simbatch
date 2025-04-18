class Logger:
    # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    console_level = 0
    log_file_level = 0
    log_file_path = ""
    force_add_to_log = False
    buffering = False
    buffer = []
    err_buffer = []

    def __init__(self, log_level=0, console_level=3):
        if console_level is None or console_level > 4:
            print("Logger init")
        self.console_level = console_level
        self.log_file_level = log_level

    def dispatch(self, level, message, force_print=False, raw=False, nl=False, nla=False, force_prefix=None):
        if self.console_level >= level or force_print:
            console_print = True
        else:
            console_print = False

        if self.log_file_level >= level:
            log_append = True
        else:
            log_append = False

        if force_prefix is not None:
            indent = "       "
            prefix = force_prefix
        elif level == 1:
            indent = ""
            prefix = "ERR"
            self.err_buffer.append(message)
        elif level == 2:
            indent = "  "
            prefix = "WRN"
        elif level == 3:
            indent = "    "
            prefix = "INF"
        elif level == 4:
            indent = "     "
            prefix = "DB"
        elif level == 5:
            indent = "     __"
            prefix = "deep"
        elif level == 6:
            indent = "     __"
            prefix = "LOG"
        else:
            indent = "'"
            prefix = "_"

        if console_print:
            if nl:
                print("\n")
            if raw:
                print(message)
            else:
                if isinstance(message, tuple):
                    out = "  ".join(str(el) for el in message)
                    print(f"{indent}[{prefix}]  {out}")
                else:
                    print(f"{indent}[{prefix}]  {message}")
            if nla:
                print("\n")

        if self.force_add_to_log or log_append:
            self.add_to_log(prefix, message)

        if self.buffering is True:
            self.buffer.append(message)

    def err(self, message, force_print=False, nl=False, nl_after=False):
        self.dispatch(1, message, force_print=force_print, nl=nl, nla=nl_after)

    def wrn(self, message, force_print=False, nl=False, nl_after=False):
        self.dispatch(2, message, force_print=force_print, nl=nl, nla=nl_after)

    def inf(self, message, force_print=False, nl=False, nl_after=False, force_prefix=None):
        self.dispatch(3, message, force_print=force_print, nl=nl, nla=nl_after, force_prefix=force_prefix)

    def db(self, message, force_print=False, nl=False, nl_after=False):
        self.dispatch(4, message, force_print=force_print, nl=nl, nla=nl_after)

    def deepdb(self, message, force_print=False, nl=False, nl_after=False):
        self.dispatch(5, message, force_print=force_print, nl=nl, nla=nl_after)

    def log(self, message, force_print=False, nl=False, nl_after=False):
        self.dispatch(6, message, force_print=force_print, nl=nl, nla=nl_after)
        self.add_to_log("TODO")  # TODO

    def raw(self, message, force_print=False, nl=False, nl_after=False, raw=True, force_prefix=None):
        self.dispatch(3, message, force_print=force_print, nl=nl, nla=nl_after, raw=raw, force_prefix=force_prefix)

    def int(self, message, force_print=False, nl=False, nl_after=False):        # interaction info
        self.dispatch(3, message, force_print=force_print, nl=nl, nla=nl_after, force_prefix="INT")

    def clear_buffer(self):
        self.buffer.clear()

    def clear_err_buffer(self):
        self.err_buffer.clear()

    def get_buffer(self):
        return self.buffer

    def get_err_buffer(self):
        return self.err_buffer

    def print_err_buffer(self):
        for err in self.err_buffer:
            self.raw(err, force_print=True, force_prefix="//")

    def buffering_on(self):
        self.buffering = True

    def buffering_off(self):
        self.buffering = False

    def set_log_level(self, lvl):
        self.log_file_level = lvl

    def set_console_level(self, lvl):
        self.console_level = lvl

    def add_to_log(self, prefix, message):
        pass
        # TODO !!!

    def print_all(self):
        print("\n\n\n")
        print("Logger")
        print("  log_level: {}".format(self.log_file_level))
        print("  log_file: {}".format(self.log_file_path))
        print("  log_file_max_size: {}".format(self.log_file_max_size))
        print("  log_file_max_count: {}".format(self.log_file_max_count))
        print("  log_file_current_size: {}".format(self.log_file_current_size))
        print("  log_file_current_count: {}".format(self.log_file_current_count))
        print("  log_file_current_name: {}".format(self.log_file_current_name))
        print("  log_file_current_path: {}".format(self.log_file_current_path))
        print("  log_file_current_dir: {}".format(self.log_file_current_dir))
        print("  log_file_current_ext: {}".format(self.log_file_current_ext))
        print("  log_file_current_base: {}".format(self.log_file_current_base))
        print("  log_file_current_date: {}".format(self.log_file_current_date))
        print("  log_file_current_time: {}".format(self.log_file_current_time))
        print("  log_file_current_datetime: {}".format(self.log_file_current_datetime))
        print("  log_file_current_timestamp: {}".format(self.log_file_current_timestamp))
        print("  log_file_current_line_count: {}".format(self.log_file_current_line_count))
        print("  log_file_current_char_count: {}".format(self.log_file_current_char_count))
        print("  log_file_current_word_count: {}".format(self.log_file_current_word_count))
        print("  log_file_current_byte_count: {}".format(self.log_file_current_byte_count))
        print("  log_file_current_kb_count: {}".format(self.log_file_current_kb_count))
        print("  log_file_current_mb_count: {}".format(self.log_file_current_mb_count))
        print("  log_file_current_gb_count: {}".format(self.log_file_current_gb_count))
        print("  log_file_current_tb_count: {}".format(self.log_file_current_tb_count))
        print("  log_file_current_pb_count: {}".format(self.log_file_current_pb_count))
        print("  log_file_current_eb_count: {}".format(self.log_file_current_eb_count))
        print("  log_file_current_zb_count: {}".format(self.log_file_current_zb_count))
        print("  log_file_current_yb_count: {}".format(self.log_file_current_yb_count))

    def print_this(self):
        print("   [INF] Logger: ")
        print("       debug level: {}".format(self.debug_level))
        print("       console print: {}".format(self.console_print))
        print("       file print: {}".format(self.file_print))
        print("       log file: {}".format(self.log_file))
        print("       log file path: {}".format(self.log_file_path))
        print("       log file name: {}".format(self.log_file_name))
        print("       log file extension: {}".format(self.log_file_extension))
        print("       log file full path: {}".format(self.log_file_full_path))
        print("       log file full name: {}".format(self.log_file_full_name))
        print("       log file full extension: {}".format(self.log_file_full_extension))
        print("       log file full path: {}".format(self.log_file_full_path))
        print("       log file full name: {}".format(self.log_file_full_name))
        print("       log file full extension: {}".format(self.log_file_full_extension))
