# This file is part of Qualified Caching-as-a-Service.
# BSD 3-Clause License
#
# Copyright (c) 2019, Intelligent-distributed Cloud and Security Laboratory (ICNS Lab.)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# title           : analyzer.py
# description     : python analyzer
# author          : Yunkon(Alvin) Kim
# date            : 20190228
# version         : 0.1
# python_version  : 3.6
# notes           : This file is an implementation of result analyzer for EDCrammer testlog
#                   in the Python Programming Language.
# ==============================================================================
import csv
import glob
import os

import numpy as np


def list_a2f_and_mean(mlist):
    return sum([float(i) for i in mlist], 0.0) / len(mlist)


def get_xy_projection_mean(list_3d, x, y):
    xy_list = [float(list_3d[i][x][y]) for i in range(len(list_3d))]
    xy_mean = list_a2f_and_mean(xy_list)
    return xy_mean


if __name__ == '__main__':

    directory = os.path.join('.', 'data')

    scenario_no = 1
    total_scenarios = 4

    while scenario_no <= total_scenarios:
        filename_format = str(scenario_no) + "-*"
        file_paths = glob.glob(os.path.join(directory, filename_format))
        list_len = len(file_paths)

        i = 0

        # check the fewest number of lines

        number_of_lines = []

        for filepath in file_paths:
            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                number_of_lines.append(sum(1 for row in reader))

            csvfile.close()

        minimum_cycle_number = min(number_of_lines) - 2

        running_times = []
        achieved_percentages = []
        feedbacks = []
        outputs = []
        difference_ratios = []
        variances = []
        standard_deviations = []

        # read csv files
        for filepath in file_paths:
            print(filepath)
            line_number = 1
            achieved_percentage = []
            feedback = []
            output = []
            difference_ratio = []
            variance = None
            standard_deviation = None

            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in reader:
                    if line_number == 1:
                        arr = ', '.join(row).split(',')
                        running_times.append(float(arr[2]))
                        line_number += 1
                    elif line_number == 2:
                        arr = ', '.join(row).split(',')
                        variance = float(arr[0])
                        standard_deviation = float(arr[1])
                        line_number += 1
                    else:
                        arr = ', '.join(row).split(',')
                        achieved_percentage.append(float(arr[1]))
                        feedback.append(float(arr[4]))
                        output.append(float(arr[2]))
                        difference_ratio.append(float(arr[5]))
                        line_number += 1

            # split a list based on minimum length because number of cycles are different due to processing time.
            achieved_percentages.append(achieved_percentage[0:minimum_cycle_number])
            feedbacks.append(feedback[0:minimum_cycle_number])
            outputs.append(output[0:minimum_cycle_number])
            difference_ratios.append(difference_ratio[0:minimum_cycle_number])
            variances.append(variance)
            standard_deviations.append(standard_deviation)
            csvfile.close()

        # Start analyzing
        # --------- Running time
        print("running_times: \n%s" % running_times)
        avg_running_times = sum(running_times) / len(running_times)
        print("Average Running Time: %s " % avg_running_times)

        # --------- Variance and standard deviation
        print("variances: \n%s" % variances)
        avg_variance = sum(variances) / len(variances)
        print("Average variances: %s " % avg_variance)

        print("standard_deviations: \n%s" % standard_deviations)
        avg_standard_deviation = sum(standard_deviations) / len(standard_deviations)
        print("Average standard deviation: %s " % avg_standard_deviation)

        # --------- Achieved percentages
        print("Length of achieved_percentages: %s" % len(achieved_percentages))
        print("achieved_percentages: \n%s" % achieved_percentages)

        # !IMPORTANCE, np.transpose does NOT work on for a jagged list of different lengths.
        transposed_ap = np.transpose(achieved_percentages)
        print("Length of transposed: %s" % len(transposed_ap))
        print("Transposed: \n%s" % transposed_ap)

        avg_achieved_percentages = []

        for values in transposed_ap:
            avg_achieved_percentages.append(sum(values) / len(values))

        print("Length of avg_achieved_percentages: %s" % len(avg_achieved_percentages))
        print("Average Achieved Percentages: \n%s" % avg_achieved_percentages)

        # --------- Feedbacks
        print("Length of feedbacks: %s" % len(feedbacks))
        print("feedbacks: \n%s" % feedbacks)

        # !IMPORTANCE, np.transpose does NOT work on for a jagged list of different lengths.
        transposed_f = np.transpose(feedbacks)
        print("Length of transposed: %s" % len(transposed_f))
        print("Transposed: \n%s" % transposed_f)

        avg_feedbacks = []

        for values in transposed_f:
            avg_feedbacks.append(sum(values) / len(values))

        print("Length of avg_achieved_percentages: %s" % len(avg_feedbacks))
        print("Average Achieved Percentages: \n%s" % avg_feedbacks)

        # --------- Outputs
        print("Length of outputs: %s" % len(outputs))
        print("Outputs: \n%s" % outputs)

        # !IMPORTANCE, np.transpose does NOT work on for a jagged list of different lengths.
        transposed_f = np.transpose(outputs)
        print("Length of transposed: %s" % len(transposed_f))
        print("Transposed: \n%s" % transposed_f)

        avg_outputs = []

        for values in transposed_f:
            avg_outputs.append(sum(values) / len(values))

        print("Length of avg_achieved_percentages: %s" % len(avg_outputs))
        print("Average Achieved Percentages: \n%s" % avg_outputs)

        # --------- difference_ratios
        print("Length of difference_ratios: %s" % len(difference_ratios))
        print("difference_ratios: \n%s" % difference_ratios)

        # !IMPORTANCE, np.transpose does NOT work on for a jagged list of different lengths.
        transposed_dr = np.transpose(difference_ratios)
        print("Length of transposed: %s" % len(transposed_dr))
        print("Transposed: \n%s" % transposed_dr)

        avg_difference_ratios = []

        for values in transposed_dr:
            avg_difference_ratios.append(sum(values) / len(values))

        print("Length of avg_achieved_percentages: %s" % len(avg_difference_ratios))
        print("Average Achieved Percentages: \n%s" % avg_difference_ratios)

        result_file_name = str(scenario_no) + "-result.csv"
        result_path = os.path.join(os.path.join(".", "result"), result_file_name)
        print(result_path)

        time_list = [i for i in range(minimum_cycle_number)]
        percentage_setpoint_list = [90 for i in range(minimum_cycle_number)]

        with open(result_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # print running time

            # print data
            for idx in range(minimum_cycle_number):
                writer.writerow(
                    [time_list[idx], avg_achieved_percentages[idx], (avg_outputs[idx] / (5 << 20) * 100),
                     percentage_setpoint_list[idx], avg_feedbacks[idx], avg_difference_ratios[idx]])

            writer.writerow([avg_running_times, minimum_cycle_number, avg_running_times/minimum_cycle_number])
            writer.writerow([avg_variance])
            writer.writerow([avg_standard_deviation])

        csvfile.close()

        # # ################ plot plot plot plot plot
        # time_sm = np.array(time_list)
        # time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
        #
        # # feedback_smooth = spline(time_list, percentage_list, time_smooth)
        # # Using make_interp_spline to create BSpline
        # helper_x3 = make_interp_spline(time_list, avg_achieved_percentages)
        # feedback_smooth = helper_x3(time_smooth)
        #
        # plt.plot(time_smooth, feedback_smooth)
        # plt.plot(time_list, percentage_setpoint_list)
        #
        # plt.xlim((0, len(percentage_setpoint_list)))
        # # plt.ylim((min(percentage_list) - 0.5, max(percentage_list) + 0.5))
        # # plt.ylim(0, 100)
        # plt.xlabel('time (s)')
        # plt.ylabel('PID (PV)')
        # plt.title('TEST PID')
        #
        # # plt.ylim((1 - 0.5, 1 + 0.5))
        #
        # plt.grid(True)
        # plt.show()

        # variation_list = [book[i][1][4] for i in range(len(book))]

        # read files of each scenario

        # open file

        # add running time

        # calc average of each cycle

        # calc gap of setpoint and c(t)

        # calc average of all cycle

        scenario_no += 1

# loop
# while scenario_no < 5:
#     filename_format = str(scenario_no) + "-*"
#     file_paths = glob.glob(os.path.join(directory, filename_format))
#     list_len = len(file_paths)
#
#     i = 0
#     book = []
#
#     # read csv files
#     for filepath in file_paths:
#         print(filepath)
#         with open(filepath, 'r', newline='') as csvfile:
#             reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#             page = []
#             for row in reader:
#                 arr = ', '.join(row).split(',')
#                 page.append(arr)
#         book.append(page)
#
#     print(book)
#     print(book[0])
#     print(book[1])
#     print(book[0][0])
#     print(book[0][0][2])
#
#     print("--- testing ---")
#     running_time_mean = get_xy_projection_mean(book, 0, 2)
#     print(running_time_mean)
#
#     print("Length: %s " % len(book[0]))
#     avg_percentage_list = [float(get_xy_projection_mean(book, i, 1)) for i in range(1, len(book[0])-1)]
#
#     time_list = [i for i in range(73)]
#     percentage_setpoint_list = [90 for i in range(73)]
#
#
#     # ################ plot plot plot plot plot
#     time_sm = np.array(time_list)
#     time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
#
#     # feedback_smooth = spline(time_list, percentage_list, time_smooth)
#     # Using make_interp_spline to create BSpline
#     helper_x3 = make_interp_spline(time_list, avg_percentage_list)
#     feedback_smooth = helper_x3(time_smooth)
#
#     plt.plot(time_smooth, feedback_smooth)
#     plt.plot(time_list, percentage_setpoint_list)
#
#     plt.xlim((0, len(percentage_setpoint_list)))
#     # plt.ylim((min(percentage_list) - 0.5, max(percentage_list) + 0.5))
#     # plt.ylim(0, 100)
#     plt.xlabel('time (s)')
#     plt.ylabel('PID (PV)')
#     plt.title('TEST PID')
#
#     # plt.ylim((1 - 0.5, 1 + 0.5))
#
#     plt.grid(True)
#     plt.show()
#
#     # variation_list = [book[i][1][4] for i in range(len(book))]
#
#     break
#         # read files of each scenario
#
#         # open file
#
#         # add running time
#
#         # calc average of each cycle
#
#         # calc gap of setpoint and c(t)
#
#         # calc average of all cycle
#
#     scenario_no += 1

