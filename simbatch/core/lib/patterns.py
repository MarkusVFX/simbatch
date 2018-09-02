from filesystem import FileSystemOperations
from common import CommonFunctions
from logger import Logger


class Patterns:    # TODO  TESTS !!!!
    patterns = None
    fso = None
    comfun = None

    def __init__(self):
        self.fso = FileSystemOperations()
        self.logger = Logger(log_level=0, console_level=3)
        self.comfun = CommonFunctions(self.logger)

    """ convert string    'BNd  2      44; sTr 1 2  '   to  'BND  2.0  44.0 ;  STR  1.0  2.0'   """
    def get_evolutions_from_string(self, evo_str):
        out_evos_array = []
        evos_arr = evo_str.split(";")
        evo_count_all = 1
        for e in evos_arr:  # TODO   optimize !!!
            e = e.replace("_", "")
            e_arr = e.split()
            counter = 0
            clean_arrr = []
            evo_count_param_vals = 0
            passed_abbreviation = False
            for eee in e_arr:
                counter += 1
                if counter > 1:
                    if passed_abbreviation:
                        if self.comfun.can_get_float(eee):
                            exist = 0
                            for c in clean_arrr:
                                if c == str(float(eee)):
                                    exist = 1
                            if exist == 0:
                                clean_arrr.append(str(float(eee)))
                                evo_count_param_vals += 1
                else:
                    if len(eee) == 3:
                        eee = eee.upper()
                        clean_arrr.append(eee)
                        passed_abbreviation = True

            if evo_count_param_vals > 0:
                evo_count_all *= evo_count_param_vals

            if passed_abbreviation:
                out_evos_array.append(clean_arrr)

        return evo_count_all, out_evos_array

    def init_dir_patterns(self):
        patterns = []
        n = "n"  # number
        s = "s"  # string
        patterns.append(n)
        patterns.append(s + n)
        patterns.append(s + n + s)
        patterns.append(n + s)

        patterns.append(n + s + n)
        patterns.append(s + n + s + n)
        patterns.append(s + n + s + n + s)
        patterns.append(n + s + n + s)

        patterns.append(n + s + n + s + n)
        patterns.append(s + n + s + n + s + n)
        patterns.append(s + n + s + n + s + n + s)
        patterns.append(n + s + n + s + n + s)

        self.patterns = patterns

    @staticmethod
    def most_occured_number(arr):
        arr = sorted(arr)
        arr.append(123456789)
        last = -400
        counter = 0
        counter_max = 0
        number_max = -1
        for i in arr:
            if not i == last:
                if counter_max < counter:
                    counter_max = counter
                    number_max = last
                counter = 0
                last = i
            counter += 1
        return number_max

    def pre_pattern_get_s_n(self, stri):     # pre s n
        last_s_n = "."
        pattern_s_n = ""
        n_count = 0
        for i in range(0, len(stri)):
            j = stri[i]
            if j.isdigit():
                current_s_n = "n"
            else:
                current_s_n = "s"

            if not last_s_n == current_s_n:
                if current_s_n == "n":
                    n_count += 1
                last_s_n = current_s_n
                pattern_s_n += current_s_n
        return [pattern_s_n, n_count]

    def get_pattern_from_string(self, stri, is_final=False, number_types=("seq", "sh", "take")):
        print "  [db] get_pattern_from_string  ", stri, number_types   # TODO logger
        last_s_n = "."
        pattern_s_n = ""        # pattern type:  snsn
        pattern_final = ""      # seq<nr##>_sh<nr####>    <seq##>_<sh####>
        tmp_nr_str = ""
        number_types_index = 0
        for i in range(0, len(stri)):
            j = stri[i]
            if j.isdigit():
                current_s_n = "n"
            else:
                current_s_n = "s"
            if is_final is True:
                if current_s_n == "s":
                    if not last_s_n == current_s_n and i > 0:
                        pattern_final += "<" + number_types[number_types_index] + tmp_nr_str + ">"
                        number_types_index += 1
                        tmp_nr_str = ""
                    pattern_final += j
                else:
                    tmp_nr_str += "#"
            if not last_s_n == current_s_n:
                last_s_n = current_s_n
                pattern_s_n += current_s_n
        if len(tmp_nr_str) > 0:
            pattern_final += "<" + number_types[number_types_index] + tmp_nr_str + ">"

        if is_final is not True:
            return pattern_s_n
        else:
            return pattern_final

    def check_dir_pattern(self, level_arr):
        all_types = []
        for li in level_arr:
            pattern_s_n = self.get_pattern_from_string(li)
            ret = self.comfun.find_string_in_list(self.patterns, pattern_s_n)
            all_types.append(ret)
        ret = self.most_occured_number(all_types)
        if ret > -1:
            return self.patterns[ret]
        else:
            return ""

    def generate_final_pattern(self, arr, patt, lvl):
        for a in arr:
            ret = self.pre_pattern_get_s_n(a)       # pre SN
            pattern_s_n = ret[0]
            if pattern_s_n == patt:
                num_types = ["seq", "sh", "take"]
                print " \n\n [db] pre SN pattern", ret   # TODO  logger
                if ret[1] == 1:
                    if lvl == 2:
                        num_types = ["sh"]
                        print " over write num_types ", num_types  # TODO  logger
                    if lvl == 3:
                        num_types = ["take"]
                ret = self.get_pattern_from_string(a, is_final=True, number_types=num_types)
                print "     [db]   final paterrn : ", pattern_s_n, ret   # TODO  logger
                return ret

    def get_dir_patterns(self, dir, db=False):
        # self.fso.maxDirDepth = 1
        self.fso.arr_dirs = []          # TODO optimize   id: 12    del[:]
        self.fso.maxDirDepth = 0        # TODO optimize   id: 12
        self.fso.get_dir_depth(dir)     # TODO optimize   id: 12

        level1arr = []
        level2arr = []
        level3arr = []

        self.init_dir_patterns()

        for i in self.fso.arr_dirs:
            if db:
                print "self.fso.arr_dirs   ", i[0], "...", i[1], "...", i[2]     # TODO logger
            if i[0] == 1:
                level1arr.append(i[1])
            if i[0] == 2:
                level2arr.append(i[1])
            if i[0] == 3:
                level3arr.append(i[1])

        patt1 = ""
        most_occurred_pattern = self.check_dir_pattern(level1arr)
        if len(most_occurred_pattern) > 0:
            patt1 = self.generate_final_pattern(level1arr, most_occurred_pattern, 1)
        full_dir_pattern = patt1
        patt2 = ""
        most_occurred_pattern = self.check_dir_pattern(level2arr)
        if len(most_occurred_pattern) > 0:
            patt2 = self.generate_final_pattern(level2arr, most_occurred_pattern, 2)
            full_dir_pattern += "\\" + patt2  # TODO os.separator
        patt3 = ""
        most_occurred_pattern = self.check_dir_pattern(level3arr)
        if len(most_occurred_pattern) > 0:
            patt3 = self.generate_final_pattern(level3arr, most_occurred_pattern, 3)
            full_dir_pattern += "\\" + patt3  # TODO os.separator
        print "\n [db]  ret full_dir_pattern     ", full_dir_pattern     # TODO  logger
        return full_dir_pattern

    def get_seq_pattern(self, full_dir_pattern):
        p_arr = full_dir_pattern.split("\\")  # TODO os.separator
        if len(p_arr) > 0:
            return p_arr[0]
        else:
            return ""

    def get_sh_pattern(self, full_dir_pattern):
        p_arr = full_dir_pattern.split("\\")  # TODO os.separator
        if len(p_arr) > 1:
            return p_arr[1]
        else:
            return ""

    def get_take_pattern(self, full_dir_pattern):
        p_arr = full_dir_pattern.split("\\")  # TODO os.separator
        if len(p_arr) > 2:
            return p_arr[2]
        else:
            return ""
