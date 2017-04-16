# coding=utf-8

import os
import numpy as np

def read_skeleton_file(file_path):
    skeleton_file = open(file_path)
    lines = skeleton_file.readlines()
    frame_count = int(lines[0])
    positions = {}
    starts = {}
    ends = {}
    ind = 1

    for f in xrange(0, frame_count):
        body_count = int(lines[ind])
        ind = ind + 1
        for b in xrange(0, body_count):
            body_id = lines[ind].split(' ')[0]
            trackingState = lines[ind].split(' ')[9]

            if body_id not in positions:
                starts[body_id] = f

                positions[body_id] = np.zeros((frame_count, 25, 3))
            joint_count = int(lines[ind + 1])
            ind = ind + 2
            for j in xrange(0, joint_count):
                line = lines[ind + j]
                positions[body_id][f, j] = [
                    float(w) for w in line.split(' ')[0:3]]
            ends[body_id] = f
            ind = ind + joint_count

    body_var = {}
    for key, value in positions.iteritems():
        # if frame_count != len(np.trim_zeros(value[:, 1, 0])):
        # print file, key, frame_count, len(np.trim_zeros(value[:, 1, 0]))
        if ends[key] - starts[key] < 5:
            continue
        body_var[key] = 0
        for j in xrange(0, 25):
            body_var[key] += np.var(value[starts[key]:ends[key], j, 0]) + \
                             np.var(value[starts[key]:ends[key], j, 1]) + \
                             np.var(value[starts[key]:ends[key], j, 2])

    if bool(body_var):
        import operator
        chosen_body_id = sorted(body_var.iteritems(), key=operator.itemgetter(1))
        if len(chosen_body_id) == 1:
            pos = positions[chosen_body_id[0][0]]
            start = starts[chosen_body_id[0][0]]
            end = ends[chosen_body_id[0][0]] + 1
            return np.repeat(pos[start:end], 2, axis=1), start, end, frame_count, 1
        elif len(chosen_body_id) >= 2:
            start0 = starts[chosen_body_id[0][0]]
            end0 = ends[chosen_body_id[0][0]] + 1
            start1 = starts[chosen_body_id[1][0]]
            end1 = ends[chosen_body_id[1][0]] + 1
            coverage = float(min(end0, end1) - max(start0, start1)) / float(max(end0, end1) - min(start0, start1))

            if coverage > 0:
                pos0 = positions[chosen_body_id[0][0]][max(start0, start1):min(end0, end1)]
                pos1 = positions[chosen_body_id[1][0]][max(start0, start1):min(end0, end1)]
                return np.concatenate((pos0, pos1), axis=1), max(start0, start1), min(end0, end1), frame_count, 2
            else:
                pos0 = positions[chosen_body_id[0][0]][start0:end0]
                return np.repeat(pos0, 2, axis=1), start0, end0, frame_count, 2
    else:
        return None, None, None, frame_count, None

def normalize():
    pass

def image_generator():
    pass

if __name__ == '__main__':
    skeleton_root = '/home/zsy/data/nturgb+d_skeletons'
    print 1
    print skeleton_root
    for root, dirs, files in os.walk(skeleton_root):
        print 2
        for file in sorted(files):
            print 3
            basename = file.split('.')[0]
            # index = index + 1
            # print index,'/',len(files),file
            # if os.path.isfile("../data/NTU-RGB+D/ICMEW2017-TEST-2P/"+basename+".hdf5"):
            #     continue
            file_path = os.path.join(root, file)
            pos, start, end, frame_count, body_count = read_skeleton_file(file_path)
            print pos
            print start
            print end
            print frame_count
            print body_count
            
            break
    # pass
