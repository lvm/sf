#!/usr/bin/env python

import os
import wave
import math
import argparse

# vars

WAVE_DIR = "./samples"

# objects

class O(object):
    def __init__(self, *args, **kwargs):
        return setattr(self, '__dict__', kwargs)

    def __repr__(self):
        _repr = "Object"
        if self.name:
            _repr = self.name

        return "<W: %s>" % _repr


class W(O):
    pass


class D(O):
    def __init__(self, *args, **kwargs):
        super(D, self).__init__(*args, **kwargs)

    def filelist(self):
        if self.filelist:
            return self.filelist

# funcs


to_seconds = lambda frames: math.ceil(float(frames)/1000)
is_wave = lambda fname: '.wav' in fname

def open_w(w_file):
    w_frate = -1
    w_frames = -1

    try:
        w_file_obj = wave.open(w_file)
        w_frate = w_file_obj.getframerate()
        w_frames = w_file_obj.getnframes()
        w_file_obj.close()
    except:
        pass

    return W(name=os.path.basename(w_file), framerate=w_frate,
             length=to_seconds(w_frames))


def w_list(w_dir):
    dir_dict = {}
    if w_dir and os.path.isdir(w_dir):
        for root, directories, files in os.walk(w_dir):
            if not root.endswith("CVS"):
                if root not in dir_dict.keys():
                    root_name = os.path.basename(root)
                    dir_dict[root_name] = map(open_w,
                                              filter(is_wave, map(lambda f: os.path.join(root, f), files)))

    return dir_dict


# params

def fn_search_time(samples, cmp_result, length, verbose):
    result = []
    length = float(length)
    for smp in samples:
        match = filter(lambda w: cmp(w.length, length) == cmp_result, samples[smp])
        if match:
            if verbose:
                result.append( (smp, match) )
            else:
                result.append(smp)

    return result


def fn_search(s_by, s_what, verbose):
    """
 Search `samples` by different methods.
  --time + --less-than
  --time + --greater-than
  --time + --equal-to
  --name
Also with -v prints also the wave files within.
    """
    result = []
    samples = w_list(WAVE_DIR)

    if s_by == "name":
        result = filter(lambda smp: s_what in smp, samples.keys())
    else:
        cmp_result = 0
        if s_by == "lt":
            cmp_result = -1

        if s_by == "gt":
            cmp_result = 1

        result = fn_search_time(samples, cmp_result, s_what, verbose)

    return result

def fn_ls(verbose):
    """
Prints the `samples`. With -v prints also the wave files within.
    """
    samples = w_list(WAVE_DIR)
    result = []
    if verbose:
        for smp in samples:
            result.append((smp, samples[smp]))
    else:
        result = map(lambda smp: "%s (%d)" % (smp, len(samples[smp])), samples.keys())

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search',
                        action="store_true",
                        help=fn_search.__doc__)

    parser.add_argument('-t', '--time',
                        action="store_true",
                        help=fn_search.__doc__)

    parser.add_argument('-lt', '--less-than',
                        type=str,
                        help=fn_search.__doc__)

    parser.add_argument('-gt', '--greater-than',
                        type=str,
                        help=fn_search.__doc__)

    parser.add_argument('-eq', '--equal-to',
                        type=str,
                        help=fn_search.__doc__)

    parser.add_argument('-n', '--name',
                        type=str,
                        help=fn_search.__doc__)

    parser.add_argument('-ls', '--list',
                        action="store_true",
                        help=fn_ls.__doc__)

    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help=fn_ls.__doc__)

    args = parser.parse_args()

    if args.search:
        if args.time:
            if args.less_than:
                print fn_search("lt", args.less_than, args.verbose)

            if args.equal_to:
                print fn_search("eq", args.equal_to, args.verbose)

            if args.greater_than:
                print fn_search("gt", args.greater_than, args.verbose)

        elif args.name:
            print fn_search("name", args.name, args.verbose)

    elif args.list:
        print fn_ls(args.verbose)
